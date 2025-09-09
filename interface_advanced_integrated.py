import streamlit as st
import os
import json
from PIL import Image
import glob
import requests
from io import BytesIO
from deep_translator import GoogleTranslator
from clientTranslation import geez_to_latin_syllable
import random
import time
from typing import Optional, Dict, List
import streamlit.components.v1 as components

# Enhanced vocabulary dictionary with categories
VOCAB_CATEGORIES = {
    "colors": {
        "red": "ቀይሕ", "blue": "ሰማያዊ", "green": "ቀጠልያ", "yellow": "ቢጫ",
        "black": "ጸሊም", "white": "ጻዕዳ", "orange": "ኣራንቾኒ", 
        "purple": "ሊላ", "brown": "ቡናዊ"
    },
    "animals": {
        "dog": "ከልቢ", "cat": "ድሙ", "cow": "ላም", "lion": "ኣንበሳ",
        "horse": "ፈረስ", "goat": "ጤል", "chicken": "ዶርሆ", "fish": "ዓሳ",
        "sheep": "በጊዕ", "camel": "ገመል", "elephant": "ሓርማዝ", "monkey": "ህበይ",
        "zebra": "ኣድጊ በረኻ", "giraffe": "ዘራፍ", "snake": "ተመን", "tiger": "ነብሪ",
        "bear": "ድቢ", "donkey": "ኣድጊ", "rabbit": "ማንቲለ", "mouse": "ኣንጭዋ"
    },
    "objects": {
        "book": "መጽሓፍ", "pen": "ብርዒ", "chair": "ኩርሲ", "table": "ጣውላ",
        "car": "መኪና", "bus": "ኣውቶቡስ", "phone": "ተሌፎን", "hat": "ቆብዕ",
        "shoe": "ሳእኒ", "house": "ገዛ", "apple": "ቱፋሕ", "banana": "ባናና",
        "bed": "ዓራት", "cup": "ቢኬሪ", "key": "መፍትሕ", "door": "ማዕጾ", "bag": "ቦርሳ"
    }
}

# Flatten vocabulary for easy access
VOCAB_DICT = {}
for category, words in VOCAB_CATEGORIES.items():
    VOCAB_DICT.update(words)

# Enhanced Tigrinya alphabets with detailed structure
TIGRINYA_ALPHABETS = {
    "ሀ": {"base": "ሀ", "forms": ["ሀ", "ሁ", "ሂ", "ሃ", "ሄ", "ህ", "ሆ"], "phonetic": ["he", "hu", "hi", "ha", "hie", "h", "ho"]},
    "ለ": {"base": "ለ", "forms": ["ለ", "ሉ", "ሊ", "ላ", "ሌ", "ል", "ሎ"], "phonetic": ["le", "lu", "li", "la", "lie", "l", "lo"]},
    "ሐ": {"base": "ሐ", "forms": ["ሐ", "ሑ", "ሒ", "ሓ", "ሔ", "ሕ", "ሖ"], "phonetic": ["He", "Hu", "Hi", "Ha", "Hie", "H", "Ho"]},
    "መ": {"base": "መ", "forms": ["መ", "ሙ", "ሚ", "ማ", "ሜ", "ም", "ሞ"], "phonetic": ["me", "mu", "mi", "ma", "mie", "m", "mo"]},
    "ሰ": {"base": "ሰ", "forms": ["ሰ", "ሱ", "ሲ", "ሳ", "ሴ", "ስ", "ሶ"], "phonetic": ["se", "su", "si", "sa", "sie", "s", "so"]},
    "ረ": {"base": "ረ", "forms": ["ረ", "ሩ", "ሪ", "ራ", "ሬ", "ር", "ሮ"], "phonetic": ["re", "ru", "ri", "ra", "rie", "r", "ro"]},
    "ሸ": {"base": "ሸ", "forms": ["ሸ", "ሹ", "ሺ", "ሻ", "ሼ", "ሽ", "ሾ"], "phonetic": ["Se", "Su", "Si", "Sa", "Sie", "S", "So"]},
    "ቀ": {"base": "ቀ", "forms": ["ቀ", "ቁ", "ቂ", "ቃ", "ቄ", "ቅ", "ቆ"], "phonetic": ["qe", "qu", "qi", "qa", "qie", "q", "qo"]},
    "በ": {"base": "በ", "forms": ["በ", "ቡ", "ቢ", "ባ", "ቤ", "ብ", "ቦ"], "phonetic": ["be", "bu", "bi", "ba", "bie", "b", "bo"]},
    "ተ": {"base": "ተ", "forms": ["ተ", "ቱ", "ቲ", "ታ", "ቴ", "ት", "ቶ"], "phonetic": ["te", "tu", "ti", "ta", "tie", "t", "to"]},
    "ቸ": {"base": "ቸ", "forms": ["ቸ", "ቹ", "ቺ", "ቻ", "ቼ", "ች", "ቾ"], "phonetic": ["ce", "cu", "ci", "ca", "cie", "c", "co"]},
    "ነ": {"base": "ነ", "forms": ["ነ", "ኑ", "ኒ", "ና", "ኔ", "ን", "ኖ"], "phonetic": ["ne", "nu", "ni", "na", "nie", "n", "no"]},
    "ኘ": {"base": "ኘ", "forms": ["ኘ", "ኙ", "ኚ", "ኛ", "ኜ", "ኝ", "ኞ"], "phonetic": ["gne", "gnu", "gni", "gna", "gnie", "gn", "gno"]},
    "አ": {"base": "አ", "forms": ["አ", "ኡ", "ኢ", "ኣ", "ኤ", "እ", "ኦ"], "phonetic": ["ae", "u", "i", "a", "ie", "e", "o"]},
    "ከ": {"base": "ከ", "forms": ["ከ", "ኩ", "ኪ", "ካ", "ኬ", "ክ", "ኮ"], "phonetic": ["ke", "ku", "ki", "ka", "kie", "k", "ko"]},
    "ኸ": {"base": "ኸ", "forms": ["ኸ", "ኹ", "ኺ", "ኻ", "ኼ", "ኽ", "ኾ"], "phonetic": ["Ke", "Ku", "Ki", "Ka", "Kie", "K", "Ko"]},
    "ወ": {"base": "ወ", "forms": ["ወ", "ዉ", "ዊ", "ዋ", "ዌ", "ው", "ዎ"], "phonetic": ["we", "wu", "wi", "wa", "wie", "w", "wo"]},
    "ዘ": {"base": "ዘ", "forms": ["ዘ", "ዙ", "ዚ", "ዛ", "ዜ", "ዝ", "ዞ"], "phonetic": ["ze", "zu", "zi", "za", "zie", "z", "zo"]},
    "ዠ": {"base": "ዠ", "forms": ["ዠ", "ዡ", "ዢ", "ዣ", "ዤ", "ዥ", "ዦ"], "phonetic": ["Ze", "Zu", "Zi", "Za", "Zie", "Z", "Zo"]},
    "የ": {"base": "የ", "forms": ["የ", "ዩ", "ዪ", "ያ", "ዬ", "ይ", "ዮ"], "phonetic": ["ye", "yu", "yi", "ya", "yie", "y", "yo"]},
    "ደ": {"base": "ደ", "forms": ["ደ", "ዱ", "ዲ", "ዳ", "ዴ", "ድ", "ዶ"], "phonetic": ["de", "du", "di", "da", "die", "d", "do"]},
    "ጀ": {"base": "ጀ", "forms": ["ጀ", "ጁ", "ጂ", "ጃ", "ጄ", "ጅ", "ጆ"], "phonetic": ["je", "ju", "ji", "ja", "jie", "j", "jo"]},
    "ገ": {"base": "ገ", "forms": ["ገ", "ጉ", "ጊ", "ጋ", "ጌ", "ግ", "ጎ"], "phonetic": ["ge", "gu", "gi", "ga", "gie", "g", "go"]},
    "ጠ": {"base": "ጠ", "forms": ["ጠ", "ጡ", "ጢ", "ጣ", "ጤ", "ጥ", "ጦ"], "phonetic": ["Te", "Tu", "Ti", "Ta", "Tie", "T", "To"]},
    "ጨ": {"base": "ጨ", "forms": ["ጨ", "ጩ", "ጪ", "ጫ", "ጬ", "ጭ", "ጮ"], "phonetic": ["Ce", "Cu", "Ci", "Ca", "Cie", "C", "Co"]},
    "ጸ": {"base": "ጸ", "forms": ["ጸ", "ጹ", "ጺ", "ጻ", "ጼ", "ጽ", "ጾ"], "phonetic": ["tse", "tsu", "tsi", "tsa", "tsie", "ts", "tso"]},
    "ፈ": {"base": "ፈ", "forms": ["ፈ", "ፉ", "ፊ", "ፋ", "ፌ", "ፍ", "ፎ"], "phonetic": ["fe", "fu", "fi", "fa", "fie", "f", "fo"]},
    "ፐ": {"base": "ፐ", "forms": ["ፐ", "ፑ", "ፒ", "ፓ", "ፔ", "ፕ", "ፖ"], "phonetic": ["pe", "pu", "pi", "pa", "pie", "p", "po"]}
}

def create_handwriting_animation_html_backup(text, pen_style="Realistic", writing_style="Natural", animation_speed=3.5):
    """Create HTML5 Canvas-based handwriting animation with proper fill rendering"""
    
    import json
    
    # Escape text for JavaScript
    safe_text = json.dumps(text)
    
    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tigrinya Handwriting Animation</title>
            <script src="https://cdn.jsdelivr.net/npm/opentype.js@latest/dist/opentype.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;700&display=swap');
                
                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: 'Noto Sans Ethiopic', 'Ebrima', 'Nyala', sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                
                .container {{
                    max-width: 1000px;
                    width: 100%;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    padding: 30px;
                    margin: 20px;
                }}
                
                h1 {{
                    text-align: center;
                    color: #2c3e50;
                    margin-bottom: 30px;
                    font-size: 2.2em;
                }}
                
                .animation-area {{
                    position: relative;
                    background: #fefefe;
                    border: 2px solid #e1e8ed;
                    border-radius: 10px;
                    margin: 20px 0;
                    min-height: 300px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                
                #animationCanvas {{
                    border-radius: 8px;
                    background: white;
                }}
                
                .controls {{
                    display: flex;
                    justify-content: center;
                    gap: 15px;
                    margin: 20px 0;
                    flex-wrap: wrap;
                }}
                
                .btn {{
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                
                .btn-primary {{
                    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                
                .btn-primary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }}
                
                .btn-secondary {{
                    background: #ecf0f1;
                    color: #34495e;
                }}
                
                .btn-secondary:hover {{
                    background: #d5dbdb;
                }}
                
                .info-panel {{
                    background: #f8f9fa;
                    border-left: 4px solid #667eea;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                }}
                
                .text-display {{
                    font-size: 1.5em;
                    text-align: center;
                    margin: 15px 0;
                    padding: 15px;
                    background: #e8f4fd;
                    border-radius: 8px;
                    border: 1px solid #bee5eb;
                }}
                
                .progress-bar {{
                    width: 100%;
                    height: 6px;
                    background: #ecf0f1;
                    border-radius: 3px;
                    margin: 10px 0;
                    overflow: hidden;
                }}
                
                .progress-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #667eea, #764ba2);
                    border-radius: 3px;
                    width: 0%;
                    transition: width 0.3s ease;
                }}
                
                .status {{
                    text-align: center;
                    margin: 10px 0;
                    font-weight: 500;
                }}

                .scroll-container {{
                    width: 100%;
                    max-width: 900px;   /* visible viewport */
                    overflow-x: auto;   /* enable horizontal scroll */
                    overflow-y: hidden; /* prevent vertical scroll unless needed */
                    border-radius: 8px;
                    border: 2px solid #e1e8ed;
                    background: white;
                }}

            </style>
        </head>
        <body>
            <div class="container">
                <h1>✍️ Tigrinya Handwriting Animation</h1>
                
                <div class="text-display">
                    <strong>Text to animate:</strong> {text}
                </div>
                
                <div class="info-panel">
                    <strong>Animation Settings:</strong><br>
                    Pen Style: {pen_style} | Writing Style: {writing_style} | Speed: {animation_speed}x
                </div>
                
                <div class="animation-area">
                    <div class="scroll-container">
                        <canvas id="animationCanvas" width="1800" height="400"></canvas>
                    </div>
                </div>

                
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                
                <div class="status" id="status">Loading font...</div>
                
                <div class="controls">
                    <button id="startBtn" class="btn btn-primary" onclick="startAnimation()" disabled>Start Animation</button>
                    <button class="btn btn-secondary" onclick="pauseAnimation()">Pause</button>
                    <button class="btn btn-secondary" onclick="resetAnimation()">Reset</button>
                    <button class="btn btn-secondary" onclick="downloadAnimation()">Download Image</button>
                </div>
            </div>

            <script>
                // Animation configuration
                const config = {{
                    text: {safe_text},
                    penStyle: "{pen_style}",
                    writingStyle: "{writing_style}",
                    animationSpeed: {animation_speed},
                    canvas: null,
                    ctx: null,
                    isAnimating: false,
                    isPaused: false,
                    currentCharIndex: 0,
                    currentStroke: 0,
                    frames: [],
                    animationFrame: null,
                    font: null,
                    characterPaths: []
                }};

                // Load font
                opentype.load('https://fonts.gstatic.com/s/notosansethiopic/v49/7cHPv50vjIepfJVOZZgcpQ5B9FBTH9KGNfhSTgtoow1KVnIvyBoMSzUMacb-T35OK6Dj.ttf', function (err, font) {{
                    if (err) {{
                        document.getElementById('status').textContent = 'Error loading font: ' + err;
                    }} else {{
                        config.font = font;
                        document.getElementById('status').textContent = 'Ready to animate';
                        document.getElementById('startBtn').disabled = false;
                    }}
                }});
                
                // Initialize canvas
                function initCanvas() {{
                    config.canvas = document.getElementById('animationCanvas');
                    config.ctx = config.canvas.getContext('2d');
                    config.ctx.imageSmoothingEnabled = true;
                    config.ctx.lineCap = 'round';
                    config.ctx.lineJoin = 'round';
                }}

                // Convert font paths to drawable strokes for handwriting effect
                function generateCharacterStrokes(text) {{
                    const strokes = [];
                    const canvas = config.canvas;
                    
                    const fontSize = 48;
                    const totalWidth = config.font.getAdvanceWidth(text, fontSize);
                    const startX = (canvas.width - totalWidth) / 2;
                    const baseY = canvas.height / 2 + fontSize / 4;
                    
                    let currentX = startX;
                    
                    for (let i = 0; i < text.length; i++) {{
                        const char = text[i];
                        
                        if (char === ' ') {{
                            currentX += config.font.getAdvanceWidth(' ', fontSize);
                            strokes.push({{
                                char: ' ',
                                type: 'space',
                                x: currentX,
                                y: baseY,
                                width: config.font.getAdvanceWidth(' ', fontSize)
                            }});
                            continue;
                        }}
                        
                        const fontPath = config.font.getPath(char, currentX, baseY, fontSize);
                        const charStrokes = convertPathToStrokes(fontPath, currentX, baseY);
                        
                        strokes.push({{
                            char: char,
                            type: 'character',
                            strokes: charStrokes,
                            x: currentX,
                            y: baseY
                        }});
                        
                        currentX += config.font.getAdvanceWidth(char, fontSize);
                    }}
                    
                    return strokes;
                }}

                // Convert OpenType path to handwriting strokes
                function convertPathToStrokes(path, offsetX, offsetY) {{
                    const strokes = [];
                    let currentStroke = [];
                    
                    for (const cmd of path.commands) {{
                        switch (cmd.type) {{
                            case 'M': // Move to
                                if (currentStroke.length > 0) {{
                                    strokes.push(currentStroke);
                                }}
                                currentStroke = [{{x: cmd.x, y: cmd.y}}];
                                break;
                                
                            case 'L': // Line to
                                currentStroke.push({{x: cmd.x, y: cmd.y}});
                                break;
                                
                            case 'Q': // Quadratic curve
                                const p0 = currentStroke[currentStroke.length - 1];
                                for (let t = 0.1; t <= 1; t += 0.1) {{
                                    const x = Math.pow(1-t, 2) * p0.x + 2*(1-t)*t * cmd.x1 + Math.pow(t, 2) * cmd.x;
                                    const y = Math.pow(1-t, 2) * p0.y + 2*(1-t)*t * cmd.y1 + Math.pow(t, 2) * cmd.y;
                                    currentStroke.push({{x, y}});
                                }}
                                break;
                                
                            case 'C': // Cubic curve
                                const p0c = currentStroke[currentStroke.length - 1];
                                for (let t = 0.1; t <= 1; t += 0.1) {{
                                    const x = Math.pow(1-t, 3) * p0c.x + 
                                            3 * Math.pow(1-t, 2) * t * cmd.x1 +
                                            3 * (1-t) * Math.pow(t, 2) * cmd.x2 + 
                                            Math.pow(t, 3) * cmd.x;
                                    const y = Math.pow(1-t, 3) * p0c.y + 
                                            3 * Math.pow(1-t, 2) * t * cmd.y1 +
                                            3 * (1-t) * Math.pow(t, 2) * cmd.y2 + 
                                            Math.pow(t, 3) * cmd.y;
                                    currentStroke.push({{x, y}});
                                }}
                                break;
                                
                            case 'Z': // Close path
                                if (currentStroke.length > 0) {{
                                    strokes.push(currentStroke);
                                    currentStroke = [];
                                }}
                                break;
                        }}
                    }}
                    
                    if (currentStroke.length > 0) {{
                        strokes.push(currentStroke);
                    }}
                    
                    return strokes;
                }}
                
                // Pen drawing functions
                function drawPen(x, y, angle = 0) {{
                    const ctx = config.ctx;
                    ctx.save();
                    ctx.translate(x, y);
                    ctx.rotate(angle);
                    
                    if (config.penStyle === 'Realistic') {{
                        drawRealisticPen(ctx);
                    }} else if (config.penStyle === 'Brush') {{
                        drawBrushPen(ctx);
                    }} else {{
                        drawSimplePen(ctx);
                    }}
                    
                    ctx.restore();
                }}
                
                function drawRealisticPen(ctx) {{
                    // Pen shadow
                    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                    ctx.fillRect(-2, 2, 4, 20);
                    
                    // Pen body
                    ctx.fillStyle = '#4169E1';
                    ctx.fillRect(-2, 0, 4, 18);
                    
                    // Pen grip
                    ctx.fillStyle = '#696969';
                    ctx.fillRect(-2.5, 6, 5, 6);
                    
                    // Pen tip
                    ctx.fillStyle = '#000080';
                    ctx.beginPath();
                    ctx.arc(0, 0, 1.5, 0, Math.PI * 2);
                    ctx.fill();
                }}
                
                function drawBrushPen(ctx) {{
                    // Brush body
                    ctx.fillStyle = '#8B4513';
                    ctx.fillRect(-1.5, 0, 3, 15);
                    
                    // Brush tip
                    ctx.fillStyle = '#D4AF37';
                    ctx.beginPath();
                    ctx.ellipse(0, 0, 3, 1.5, Math.PI/4, 0, Math.PI * 2);
                    ctx.fill();
                }}
                
                function drawSimplePen(ctx) {{
                    // Simple pen
                    ctx.strokeStyle = '#333';
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.moveTo(0, 0);
                    ctx.lineTo(0, 15);
                    ctx.stroke();
                    
                    ctx.fillStyle = '#333';
                    ctx.beginPath();
                    ctx.arc(0, 0, 2, 0, Math.PI * 2);
                    ctx.fill();
                }}
                
                // Main animation functions
                function startAnimation() {{
                    if (config.isAnimating && !config.isPaused) return;
                    
                    if (!config.isAnimating) {{
                        resetAnimation();
                        config.isAnimating = true;
                        config.characterPaths = generateCharacterStrokes(config.text);
                        console.log('Generated character paths:', config.characterPaths);
                    }}
                    
                    config.isPaused = false;
                    document.getElementById('status').textContent = 'Animating...';
                    animateNextFrame();
                }}
                
                function pauseAnimation() {{
                    config.isPaused = true;
                    if (config.animationFrame) {{
                        cancelAnimationFrame(config.animationFrame);
                    }}
                    document.getElementById('status').textContent = 'Paused';
                }}

                function animateNextFrame() {{
                    if (config.isPaused || !config.isAnimating) return;
                    
                    const paths = config.characterPaths;
                    if (!paths || config.currentCharIndex >= paths.length) {{
                        // Animation complete
                        config.isAnimating = false;
                        document.getElementById('status').textContent = 'Animation complete!';
                        document.getElementById('progressFill').style.width = '100%';
                        return;
                    }}
                    
                    const currentPath = paths[config.currentCharIndex];
                    
                    // Update progress
                    const progress = (config.currentCharIndex / paths.length) * 100;
                    document.getElementById('progressFill').style.width = progress + '%';
                    
                    if (currentPath.type === 'space') {{
                        // Handle space - just move to next character
                        setTimeout(() => {{
                            config.currentCharIndex++;
                            config.currentStroke = 0;
                            config.animationFrame = requestAnimationFrame(animateNextFrame);
                        }}, 300 / config.animationSpeed);
                        return;
                    }}
                    
                    if (config.currentStroke >= currentPath.strokes.length) {{
                        // Move to next character
                        config.currentCharIndex++;
                        config.currentStroke = 0;
                        config.animationFrame = requestAnimationFrame(animateNextFrame);
                        return;
                    }}
                    
                    // Animate current stroke
                    const stroke = currentPath.strokes[config.currentStroke];
                    animateStroke(stroke, () => {{
                        config.currentStroke++;
                        setTimeout(() => {{
                            config.animationFrame = requestAnimationFrame(animateNextFrame);
                        }}, 100 / config.animationSpeed);
                    }});
                }}

                // Animate individual stroke with handwriting effect
                function animateStroke(stroke, callback) {{
                    if (!stroke || stroke.length === 0) {{
                        callback();
                        return;
                    }}
                    
                    let pointIndex = 0;
                    const ctx = config.ctx;
                    
                    function drawNextSegment() {{
                        if (pointIndex >= stroke.length) {{
                            callback();
                            return;
                        }}
                        
                        // Clear and redraw everything
                        redrawCanvas();
                        
                        if (pointIndex === 0) {{
                            // Just show pen at starting position
                            drawPen(stroke[0].x, stroke[0].y - 25);
                        }} else {{
                            // Draw stroke segments up to current point
                            ctx.strokeStyle = '#2c3e50';
                            ctx.lineWidth = 3;
                            ctx.lineCap = 'round';
                            ctx.lineJoin = 'round';
                            
                            ctx.beginPath();
                            ctx.moveTo(stroke[0].x, stroke[0].y);
                            
                            for (let i = 1; i <= pointIndex; i++) {{
                                ctx.lineTo(stroke[i].x, stroke[i].y);
                            }}
                            ctx.stroke();
                            
                            // Show pen at current position
                            const currentPoint = stroke[pointIndex];
                            drawPen(currentPoint.x, currentPoint.y - 25);
                        }}
                        
                        pointIndex++;
                        
                        // Continue to next segment
                        setTimeout(drawNextSegment, 50 / config.animationSpeed);
                    }}
                    
                    drawNextSegment();
                }}

                // Redraw the entire canvas with completed characters and strokes
                function redrawCanvas() {{
                    const ctx = config.ctx;
                    
                    // Clear canvas
                    ctx.clearRect(0, 0, config.canvas.width, config.canvas.height);
                    
                    // Draw background
                    ctx.fillStyle = '#fefefe';
                    ctx.fillRect(0, 0, config.canvas.width, config.canvas.height);
                    
                    // Draw all completed characters
                    for (let charIndex = 0; charIndex < config.currentCharIndex; charIndex++) {{
                        const path = config.characterPaths[charIndex];
                        if (path.type === 'character') {{
                            drawCompletedCharacter(path);
                        }}
                    }}
                    
                    // Draw completed strokes of current character
                    if (config.currentCharIndex < config.characterPaths.length && 
                        config.characterPaths[config.currentCharIndex].type === 'character') {{
                        const currentPath = config.characterPaths[config.currentCharIndex];
                        
                        ctx.strokeStyle = '#2c3e50';
                        ctx.lineWidth = 3;
                        ctx.lineCap = 'round';
                        ctx.lineJoin = 'round';
                        
                        for (let strokeIndex = 0; strokeIndex < config.currentStroke; strokeIndex++) {{
                            const stroke = currentPath.strokes[strokeIndex];
                            if (stroke && stroke.length > 0) {{
                                ctx.beginPath();
                                ctx.moveTo(stroke[0].x, stroke[0].y);
                                for (let i = 1; i < stroke.length; i++) {{
                                    ctx.lineTo(stroke[i].x, stroke[i].y);
                                }}
                                ctx.stroke();
                            }}
                        }}
                    }}
                }}

                // Draw a completed character
                function drawCompletedCharacter(path) {{
                    const ctx = config.ctx;
                    
                    ctx.strokeStyle = '#2c3e50';
                    ctx.lineWidth = 3;
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';
                    
                    for (const stroke of path.strokes) {{
                        if (stroke && stroke.length > 0) {{
                            ctx.beginPath();
                            ctx.moveTo(stroke[0].x, stroke[0].y);
                            for (let i = 1; i < stroke.length; i++) {{
                                ctx.lineTo(stroke[i].x, stroke[i].y);
                            }}
                            ctx.stroke();
                        }}
                    }}
                }}

                // Reset animation
                function resetAnimation() {{
                    config.isAnimating = false;
                    config.isPaused = false;
                    config.currentCharIndex = 0;
                    config.currentStroke = 0;
                    config.frames = [];
                    
                    if (config.animationFrame) {{
                        cancelAnimationFrame(config.animationFrame);
                    }}
                    
                    // Clear canvas
                    const ctx = config.ctx;
                    ctx.clearRect(0, 0, config.canvas.width, config.canvas.height);
                    
                    // Draw background
                    ctx.fillStyle = '#fefefe';
                    ctx.fillRect(0, 0, config.canvas.width, config.canvas.height);
                    
                    document.getElementById('status').textContent = 'Ready to animate';
                    document.getElementById('progressFill').style.width = '0%';
                }}
                
                function downloadAnimation() {{
                    if (!config.canvas) {{
                        alert('No animation canvas found.');
                        return;
                    }}
                    
                    // Convert canvas to data URL and trigger download
                    const link = document.createElement('a');
                    link.download = 'tigrinya_handwriting_animation.png';
                    link.href = config.canvas.toDataURL();
                    link.click();
                }}
                
                // Initialize when page loads
                window.onload = function() {{
                    initCanvas();
                    resetAnimation();
                }};
            </script>
        </body>
        </html>
            """
    return html_content


def create_handwriting_animation_html(text, pen_style="Realistic", writing_style="Natural", animation_speed=3.5):
    """Create HTML5 Canvas-based handwriting animation with scrollable canvas"""
    
    import json
    
    # Escape text for JavaScript
    safe_text = json.dumps(text)
    
    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tigrinya Handwriting Animation</title>
            <script src="https://cdn.jsdelivr.net/npm/opentype.js@latest/dist/opentype.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;700&display=swap');
                
                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: 'Noto Sans Ethiopic', 'Ebrima', 'Nyala', sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                
                .container {{
                    max-width: 1000px;
                    width: 100%;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    padding: 30px;
                    margin: 20px;
                }}
                
                h1 {{
                    text-align: center;
                    color: #2c3e50;
                    margin-bottom: 30px;
                    font-size: 2.2em;
                }}
                
                .animation-area {{
                    position: relative;
                    background: #fefefe;
                    border: 2px solid #e1e8ed;
                    border-radius: 10px;
                    margin: 20px 0;
                    min-height: 300px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 10px;
                }}
                
                .scroll-container {{
                    width: 100%;
                    max-width: 900px;
                    max-height: 400px;
                    overflow: auto;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                    background: white;
                    position: relative;
                }}
                
                #animationCanvas {{
                    display: block;
                    background: white;
                    border-radius: 4px;
                }}
                
                .controls {{
                    display: flex;
                    justify-content: center;
                    gap: 15px;
                    margin: 20px 0;
                    flex-wrap: wrap;
                }}
                
                .btn {{
                    padding: 12px 24px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-size: 16px;
                    font-weight: 600;
                    transition: all 0.3s ease;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                
                .btn-primary {{
                    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                
                .btn-primary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
                }}
                
                .btn-secondary {{
                    background: #ecf0f1;
                    color: #34495e;
                }}
                
                .btn-secondary:hover {{
                    background: #d5dbdb;
                }}
                
                .info-panel {{
                    background: #f8f9fa;
                    border-left: 4px solid #667eea;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                }}
                
                .text-display {{
                    font-size: 1.5em;
                    text-align: center;
                    margin: 15px 0;
                    padding: 15px;
                    background: #e8f4fd;
                    border-radius: 8px;
                    border: 1px solid #bee5eb;
                }}
                
                .progress-bar {{
                    width: 100%;
                    height: 6px;
                    background: #ecf0f1;
                    border-radius: 3px;
                    margin: 10px 0;
                    overflow: hidden;
                }}
                
                .progress-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #667eea, #764ba2);
                    border-radius: 3px;
                    width: 0%;
                    transition: width 0.3s ease;
                }}
                
                .status {{
                    text-align: center;
                    margin: 10px 0;
                    font-weight: 500;
                }}

                .scroll-info {{
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                    margin: 10px 0;
                    font-style: italic;
                }}

                /* Custom scrollbar styling */
                .scroll-container::-webkit-scrollbar {{
                    width: 8px;
                    height: 8px;
                }}

                .scroll-container::-webkit-scrollbar-track {{
                    background: #f1f1f1;
                    border-radius: 4px;
                }}

                .scroll-container::-webkit-scrollbar-thumb {{
                    background: #667eea;
                    border-radius: 4px;
                }}

                .scroll-container::-webkit-scrollbar-thumb:hover {{
                    background: #5a67d8;
                }}

            </style>
        </head>
        <body>
            <div class="container">
                <h1>✍️ Tigrinya Handwriting Animation</h1>
                
                <div class="text-display">
                    <strong>Text to animate:</strong> {text}
                </div>
                
                <div class="info-panel">
                    <strong>Animation Settings:</strong><br>
                    Pen Style: {pen_style} | Writing Style: {writing_style} | Speed: {animation_speed}x
                </div>
                
                <div class="scroll-info">
                    💡 The canvas will automatically scroll to follow the pen as it writes
                </div>
                
                <div class="animation-area">
                    <div class="scroll-container" id="scrollContainer">
                        <canvas id="animationCanvas"></canvas>
                    </div>
                </div>

                
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                
                <div class="status" id="status">Loading font...</div>
                
                <div class="controls">
                    <button id="startBtn" class="btn btn-primary" onclick="startAnimation()" disabled>Start Animation</button>
                    <button class="btn btn-secondary" onclick="pauseAnimation()">Pause</button>
                    <button class="btn btn-secondary" onclick="resetAnimation()">Reset</button>
                    <button class="btn btn-secondary" onclick="downloadAnimation()">Download Image</button>
                </div>
            </div>

            <script>
                // Animation configuration
                const config = {{
                    text: {safe_text},
                    penStyle: "{pen_style}",
                    writingStyle: "{writing_style}",
                    animationSpeed: {animation_speed},
                    canvas: null,
                    ctx: null,
                    isAnimating: false,
                    isPaused: false,
                    currentCharIndex: 0,
                    currentStroke: 0,
                    frames: [],
                    animationFrame: null,
                    font: null,
                    characterPaths: [],
                    scrollContainer: null,
                    canvasWidth: 2400, // Wider canvas for longer text
                    canvasHeight: 400
                }};

                // Load font
                opentype.load('https://fonts.gstatic.com/s/notosansethiopic/v49/7cHPv50vjIepfJVOZZgcpQ5B9FBTH9KGNfhSTgtoow1KVnIvyBoMSzUMacb-T35OK6Dj.ttf', function (err, font) {{
                    if (err) {{
                        document.getElementById('status').textContent = 'Error loading font: ' + err;
                    }} else {{
                        config.font = font;
                        document.getElementById('status').textContent = 'Ready to animate';
                        document.getElementById('startBtn').disabled = false;
                        initCanvas();
                    }}
                }});
                
                // Initialize canvas with proper dimensions
                function initCanvas() {{
                    config.canvas = document.getElementById('animationCanvas');
                    config.scrollContainer = document.getElementById('scrollContainer');
                    
                    // Set canvas size based on text length
                    const textLength = config.text.length;
                    const estimatedWidth = Math.max(2400, textLength * 60); // Estimate width based on text length
                    
                    config.canvasWidth = estimatedWidth;
                    config.canvas.width = config.canvasWidth;
                    config.canvas.height = config.canvasHeight;
                    
                    config.ctx = config.canvas.getContext('2d');
                    config.ctx.imageSmoothingEnabled = true;
                    config.ctx.lineCap = 'round';
                    config.ctx.lineJoin = 'round';
                    
                    // Reset scroll to beginning
                    config.scrollContainer.scrollLeft = 0;
                }}

                // Auto-scroll to follow the pen
                function scrollToPosition(x) {{
                    if (!config.scrollContainer) return;
                    
                    const containerWidth = config.scrollContainer.clientWidth;
                    const scrollLeft = config.scrollContainer.scrollLeft;
                    const scrollRight = scrollLeft + containerWidth;
                    
                    // Keep pen in view with some padding
                    const padding = 100;
                    
                    if (x < scrollLeft + padding) {{
                        // Scroll left
                        config.scrollContainer.scrollLeft = Math.max(0, x - padding);
                    }} else if (x > scrollRight - padding) {{
                        // Scroll right
                        config.scrollContainer.scrollLeft = x - containerWidth + padding;
                    }}
                }}

                // Convert font paths to drawable strokes for handwriting effect
                function generateCharacterStrokes(text) {{
                    const strokes = [];
                    
                    const fontSize = 48;
                    const totalWidth = config.font.getAdvanceWidth(text, fontSize);
                    const padding = 100; // Padding from edges
                    const startX = padding; // Start from left with padding
                    const baseY = config.canvasHeight / 2 + fontSize / 4;
                    
                    let currentX = startX;
                    
                    for (let i = 0; i < text.length; i++) {{
                        const char = text[i];
                        
                        if (char === ' ') {{
                            const spaceWidth = config.font.getAdvanceWidth(' ', fontSize);
                            currentX += spaceWidth;
                            strokes.push({{
                                char: ' ',
                                type: 'space',
                                x: currentX,
                                y: baseY,
                                width: spaceWidth
                            }});
                            continue;
                        }}
                        
                        const fontPath = config.font.getPath(char, currentX, baseY, fontSize);
                        const charStrokes = convertPathToStrokes(fontPath, currentX, baseY);
                        
                        strokes.push({{
                            char: char,
                            type: 'character',
                            strokes: charStrokes,
                            x: currentX,
                            y: baseY
                        }});
                        
                        currentX += config.font.getAdvanceWidth(char, fontSize);
                    }}
                    
                    return strokes;
                }}

                // Convert OpenType path to handwriting strokes
                function convertPathToStrokes(path, offsetX, offsetY) {{
                    const strokes = [];
                    let currentStroke = [];
                    
                    for (const cmd of path.commands) {{
                        switch (cmd.type) {{
                            case 'M': // Move to
                                if (currentStroke.length > 0) {{
                                    strokes.push(currentStroke);
                                }}
                                currentStroke = [{{x: cmd.x, y: cmd.y}}];
                                break;
                                
                            case 'L': // Line to
                                currentStroke.push({{x: cmd.x, y: cmd.y}});
                                break;
                                
                            case 'Q': // Quadratic curve
                                const p0 = currentStroke[currentStroke.length - 1];
                                for (let t = 0.1; t <= 1; t += 0.1) {{
                                    const x = Math.pow(1-t, 2) * p0.x + 2*(1-t)*t * cmd.x1 + Math.pow(t, 2) * cmd.x;
                                    const y = Math.pow(1-t, 2) * p0.y + 2*(1-t)*t * cmd.y1 + Math.pow(t, 2) * cmd.y;
                                    currentStroke.push({{x, y}});
                                }}
                                break;
                                
                            case 'C': // Cubic curve
                                const p0c = currentStroke[currentStroke.length - 1];
                                for (let t = 0.1; t <= 1; t += 0.1) {{
                                    const x = Math.pow(1-t, 3) * p0c.x + 
                                            3 * Math.pow(1-t, 2) * t * cmd.x1 +
                                            3 * (1-t) * Math.pow(t, 2) * cmd.x2 + 
                                            Math.pow(t, 3) * cmd.x;
                                    const y = Math.pow(1-t, 3) * p0c.y + 
                                            3 * Math.pow(1-t, 2) * t * cmd.y1 +
                                            3 * (1-t) * Math.pow(t, 2) * cmd.y2 + 
                                            Math.pow(t, 3) * cmd.y;
                                    currentStroke.push({{x, y}});
                                }}
                                break;
                                
                            case 'Z': // Close path
                                if (currentStroke.length > 0) {{
                                    strokes.push(currentStroke);
                                    currentStroke = [];
                                }}
                                break;
                        }}
                    }}
                    
                    if (currentStroke.length > 0) {{
                        strokes.push(currentStroke);
                    }}
                    
                    return strokes;
                }}
                
                // Pen drawing functions
                function drawPen(x, y, angle = 0) {{
                    const ctx = config.ctx;
                    ctx.save();
                    ctx.translate(x, y);
                    ctx.rotate(angle);
                    
                    if (config.penStyle === 'Realistic') {{
                        drawRealisticPen(ctx);
                    }} else if (config.penStyle === 'Brush') {{
                        drawBrushPen(ctx);
                    }} else {{
                        drawSimplePen(ctx);
                    }}
                    
                    ctx.restore();
                }}
                
                function drawRealisticPen(ctx) {{
                    // Pen shadow
                    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                    ctx.fillRect(-2, 2, 4, 20);
                    
                    // Pen body
                    ctx.fillStyle = '#4169E1';
                    ctx.fillRect(-2, 0, 4, 18);
                    
                    // Pen grip
                    ctx.fillStyle = '#696969';
                    ctx.fillRect(-2.5, 6, 5, 6);
                    
                    // Pen tip
                    ctx.fillStyle = '#000080';
                    ctx.beginPath();
                    ctx.arc(0, 0, 1.5, 0, Math.PI * 2);
                    ctx.fill();
                }}
                
                function drawBrushPen(ctx) {{
                    // Brush body
                    ctx.fillStyle = '#8B4513';
                    ctx.fillRect(-1.5, 0, 3, 15);
                    
                    // Brush tip
                    ctx.fillStyle = '#D4AF37';
                    ctx.beginPath();
                    ctx.ellipse(0, 0, 3, 1.5, Math.PI/4, 0, Math.PI * 2);
                    ctx.fill();
                }}
                
                function drawSimplePen(ctx) {{
                    // Simple pen
                    ctx.strokeStyle = '#333';
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.moveTo(0, 0);
                    ctx.lineTo(0, 15);
                    ctx.stroke();
                    
                    ctx.fillStyle = '#333';
                    ctx.beginPath();
                    ctx.arc(0, 0, 2, 0, Math.PI * 2);
                    ctx.fill();
                }}
                
                // Main animation functions
                function startAnimation() {{
                    if (config.isAnimating && !config.isPaused) return;
                    
                    if (!config.isAnimating) {{
                        resetAnimation();
                        config.isAnimating = true;
                        config.characterPaths = generateCharacterStrokes(config.text);
                        console.log('Generated character paths:', config.characterPaths);
                    }}
                    
                    config.isPaused = false;
                    document.getElementById('status').textContent = 'Animating...';
                    animateNextFrame();
                }}
                
                function pauseAnimation() {{
                    config.isPaused = true;
                    if (config.animationFrame) {{
                        cancelAnimationFrame(config.animationFrame);
                    }}
                    document.getElementById('status').textContent = 'Paused';
                }}

                function animateNextFrame() {{
                    if (config.isPaused || !config.isAnimating) return;
                    
                    const paths = config.characterPaths;
                    if (!paths || config.currentCharIndex >= paths.length) {{
                        // Animation complete
                        config.isAnimating = false;
                        document.getElementById('status').textContent = 'Animation complete!';
                        document.getElementById('progressFill').style.width = '100%';
                        return;
                    }}
                    
                    const currentPath = paths[config.currentCharIndex];
                    
                    // Update progress
                    const progress = (config.currentCharIndex / paths.length) * 100;
                    document.getElementById('progressFill').style.width = progress + '%';
                    
                    if (currentPath.type === 'space') {{
                        // Handle space - just move to next character and scroll to position
                        scrollToPosition(currentPath.x);
                        setTimeout(() => {{
                            config.currentCharIndex++;
                            config.currentStroke = 0;
                            config.animationFrame = requestAnimationFrame(animateNextFrame);
                        }}, 300 / config.animationSpeed);
                        return;
                    }}
                    
                    if (config.currentStroke >= currentPath.strokes.length) {{
                        // Move to next character
                        config.currentCharIndex++;
                        config.currentStroke = 0;
                        config.animationFrame = requestAnimationFrame(animateNextFrame);
                        return;
                    }}
                    
                    // Animate current stroke
                    const stroke = currentPath.strokes[config.currentStroke];
                    animateStroke(stroke, () => {{
                        config.currentStroke++;
                        setTimeout(() => {{
                            config.animationFrame = requestAnimationFrame(animateNextFrame);
                        }}, 100 / config.animationSpeed);
                    }});
                }}

                // Animate individual stroke with handwriting effect
                function animateStroke(stroke, callback) {{
                    if (!stroke || stroke.length === 0) {{
                        callback();
                        return;
                    }}
                    
                    let pointIndex = 0;
                    const ctx = config.ctx;
                    
                    function drawNextSegment() {{
                        if (pointIndex >= stroke.length) {{
                            callback();
                            return;
                        }}
                        
                        // Clear and redraw everything
                        redrawCanvas();
                        
                        if (pointIndex === 0) {{
                            // Just show pen at starting position
                            const penX = stroke[0].x;
                            const penY = stroke[0].y - 25;
                            drawPen(penX, penY);
                            scrollToPosition(penX);
                        }} else {{
                            // Draw stroke segments up to current point
                            ctx.strokeStyle = '#2c3e50';
                            ctx.lineWidth = 3;
                            ctx.lineCap = 'round';
                            ctx.lineJoin = 'round';
                            
                            ctx.beginPath();
                            ctx.moveTo(stroke[0].x, stroke[0].y);
                            
                            for (let i = 1; i <= pointIndex; i++) {{
                                ctx.lineTo(stroke[i].x, stroke[i].y);
                            }}
                            ctx.stroke();
                            
                            // Show pen at current position
                            const currentPoint = stroke[pointIndex];
                            const penX = currentPoint.x;
                            const penY = currentPoint.y - 25;
                            drawPen(penX, penY);
                            scrollToPosition(penX);
                        }}
                        
                        pointIndex++;
                        
                        // Continue to next segment
                        setTimeout(drawNextSegment, 50 / config.animationSpeed);
                    }}
                    
                    drawNextSegment();
                }}

                // Redraw the entire canvas with completed characters and strokes
                function redrawCanvas() {{
                    const ctx = config.ctx;
                    
                    // Clear canvas
                    ctx.clearRect(0, 0, config.canvas.width, config.canvas.height);
                    
                    // Draw background
                    ctx.fillStyle = '#fefefe';
                    ctx.fillRect(0, 0, config.canvas.width, config.canvas.height);
                    
                    // Draw all completed characters
                    for (let charIndex = 0; charIndex < config.currentCharIndex; charIndex++) {{
                        const path = config.characterPaths[charIndex];
                        if (path.type === 'character') {{
                            drawCompletedCharacter(path);
                        }}
                    }}
                    
                    // Draw completed strokes of current character
                    if (config.currentCharIndex < config.characterPaths.length && 
                        config.characterPaths[config.currentCharIndex].type === 'character') {{
                        const currentPath = config.characterPaths[config.currentCharIndex];
                        
                        ctx.strokeStyle = '#2c3e50';
                        ctx.lineWidth = 3;
                        ctx.lineCap = 'round';
                        ctx.lineJoin = 'round';
                        
                        for (let strokeIndex = 0; strokeIndex < config.currentStroke; strokeIndex++) {{
                            const stroke = currentPath.strokes[strokeIndex];
                            if (stroke && stroke.length > 0) {{
                                ctx.beginPath();
                                ctx.moveTo(stroke[0].x, stroke[0].y);
                                for (let i = 1; i < stroke.length; i++) {{
                                    ctx.lineTo(stroke[i].x, stroke[i].y);
                                }}
                                ctx.stroke();
                            }}
                        }}
                    }}
                }}

                // Draw a completed character
                function drawCompletedCharacter(path) {{
                    const ctx = config.ctx;
                    
                    ctx.strokeStyle = '#2c3e50';
                    ctx.lineWidth = 3;
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';
                    
                    for (const stroke of path.strokes) {{
                        if (stroke && stroke.length > 0) {{
                            ctx.beginPath();
                            ctx.moveTo(stroke[0].x, stroke[0].y);
                            for (let i = 1; i < stroke.length; i++) {{
                                ctx.lineTo(stroke[i].x, stroke[i].y);
                            }}
                            ctx.stroke();
                        }}
                    }}
                }}

                // Reset animation
                function resetAnimation() {{
                    config.isAnimating = false;
                    config.isPaused = false;
                    config.currentCharIndex = 0;
                    config.currentStroke = 0;
                    config.frames = [];
                    
                    if (config.animationFrame) {{
                        cancelAnimationFrame(config.animationFrame);
                    }}
                    
                    // Clear canvas
                    if (config.ctx) {{
                        const ctx = config.ctx;
                        ctx.clearRect(0, 0, config.canvas.width, config.canvas.height);
                        
                        // Draw background
                        ctx.fillStyle = '#fefefe';
                        ctx.fillRect(0, 0, config.canvas.width, config.canvas.height);
                    }}
                    
                    // Reset scroll position
                    if (config.scrollContainer) {{
                        config.scrollContainer.scrollLeft = 0;
                    }}
                    
                    document.getElementById('status').textContent = 'Ready to animate';
                    document.getElementById('progressFill').style.width = '0%';
                }}
                
                function downloadAnimation() {{
                    if (!config.canvas) {{
                        alert('No animation canvas found.');
                        return;
                    }}
                    
                    // Convert canvas to data URL and trigger download
                    const link = document.createElement('a');
                    link.download = 'tigrinya_handwriting_animation.png';
                    link.href = config.canvas.toDataURL();
                    link.click();
                }}
                
                // Initialize when page loads
                window.onload = function() {{
                    // Initialization will happen after font loads
                }};
            </script>
        </body>
        </html>
            """
    return html_content

class ImageLoader:
    """Handles image loading from various sources with caching"""
    
    def __init__(self, images_folder: str = "images"):
        self.images_folder = images_folder
    
    @st.cache_data
    def get_local_image(_self, word: str) -> Optional[bytes]:
        """Load image from local folder with caching"""
        if not os.path.exists(_self.images_folder):
            return None
        
        extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
        
        for ext in extensions:
            for case_word in [word, word.lower(), word.upper(), word.title()]:
                image_path = os.path.join(_self.images_folder, f"{case_word}{ext}")
                if os.path.exists(image_path):
                    try:
                        with open(image_path, "rb") as f:
                            return f.read()
                    except Exception as e:
                        st.error(f"Error loading {image_path}: {e}")
        
        return None
    
    @st.cache_data
    def get_unsplash_image(_self, query: str, width: int = 400, height: int = 300) -> Optional[bytes]:
        """Fetch image from Unsplash with error handling"""
        try:
            url = f"https://source.unsplash.com/{width}x{height}/?{query}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.content
        except Exception as e:
            st.warning(f"Could not load online image for '{query}': {str(e)}")
        return None
    
    def get_image(self, word: str) -> Optional[bytes]:
        """Get image with fallback priority: local -> unsplash -> placeholder"""
        # Try local first
        image = self.get_local_image(word)
        if image:
            return image
        
        # Try Unsplash
        image = self.get_unsplash_image(word)
        if image:
            return image
        
        return None

class QuizManager:
    """Manages quiz state and scoring"""
    
    def __init__(self):
        if 'quiz_state' not in st.session_state:
            self.reset_quiz()
    
    def reset_quiz(self):
        """Reset quiz statistics"""
        st.session_state.quiz_state = {
            'score': 0,
            'total': 0,
            'streak': 0,
            'best_streak': 0,
            'current_question': None,
            'answered': False
        }
    
    def generate_question(self, category: str = "all") -> Dict:
        """Generate a new quiz question"""
        if category == "all":
            word = random.choice(list(VOCAB_DICT.keys()))
        else:
            if category in VOCAB_CATEGORIES:
                word = random.choice(list(VOCAB_CATEGORIES[category].keys()))
            else:
                word = random.choice(list(VOCAB_DICT.keys()))
        
        correct_answer = VOCAB_DICT[word]
        
        # Generate wrong answers from same category when possible
        wrong_pool = list(VOCAB_DICT.values())
        wrong_answers = [ans for ans in wrong_pool if ans != correct_answer]
        wrong_answers = random.sample(wrong_answers, min(3, len(wrong_answers)))
        
        options = [correct_answer] + wrong_answers
        random.shuffle(options)
        
        question = {
            'word': word,
            'correct_answer': correct_answer,
            'options': options,
            'phonetic': geez_to_latin_syllable(correct_answer)
        }
        
        st.session_state.quiz_state['current_question'] = question
        st.session_state.quiz_state['answered'] = False
        return question
    
    def submit_answer(self, user_answer: str) -> bool:
        """Submit quiz answer and update statistics"""
        if st.session_state.quiz_state['answered']:
            return False
        
        question = st.session_state.quiz_state['current_question']
        is_correct = user_answer == question['correct_answer']
        
        st.session_state.quiz_state['total'] += 1
        st.session_state.quiz_state['answered'] = True
        
        if is_correct:
            st.session_state.quiz_state['score'] += 1
            st.session_state.quiz_state['streak'] += 1
            if st.session_state.quiz_state['streak'] > st.session_state.quiz_state['best_streak']:
                st.session_state.quiz_state['best_streak'] = st.session_state.quiz_state['streak']
        else:
            st.session_state.quiz_state['streak'] = 0
        
        return is_correct

def create_word_card(word: str, translation: str, phonetic: str, show_image: bool = True):
    """Create a styled word card"""
    col1, col2 = st.columns([2, 3] if show_image else [1, 1])
    
    with col1:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px; 
            border-radius: 15px; 
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            color: white;
            text-align: center;
        '>
            <h2 style='margin: 0; font-size: 1.5em;'>{word.title()}</h2>
            <h1 style='margin: 15px 0; font-size: 3.5em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{translation}</h1>
            <h3 style='margin: 0; opacity: 0.9;'>({phonetic})</h3>
        </div>
        """, unsafe_allow_html=True)
    
    if show_image:
        with col2:
            image_loader = ImageLoader()
            image = image_loader.get_image(word)
            if image:
                st.image(image, use_container_width=True)
                st.markdown(f"""
                <div style='
                    text-align: center; 
                    font-size: 1.4em; 
                    font-weight: bold;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 15px; 
                    border-radius: 10px; 
                    margin-top: 10px;
                    box-shadow: 0 3px 10px rgba(0,0,0,0.2);
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                '>
                    {word.title()} - {translation} - ({phonetic})
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"No image available for '{word}'")

def search_page():
    """Search and translation page"""
    st.subheader("Search for a word")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Input methods
        input_method = st.radio(
            "Input method:", 
            ["Type word", "Select from dropdown"],
            help="Choose how you want to input the word"
        )
        
        search_word = ""
        if input_method == "Type word":
            search_word = st.text_input(
                "Enter English word:",
                placeholder="e.g., house, cat, red...",
                help="Type any English word to translate"
            ).lower().strip()
        else:
            search_word = st.selectbox(
                "Select English word:",
                options=[""] + sorted(VOCAB_DICT.keys()),
                help="Choose from available vocabulary"
            )
    
    with col2:
        if search_word:
            st.subheader("Translation Result")
            
            if search_word in VOCAB_DICT:
                translation = VOCAB_DICT[search_word]
                phonetic = geez_to_latin_syllable(translation)
                st.success("Found in vocabulary!")
                
                # Find category
                category = "Unknown"
                for cat, words in VOCAB_CATEGORIES.items():
                    if search_word in words:
                        category = cat.title()
                        break
                
                st.info(f"Category: {category}")
                
            else:
                with st.spinner(f"Translating '{search_word}' using Google Translate..."):
                    try:
                        translator = GoogleTranslator(source='auto', target='ti')
                        translation = translator.translate(search_word)
                        
                        if translation and translation.lower() != search_word.lower():
                            phonetic = geez_to_latin_syllable(translation)
                            st.success("Online translation successful!")
                            st.warning("Not in local vocabulary - accuracy may vary")
                        else:
                            st.error(f"Could not translate '{search_word}'")
                            return
                    except Exception as e:
                        st.error(f"Translation error: {str(e)}")
                        return
    
    # Display word card if translation exists
    if search_word and 'translation' in locals():
        st.markdown("---")
        create_word_card(search_word, translation, phonetic)

def browse_page():
    """Browse all vocabulary page"""
    st.subheader("Complete Vocabulary Browser")
    
    # Category filter
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox(
            "Filter by category:",
            ["All"] + [cat.title() for cat in VOCAB_CATEGORIES.keys()]
        )
    
    with col2:
        sort_by = st.selectbox("Sort by:", ["Alphabetical", "Category", "Length"])
    
    with col3:
        view_mode = st.selectbox("View mode:", ["Cards", "Table", "List"])
    
    # Get words to display
    if category_filter == "All":
        words_to_show = VOCAB_DICT
    else:
        words_to_show = VOCAB_CATEGORIES[category_filter.lower()]
    
    # Sort words
    if sort_by == "Alphabetical":
        sorted_words = sorted(words_to_show.items())
    elif sort_by == "Length":
        sorted_words = sorted(words_to_show.items(), key=lambda x: len(x[0]))
    else:  # Category
        sorted_words = list(words_to_show.items())
    
    st.write(f"Showing {len(sorted_words)} words")
    
    if view_mode == "Cards":
        # Display as cards (2 columns)
        for i in range(0, len(sorted_words), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                word, translation = sorted_words[i]
                phonetic = geez_to_latin_syllable(translation)
                create_word_card(word, translation, phonetic, show_image=False)
            
            if i + 1 < len(sorted_words):
                with col2:
                    word, translation = sorted_words[i + 1]
                    phonetic = geez_to_latin_syllable(translation)
                    create_word_card(word, translation, phonetic, show_image=False)
    
    elif view_mode == "Table":
        # Display as table
        import pandas as pd
        
        df_data = []
        for word, translation in sorted_words:
            phonetic = geez_to_latin_syllable(translation)
            # Find category
            category = "Unknown"
            for cat, words in VOCAB_CATEGORIES.items():
                if word in words:
                    category = cat.title()
                    break
            
            df_data.append({
                "English": word.title(),
                "Tigrinya": translation,
                "Phonetic": phonetic,
                "Category": category
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
    
    else:  # List view
        for word, translation in sorted_words:
            phonetic = geez_to_latin_syllable(translation)
            st.markdown(f"**{word.title()}** → {translation} *({phonetic})*")

def quiz_page():
    """Interactive quiz page"""
    st.subheader("Vocabulary Quiz")
    
    quiz = QuizManager()
    
    # Quiz controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("New Question", type="primary"):
            quiz.generate_question()
    
    with col2:
        quiz_category = st.selectbox(
            "Quiz category:",
            ["all"] + list(VOCAB_CATEGORIES.keys())
        )
    
    with col3:
        if st.button("Reset Stats", help="Reset all quiz statistics"):
            quiz.reset_quiz()
            st.rerun()
    
    # Display current statistics
    stats = st.session_state.quiz_state
    if stats['total'] > 0:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Score", f"{stats['score']}/{stats['total']}")
        with col2:
            accuracy = (stats['score'] / stats['total']) * 100
            st.metric("Accuracy", f"{accuracy:.1f}%")
        with col3:
            st.metric("Current Streak", stats['streak'])
        with col4:
            st.metric("Best Streak", stats['best_streak'])
    
    # Quiz question
    if stats['current_question']:
        question = stats['current_question']
        
        st.markdown("---")
        st.markdown(f"### What is the Tigrinya translation for: **{question['word'].title()}**?")
        
        # Multiple choice options
        user_answer = st.radio(
            "Choose the correct translation:",
            question['options'],
            disabled=stats['answered'],
            key=f"quiz_answer_{stats['total']}"
        )
        
        if not stats['answered']:
            if st.button("Submit Answer"):
                is_correct = quiz.submit_answer(user_answer)
                st.rerun()
        else:
            # Show result
            if user_answer == question['correct_answer']:
                st.success(f"Correct! Great job!")
                if stats['streak'] > 1:
                    st.balloons()
            else:
                st.error(f"Wrong! The correct answer is: **{question['correct_answer']}** ({question['phonetic']})")
            
            # Show image for the word
            image_loader = ImageLoader()
            image = image_loader.get_image(question['word'])
            if image:
                st.image(image, width=300)
                st.markdown(f"""
                <div style='
                    text-align: center; 
                    font-size: 1.3em; 
                    font-weight: bold;
                    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                    color: white;
                    padding: 12px; 
                    border-radius: 8px; 
                    margin-top: 10px;
                    box-shadow: 0 3px 8px rgba(0,0,0,0.15);
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                '>
                    {question['word'].title()} - {question['correct_answer']} - ({question['phonetic']})
                </div>
                """, unsafe_allow_html=True)
    
    else:
        st.info("Click 'New Question' to start the quiz!")

def statistics_page():
    """Statistics and progress tracking"""
    st.subheader("Learning Statistics")
    
    # Vocabulary statistics
    st.markdown("### Vocabulary Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Words", len(VOCAB_DICT))
    
    with col2:
        st.metric("Categories", len(VOCAB_CATEGORIES))
    
    with col3:
        avg_length = sum(len(word) for word in VOCAB_DICT.keys()) / len(VOCAB_DICT)
        st.metric("Avg. Word Length", f"{avg_length:.1f}")
    
    # Category breakdown
    st.markdown("### Category Breakdown")
    
    category_data = []
    for category, words in VOCAB_CATEGORIES.items():
        category_data.append({
            "Category": category.title(),
            "Word Count": len(words),
            "Percentage": f"{(len(words) / len(VOCAB_DICT)) * 100:.1f}%"
        })
    
    import pandas as pd
    df = pd.DataFrame(category_data)
    st.dataframe(df, use_container_width=True)
    
    # Quiz statistics (if available)
    if 'quiz_state' in st.session_state and st.session_state.quiz_state['total'] > 0:
        st.markdown("### Quiz Performance")
        
        stats = st.session_state.quiz_state
        
        col1, col2 = st.columns(2)
        
        with col1:
            accuracy = (stats['score'] / stats['total']) * 100
            st.metric("Overall Accuracy", f"{accuracy:.1f}%")
            st.metric("Questions Answered", stats['total'])
        
        with col2:
            st.metric("Correct Answers", stats['score'])
            st.metric("Best Streak", stats['best_streak'])

def alphabet_page_backup():
    """Enhanced alphabets page with interactive handwriting animation"""
    st.subheader("ፊደላት (Tigrinya Alphabets)")
    
    # Initialize session state for selected character
    if 'selected_character' not in st.session_state:
        st.session_state.selected_character = None
    
    # Display alphabet grid
    st.markdown("### Click any character to see handwriting animation:")
    
    # Create alphabet grid with clickable buttons
    cols_per_row = 7
    alphabet_keys = list(TIGRINYA_ALPHABETS.keys())
    
    for i in range(0, len(alphabet_keys), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(alphabet_keys):
                alphabet_key = alphabet_keys[i + j]
                alphabet_data = TIGRINYA_ALPHABETS[alphabet_key]
                
                with col:
                    if st.button(
                        f"{alphabet_key}",
                        key=f"alphabet_{alphabet_key}",
                        help=f"Click to animate {alphabet_key}",
                        use_container_width=True
                    ):
                        st.session_state.selected_character = alphabet_key
                        st.rerun()
    
    # Display selected character details and animation
    if st.session_state.selected_character:
        selected_char = st.session_state.selected_character
        char_data = TIGRINYA_ALPHABETS[selected_char]
        
        st.markdown("---")
        
        # Character information
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 30px; 
                border-radius: 15px; 
                color: white;
                text-align: center;
                margin: 20px 0;
            '>
                <h1 style='font-size: 4em; margin: 0; font-family: "Noto Sans Ethiopic", serif;'>{selected_char}</h1>
                <h3 style='margin: 10px 0;'>Base Character</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Character forms table
            st.markdown("#### All Forms:")
            forms_df = []
            for i, (form, phonetic) in enumerate(zip(char_data['forms'], char_data['phonetic'])):
                forms_df.append({
                    "Form": form,
                    "Sound": phonetic,
                    "Order": i + 1
                })
            
            import pandas as pd
            df = pd.DataFrame(forms_df)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        with col2:
            # Handwriting animation
            st.markdown("#### Handwriting Animation")
            
            # Animation controls
            animation_col1, animation_col2 = st.columns(2)
            
            with animation_col1:
                pen_style = st.selectbox(
                    "Pen Style:",
                    ["Realistic", "Brush", "Simple"],
                    key="pen_style"
                )
            
            with animation_col2:
                animation_speed = st.slider(
                    "Speed:",
                    min_value=1.0,
                    max_value=5.0,
                    value=3.0,
                    step=0.5,
                    key="animation_speed"
                )
            
            # Generate and display handwriting animation
            if st.button("Start Handwriting Animation", type="primary", use_container_width=True):
                animation_html = create_handwriting_animation_html(
                    text=selected_char,
                    pen_style=pen_style,
                    writing_style="Natural",
                    animation_speed=animation_speed
                )
                
                components.html(
                    animation_html,
                    height=900,
                    scrolling=True
                )
            
            # Character practice section
            st.markdown("#### Practice Writing")
            st.info("Try writing this character on paper while watching the animation!")
            
            # Related characters or similar forms
            st.markdown("#### Related Forms")
            related_forms = char_data['forms'][:4]  # Show first 4 forms
            related_phonetics = char_data['phonetic'][:4]
            
            form_cols = st.columns(4)
            for i, (form, phonetic) in enumerate(zip(related_forms, related_phonetics)):
                with form_cols[i]:
                    if st.button(
                        f"{form}",
                        key=f"related_{form}",
                        help=f"Animate {form} ({phonetic})",
                        use_container_width=True
                    ):
                        animation_html = create_handwriting_animation_html(
                            text=form,
                            pen_style=pen_style,
                            writing_style="Natural",
                            animation_speed=animation_speed
                        )
                        
                        components.html(
                            animation_html,
                            height=400,
                            scrolling=False
                        )
    
    else:
        st.info("Select a character above to see its handwriting animation and details!")
    
    # Traditional alphabet table for reference
    st.markdown("---")
    st.markdown("### Traditional Alphabet Reference")
    
    # Show traditional grid format
    sample_alphabets = [
        ["በ (be)", "ቡ (bu)", "ቢ (bi)", "ባ (ba)", "ቤ (bie)", "ብ (b)", "ቦ (bo)"],
        ["ከ (ke)", "ኩ (ku)", "ኪ (ki)", "ካ (ka)", "ኬ (kie)", "ክ (k)", "ኮ (ko)"],
        ["ሰ (se)", "ሱ (su)", "ሲ (si)", "ሳ (sa)", "ሴ (sie)", "ስ (s)", "ሶ (so)"],
        ["ሸ (Se)", "ሹ (Su)", "ሺ (Si)", "ሻ (Sa)", "ሼ (Sie)", "ሽ (S)", "ሾ (So)"],
    ]

    table_header = '''
| 1st Order | 2nd Order | 3rd Order | 4th Order | 5th Order | 6th Order | 7th Order |
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
'''
    
    table_rows = ""
    for row in sample_alphabets:
        table_rows += f"| {' | '.join(row)} |\n"
        
    st.markdown(table_header + table_rows, unsafe_allow_html=True)

def alphabet_page():
    """Enhanced alphabets page with automatic handwriting animation"""
    st.subheader("ፊደላት (Tigrinya Alphabets)")
    
    # Initialize session state for selected character
    if 'selected_character' not in st.session_state:
        st.session_state.selected_character = None
    
    # Display alphabet grid
    st.markdown("### Click any character to see automatic handwriting animation:")
    
    # Create alphabet grid with clickable buttons
    cols_per_row = 7
    alphabet_keys = list(TIGRINYA_ALPHABETS.keys())
    
    for i in range(0, len(alphabet_keys), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(alphabet_keys):
                alphabet_key = alphabet_keys[i + j]
                alphabet_data = TIGRINYA_ALPHABETS[alphabet_key]
                
                with col:
                    if st.button(
                        f"{alphabet_key}",
                        key=f"alphabet_{alphabet_key}",
                        help=f"Click to animate {alphabet_key}",
                        use_container_width=True
                    ):
                        st.session_state.selected_character = alphabet_key
                        st.rerun()
    
    # Display selected character details and animation
    if st.session_state.selected_character:
        selected_char = st.session_state.selected_character
        char_data = TIGRINYA_ALPHABETS[selected_char]
        
        st.markdown("---")
        
        # Character information
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 30px; 
                border-radius: 15px; 
                color: white;
                text-align: center;
                margin: 20px 0;
            '>
                <h1 style='font-size: 4em; margin: 0; font-family: "Noto Sans Ethiopic", serif;'>{selected_char}</h1>
                <h3 style='margin: 10px 0;'>Base Character</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Character forms table
            st.markdown("#### All Forms:")
            forms_df = []
            for i, (form, phonetic) in enumerate(zip(char_data['forms'], char_data['phonetic'])):
                forms_df.append({
                    "Form": form,
                    "Sound": phonetic,
                    "Order": i + 1
                })
            
            import pandas as pd
            df = pd.DataFrame(forms_df)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        with col2:
            # Automatic handwriting animation - no button needed
            st.markdown("#### Handwriting Animation")
            st.info("Animation starting automatically...")
            
            # Generate and display handwriting animation that auto-starts
            animation_html = create_auto_start_handwriting_html(
                text=selected_char,
                pen_style="Realistic",  # Fixed to Realistic
                writing_style="Natural",
                animation_speed=4.0  # Fixed to 4.0
            )
            
            components.html(
                animation_html,
                height=900,
                scrolling=True
            )
            
            # Character practice section
            st.markdown("#### Practice Writing")
            st.info("Try writing this character on paper while watching the animation!")
            
            # Related characters or similar forms with auto-animation
            st.markdown("#### Related Forms - Click to animate")
            related_forms = char_data['forms'][:4]  # Show first 4 forms
            related_phonetics = char_data['phonetic'][:4]
            
            form_cols = st.columns(4)
            for i, (form, phonetic) in enumerate(zip(related_forms, related_phonetics)):
                with form_cols[i]:
                    if st.button(
                        f"{form}",
                        key=f"related_{form}_{selected_char}",  # Added selected_char to make unique
                        help=f"Animate {form} ({phonetic})",
                        use_container_width=True
                    ):
                        # Auto-animate related form
                        related_animation_html = create_handwriting_animation_html(
                            text=form,
                            pen_style="Realistic",
                            writing_style="Natural",
                            animation_speed=4.0
                        )
                        
                        # Display related form animation in an expander
                        with st.expander(f"Animation for {form} ({phonetic})", expanded=True):
                            components.html(
                                related_animation_html,
                                height=600,
                                scrolling=True
                            )
    
    else:
        st.info("Select a character above to see its automatic handwriting animation and details!")
    
    # Traditional alphabet table for reference
    st.markdown("---")
    st.markdown("### Traditional Alphabet Reference")
    
    # Show traditional grid format
    sample_alphabets = [
        ["በ (be)", "ቡ (bu)", "ቢ (bi)", "ባ (ba)", "ቤ (bie)", "ብ (b)", "ቦ (bo)"],
        ["ከ (ke)", "ኩ (ku)", "ኪ (ki)", "ካ (ka)", "ኬ (kie)", "ክ (k)", "ኮ (ko)"],
        ["ሰ (se)", "ሱ (su)", "ሲ (si)", "ሳ (sa)", "ሴ (sie)", "ስ (s)", "ሶ (so)"],
        ["ሸ (Se)", "ሹ (Su)", "ሺ (Si)", "ሻ (Sa)", "ሼ (Sie)", "ሽ (S)", "ሾ (So)"],
    ]

    table_header = '''
| 1st Order | 2nd Order | 3rd Order | 4th Order | 5th Order | 6th Order | 7th Order |
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
'''
    
    table_rows = ""
    for row in sample_alphabets:
        table_rows += f"| {' | '.join(row)} |\n"
        
    st.markdown(table_header + table_rows, unsafe_allow_html=True)

def create_auto_start_handwriting_html(text, pen_style="Realistic", writing_style="Natural", animation_speed=4.0):
    """Create HTML5 Canvas-based handwriting animation that starts automatically without buttons"""
    
    import json
    
    # Escape text for JavaScript
    safe_text = json.dumps(text)
    
    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tigrinya Handwriting Animation</title>
            <script src="https://cdn.jsdelivr.net/npm/opentype.js@latest/dist/opentype.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;700&display=swap');
                
                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: 'Noto Sans Ethiopic', 'Ebrima', 'Nyala', sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                
                .container {{
                    max-width: 1000px;
                    width: 100%;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    padding: 30px;
                    margin: 20px;
                }}
                
                h1 {{
                    text-align: center;
                    color: #2c3e50;
                    margin-bottom: 30px;
                    font-size: 2.2em;
                }}
                
                .animation-area {{
                    position: relative;
                    background: #fefefe;
                    border: 2px solid #e1e8ed;
                    border-radius: 10px;
                    margin: 20px 0;
                    min-height: 300px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 10px;
                }}
                
                .scroll-container {{
                    width: 100%;
                    max-width: 900px;
                    max-height: 400px;
                    overflow: auto;
                    border-radius: 8px;
                    border: 1px solid #ddd;
                    background: white;
                    position: relative;
                }}
                
                #animationCanvas {{
                    display: block;
                    background: white;
                    border-radius: 4px;
                }}
                
                .info-panel {{
                    background: #f8f9fa;
                    border-left: 4px solid #667eea;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                }}
                
                .text-display {{
                    font-size: 1.5em;
                    text-align: center;
                    margin: 15px 0;
                    padding: 15px;
                    background: #e8f4fd;
                    border-radius: 8px;
                    border: 1px solid #bee5eb;
                }}
                
                .progress-bar {{
                    width: 100%;
                    height: 6px;
                    background: #ecf0f1;
                    border-radius: 3px;
                    margin: 10px 0;
                    overflow: hidden;
                }}
                
                .progress-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #667eea, #764ba2);
                    border-radius: 3px;
                    width: 0%;
                    transition: width 0.3s ease;
                }}
                
                .status {{
                    text-align: center;
                    margin: 10px 0;
                    font-weight: 500;
                }}

                /* Custom scrollbar styling */
                .scroll-container::-webkit-scrollbar {{
                    width: 8px;
                    height: 8px;
                }}

                .scroll-container::-webkit-scrollbar-track {{
                    background: #f1f1f1;
                    border-radius: 4px;
                }}

                .scroll-container::-webkit-scrollbar-thumb {{
                    background: #667eea;
                    border-radius: 4px;
                }}

                .scroll-container::-webkit-scrollbar-thumb:hover {{
                    background: #5a67d8;
                }}

            </style>
        </head>
        <body>
            <div class="container">
                <h1>✍️ Tigrinya Handwriting Animation</h1>
                
                <div class="text-display">
                    <strong>Animating:</strong> {text}
                </div>
                
                <div class="info-panel">
                    <strong>Settings:</strong> Pen Style: {pen_style} | Writing Style: {writing_style} | Speed: {animation_speed}x
                </div>
                
                <div class="animation-area">
                    <div class="scroll-container" id="scrollContainer">
                        <canvas id="animationCanvas"></canvas>
                    </div>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                
                <div class="status" id="status">Loading font...</div>
            </div>

            <script>
                // Animation configuration
                const config = {{
                    text: {safe_text},
                    penStyle: "{pen_style}",
                    writingStyle: "{writing_style}",
                    animationSpeed: {animation_speed},
                    canvas: null,
                    ctx: null,
                    isAnimating: false,
                    isPaused: false,
                    currentCharIndex: 0,
                    currentStroke: 0,
                    frames: [],
                    animationFrame: null,
                    font: null,
                    characterPaths: [],
                    scrollContainer: null,
                    canvasWidth: 2400,
                    canvasHeight: 400
                }};

                // Load font and auto-start animation
                opentype.load('https://fonts.gstatic.com/s/notosansethiopic/v49/7cHPv50vjIepfJVOZZgcpQ5B9FBTH9KGNfhSTgtoow1KVnIvyBoMSzUMacb-T35OK6Dj.ttf', function (err, font) {{
                    if (err) {{
                        document.getElementById('status').textContent = 'Error loading font: ' + err;
                    }} else {{
                        config.font = font;
                        document.getElementById('status').textContent = 'Font loaded - Starting animation...';
                        initCanvas();
                        // Auto-start animation after a short delay
                        setTimeout(startAnimation, 500);
                    }}
                }});
                
                // Initialize canvas with proper dimensions
                function initCanvas() {{
                    config.canvas = document.getElementById('animationCanvas');
                    config.scrollContainer = document.getElementById('scrollContainer');
                    
                    // Set canvas size based on text length
                    const textLength = config.text.length;
                    const estimatedWidth = Math.max(800, textLength * 120);
                    
                    config.canvasWidth = estimatedWidth;
                    config.canvas.width = config.canvasWidth;
                    config.canvas.height = config.canvasHeight;
                    
                    config.ctx = config.canvas.getContext('2d');
                    config.ctx.imageSmoothingEnabled = true;
                    config.ctx.lineCap = 'round';
                    config.ctx.lineJoin = 'round';
                    
                    // Reset scroll to beginning
                    config.scrollContainer.scrollLeft = 0;
                }}

                // Auto-scroll to follow the pen
                function scrollToPosition(x) {{
                    if (!config.scrollContainer) return;
                    
                    const containerWidth = config.scrollContainer.clientWidth;
                    const scrollLeft = config.scrollContainer.scrollLeft;
                    const scrollRight = scrollLeft + containerWidth;
                    
                    // Keep pen in view with some padding
                    const padding = 100;
                    
                    if (x < scrollLeft + padding) {{
                        config.scrollContainer.scrollLeft = Math.max(0, x - padding);
                    }} else if (x > scrollRight - padding) {{
                        config.scrollContainer.scrollLeft = x - containerWidth + padding;
                    }}
                }}

                // Convert font paths to drawable strokes for handwriting effect
                function generateCharacterStrokes(text) {{
                    const strokes = [];
                    
                    const fontSize = 120; // Larger font size for single characters
                    const padding = 100;
                    const startX = padding;
                    const baseY = config.canvasHeight / 2 + fontSize / 4;
                    
                    let currentX = startX;
                    
                    for (let i = 0; i < text.length; i++) {{
                        const char = text[i];
                        
                        if (char === ' ') {{
                            const spaceWidth = config.font.getAdvanceWidth(' ', fontSize);
                            currentX += spaceWidth;
                            strokes.push({{
                                char: ' ',
                                type: 'space',
                                x: currentX,
                                y: baseY,
                                width: spaceWidth
                            }});
                            continue;
                        }}
                        
                        const fontPath = config.font.getPath(char, currentX, baseY, fontSize);
                        const charStrokes = convertPathToStrokes(fontPath, currentX, baseY);
                        
                        strokes.push({{
                            char: char,
                            type: 'character',
                            strokes: charStrokes,
                            x: currentX,
                            y: baseY
                        }});
                        
                        currentX += config.font.getAdvanceWidth(char, fontSize);
                    }}
                    
                    return strokes;
                }}

                // Convert OpenType path to handwriting strokes
                function convertPathToStrokes(path, offsetX, offsetY) {{
                    const strokes = [];
                    let currentStroke = [];
                    
                    for (const cmd of path.commands) {{
                        switch (cmd.type) {{
                            case 'M': // Move to
                                if (currentStroke.length > 0) {{
                                    strokes.push(currentStroke);
                                }}
                                currentStroke = [{{x: cmd.x, y: cmd.y}}];
                                break;
                                
                            case 'L': // Line to
                                currentStroke.push({{x: cmd.x, y: cmd.y}});
                                break;
                                
                            case 'Q': // Quadratic curve
                                const p0 = currentStroke[currentStroke.length - 1];
                                for (let t = 0.1; t <= 1; t += 0.1) {{
                                    const x = Math.pow(1-t, 2) * p0.x + 2*(1-t)*t * cmd.x1 + Math.pow(t, 2) * cmd.x;
                                    const y = Math.pow(1-t, 2) * p0.y + 2*(1-t)*t * cmd.y1 + Math.pow(t, 2) * cmd.y;
                                    currentStroke.push({{x, y}});
                                }}
                                break;
                                
                            case 'C': // Cubic curve
                                const p0c = currentStroke[currentStroke.length - 1];
                                for (let t = 0.1; t <= 1; t += 0.1) {{
                                    const x = Math.pow(1-t, 3) * p0c.x + 
                                            3 * Math.pow(1-t, 2) * t * cmd.x1 +
                                            3 * (1-t) * Math.pow(t, 2) * cmd.x2 + 
                                            Math.pow(t, 3) * cmd.x;
                                    const y = Math.pow(1-t, 3) * p0c.y + 
                                            3 * Math.pow(1-t, 2) * t * cmd.y1 +
                                            3 * (1-t) * Math.pow(t, 2) * cmd.y2 + 
                                            Math.pow(t, 3) * cmd.y;
                                    currentStroke.push({{x, y}});
                                }}
                                break;
                                
                            case 'Z': // Close path
                                if (currentStroke.length > 0) {{
                                    strokes.push(currentStroke);
                                    currentStroke = [];
                                }}
                                break;
                        }}
                    }}
                    
                    if (currentStroke.length > 0) {{
                        strokes.push(currentStroke);
                    }}
                    
                    return strokes;
                }}
                
                // Pen drawing functions
                function drawPen(x, y, angle = 0) {{
                    const ctx = config.ctx;
                    ctx.save();
                    ctx.translate(x, y);
                    ctx.rotate(angle);
                    
                    // Realistic pen style
                    // Pen shadow
                    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
                    ctx.fillRect(-3, 3, 6, 30);
                    
                    // Pen body
                    ctx.fillStyle = '#4169E1';
                    ctx.fillRect(-3, 0, 6, 27);
                    
                    // Pen grip
                    ctx.fillStyle = '#696969';
                    ctx.fillRect(-3.5, 9, 7, 9);
                    
                    // Pen tip
                    ctx.fillStyle = '#000080';
                    ctx.beginPath();
                    ctx.arc(0, 0, 2, 0, Math.PI * 2);
                    ctx.fill();
                    
                    ctx.restore();
                }}
                
                // Main animation functions
                function startAnimation() {{
                    if (config.isAnimating) return;
                    
                    config.isAnimating = true;
                    config.characterPaths = generateCharacterStrokes(config.text);
                    config.currentCharIndex = 0;
                    config.currentStroke = 0;
                    
                    document.getElementById('status').textContent = 'Animating...';
                    animateNextFrame();
                }}

                function animateNextFrame() {{
                    if (config.isPaused || !config.isAnimating) return;
                    
                    const paths = config.characterPaths;
                    if (!paths || config.currentCharIndex >= paths.length) {{
                        // Animation complete
                        config.isAnimating = false;
                        document.getElementById('status').textContent = 'Animation complete!';
                        document.getElementById('progressFill').style.width = '100%';
                        return;
                    }}
                    
                    const currentPath = paths[config.currentCharIndex];
                    
                    // Update progress
                    const progress = (config.currentCharIndex / paths.length) * 100;
                    document.getElementById('progressFill').style.width = progress + '%';
                    
                    if (currentPath.type === 'space') {{
                        scrollToPosition(currentPath.x);
                        setTimeout(() => {{
                            config.currentCharIndex++;
                            config.currentStroke = 0;
                            config.animationFrame = requestAnimationFrame(animateNextFrame);
                        }}, 300 / config.animationSpeed);
                        return;
                    }}
                    
                    if (config.currentStroke >= currentPath.strokes.length) {{
                        config.currentCharIndex++;
                        config.currentStroke = 0;
                        config.animationFrame = requestAnimationFrame(animateNextFrame);
                        return;
                    }}
                    
                    const stroke = currentPath.strokes[config.currentStroke];
                    animateStroke(stroke, () => {{
                        config.currentStroke++;
                        setTimeout(() => {{
                            config.animationFrame = requestAnimationFrame(animateNextFrame);
                        }}, 100 / config.animationSpeed);
                    }});
                }}

                // Animate individual stroke with handwriting effect
                function animateStroke(stroke, callback) {{
                    if (!stroke || stroke.length === 0) {{
                        callback();
                        return;
                    }}
                    
                    let pointIndex = 0;
                    const ctx = config.ctx;
                    
                    function drawNextSegment() {{
                        if (pointIndex >= stroke.length) {{
                            callback();
                            return;
                        }}
                        
                        redrawCanvas();
                        
                        if (pointIndex === 0) {{
                            const penX = stroke[0].x;
                            const penY = stroke[0].y - 35;
                            drawPen(penX, penY);
                            scrollToPosition(penX);
                        }} else {{
                            ctx.strokeStyle = '#2c3e50';
                            ctx.lineWidth = 4;
                            ctx.lineCap = 'round';
                            ctx.lineJoin = 'round';
                            
                            ctx.beginPath();
                            ctx.moveTo(stroke[0].x, stroke[0].y);
                            
                            for (let i = 1; i <= pointIndex; i++) {{
                                ctx.lineTo(stroke[i].x, stroke[i].y);
                            }}
                            ctx.stroke();
                            
                            const currentPoint = stroke[pointIndex];
                            const penX = currentPoint.x;
                            const penY = currentPoint.y - 35;
                            drawPen(penX, penY);
                            scrollToPosition(penX);
                        }}
                        
                        pointIndex++;
                        setTimeout(drawNextSegment, 40 / config.animationSpeed);
                    }}
                    
                    drawNextSegment();
                }}

                // Redraw the entire canvas with completed characters and strokes
                function redrawCanvas() {{
                    const ctx = config.ctx;
                    
                    ctx.clearRect(0, 0, config.canvas.width, config.canvas.height);
                    ctx.fillStyle = '#fefefe';
                    ctx.fillRect(0, 0, config.canvas.width, config.canvas.height);
                    
                    // Draw all completed characters
                    for (let charIndex = 0; charIndex < config.currentCharIndex; charIndex++) {{
                        const path = config.characterPaths[charIndex];
                        if (path.type === 'character') {{
                            drawCompletedCharacter(path);
                        }}
                    }}
                    
                    // Draw completed strokes of current character
                    if (config.currentCharIndex < config.characterPaths.length && 
                        config.characterPaths[config.currentCharIndex].type === 'character') {{
                        const currentPath = config.characterPaths[config.currentCharIndex];
                        
                        ctx.strokeStyle = '#2c3e50';
                        ctx.lineWidth = 4;
                        ctx.lineCap = 'round';
                        ctx.lineJoin = 'round';
                        
                        for (let strokeIndex = 0; strokeIndex < config.currentStroke; strokeIndex++) {{
                            const stroke = currentPath.strokes[strokeIndex];
                            if (stroke && stroke.length > 0) {{
                                ctx.beginPath();
                                ctx.moveTo(stroke[0].x, stroke[0].y);
                                for (let i = 1; i < stroke.length; i++) {{
                                    ctx.lineTo(stroke[i].x, stroke[i].y);
                                }}
                                ctx.stroke();
                            }}
                        }}
                    }}
                }}

                // Draw a completed character
                function drawCompletedCharacter(path) {{
                    const ctx = config.ctx;
                    
                    ctx.strokeStyle = '#2c3e50';
                    ctx.lineWidth = 4;
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';
                    
                    for (const stroke of path.strokes) {{
                        if (stroke && stroke.length > 0) {{
                            ctx.beginPath();
                            ctx.moveTo(stroke[0].x, stroke[0].y);
                            for (let i = 1; i < stroke.length; i++) {{
                                ctx.lineTo(stroke[i].x, stroke[i].y);
                            }}
                            ctx.stroke();
                        }}
                    }}
                }}
            </script>
        </body>
        </html>
            """
    return html_content    

def main():
    # Page configuration
    st.set_page_config(
        page_title="Tigrinya Vocabulary Learning App",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stSelectbox > div > div > div > div {
        font-size: 16px;
    }
    .stButton > button {
        font-family: 'Noto Sans Ethiopic', serif;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main title
    st.title("📚 English-Tigrinya Vocabulary Learning App")
    st.markdown("*Learn Tigrinya vocabulary with visual aids, interactive quizzes, and handwriting animations*")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Choose a learning mode:")
    
    page = st.sidebar.radio(
        "Choose a page:",
        ["🔍 Search Translation", "📚 Browse Vocabulary", "✍️ ፊደላት (Alphabets)", "🎯 Quiz Mode", "📊 Statistics"],
        label_visibility="collapsed"
    )
    
    # Page routing
    if page == "🔍 Search Translation":
        search_page()
    elif page == "📚 Browse Vocabulary":
        browse_page()
    elif page == "✍️ ፊደላት (Alphabets)":
        alphabet_page()
    elif page == "🎯 Quiz Mode":
        quiz_page()
    elif page == "📊 Statistics":
        statistics_page()
    
    # Sidebar information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Tips")
    st.sidebar.info(
        "• Use the search to find specific words\n"
        "• Browse vocabulary by category\n"
        "• Click alphabet characters for handwriting animations\n"
        "• Take quizzes to test your knowledge\n"
        "• Check statistics to track progress"
    )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ using Streamlit | Enhanced with handwriting animations"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()