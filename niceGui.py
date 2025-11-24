import os
import random
import requests
from io import BytesIO
from typing import Dict, Optional, Tuple

from nicegui import ui, app
from PIL import Image
import base64
import json

# --- Data from clientTranslation.py and interface_advanced_integrated.py ---

# Vowel mapping
vowel_to_index = {"e":0,"u":1,"i":2,"a":3,"ē":4,"ə":5,"":5,"o":6}

# Feedel rows
feedel_rows = {
    'h':  ("ሀ","ሁ","ሂ","ሃ","ሄ","ህ","ሆ"),
    'ḥ':  ("ሐ","ሑ","ሒ","ሓ","ሔ","ሕ","ሖ"),
    'x':  ("ኀ","ኁ","ኂ","ኃ","ኄ","ኅ","ኆ"),
    'ḫ':  ("ኸ","ኹ","ኺ","ኻ","ኼ","ኽ","ኾ"),
    'k':  ("ከ","ኩ","ኪ","ካ","ኬ","ክ","ኮ"),
    'ʿ':  ("ዐ","ዑ","ዒ","ዓ","ዔ","ዕ","ዖ"),
    'l':  ("ለ","ሉ","ሊ","ላ", "ሌ","ል","ሎ"),
    'm':  ("መ","ሙ","ሚ","ማ","ሜ","ም","ሞ"),
    'r':  ("ረ","ሩ","ሪ","ራ","ሬ","ር","ሮ"),
    's':  ("ሰ","ሱ","ሲ","ሳ","ሴ","ስ","ሶ"),
    'š':  ("ሸ","ሹ","ሺ","ሻ","ሼ","ሽ","ሾ"),
    'q':  ("ቀ","ቁ","ቂ","ቃ","ቄ","ቅ","ቆ"),
    'b':  ("በ","ቡ","ቢ","ባ","ቤ","ብ","ቦ"),
    't':  ("ተ","ቱ","ቲ","ታ","ቴ","ት","ቶ"),
    'ṭ':  ("ጠ","ጡ","ጢ","ጣ","ጤ","ጥ","ጦ"),
    'č':  ("ቸ","ቹ","ቺ","ቻ","ቼ","ች","ቾ"),
    'č̣':  ("ጨ","ጩ","ጪ","ጫ","ጬ","ጭ","ጮ"),
    'p':  ("ፐ","ፑ","ፒ","ፓ","ፔ","ፕ","ፖ"),
    'p̣':  ("ጰ","ጱ","ጲ","ጳ","ጴ","ጵ","ጶ"),
    'g':  ("ገ","ጉ","ጊ","ጋ","ጌ","ግ","ጎ"),
    'd':  ("ደ","ዱ","ዲ","ዳ","ዴ","ድ","ዶ"),
    'f':  ("ፈ","ፉ","ፊ","ፋ","ፌ","ፍ","ፎ"),
    'z':  ("ዘ","ዙ","ዚ","ዛ","ዜ","ዝ","ዞ"),
    'ž':  ("ዠ","ዡ","ዢ","ዣ","ዤ","ዥ","ዦ"),
    'y':  ("የ","ዩ","ዪ","ያ","ዬ","ይ","ዮ"),
    'w':  ("ወ","ዉ", "ዊ","ዋ","ዌ","ው","ዎ"),
    'n':  ("ነ","ኑ","ኒ","ና","ኔ","ን","ኖ"),
    'ñ':  ("ኘ","ኙ","ኚ","ኛ","ኜ","ኝ","ኞ"),
    'ṣ':  ("ፀ","ፁ","ፂ","ፃ","ፄ","ፅ","ፆ"),
    'j':  ("ጀ","ጁ","ጂ","ጃ","ጄ","ጅ","ጆ"),
}
alef_row = ("አ","ኡ","ኢ","ኣ","ኤ","እ","ኦ")

# Reverse mapping for Geʽez → Latin
geez_char_to_cv: Dict[str, Tuple[str,str]] = {}
for cons, row in feedel_rows.items():
    geez_char_to_cv.update({row[i]:(cons,v) for i,v in enumerate(["e","u","i","a","ē","ə","o"])})
geez_char_to_cv.update({
    alef_row[0]:("", "a"), alef_row[1]:("", "u"), alef_row[2]:("", "i"),
    alef_row[3]:("", "ā"), alef_row[4]:("", "ē"), alef_row[5]:("", "ə"),
    alef_row[6]:("", "o")
})

def geez_to_latin_syllable(text: str) -> str:
    """Convert Geʽez to Latin transliteration (syllable-based)"""
    result = ""
    for ch in text:
        if ch in geez_char_to_cv:
            cons, vowel = geez_char_to_cv[ch]
            if vowel == "ə": result += cons
            else: result += cons + vowel
        else: result += ch
    return result

# Vocabulary
VOCAB_CATEGORIES = {
    "colors": {"red": "ቀይሕ", "blue": "ሰማያዊ", "green": "ቀጠልያ", "yellow": "ቢጫ", "black": "ጸሊም", "white": "ጻዕዳ", "orange": "ኣራንቾኒ", "purple": "ሊላ", "brown": "ቡናዊ"},
    "animals": {"dog": "ከልቢ", "cat": "ድሙ", "cow": "ላም", "lion": "ኣንበሳ", "horse": "ፈረስ", "goat": "ጤል", "chicken": "ዶርሆ", "fish": "ዓሳ", "sheep": "በጊዕ", "camel": "ገመል", "elephant": "ሓርማዝ", "monkey": "ህበይ", "zebra": "ኣድጊ በረኻ", "giraffe": "ዘራፍ", "snake": "ተመን", "tiger": "ነብሪ", "bear": "ድቢ", "donkey": "ኣድጊ", "rabbit": "ማንቲለ", "mouse": "ኣንጭዋ"},
    "objects": {"book": "መጽሓፍ", "pen": "ብርዒ", "chair": "ኩርሲ", "table": "ጣውላ", "car": "መኪና", "bus": "ኣውቶቡስ", "phone": "ተሌፎን", "hat": "ቆብዕ", "shoe": "ሳእኒ", "house": "ገዛ", "apple": "ቱፋሕ", "banana": "ባናና", "bed": "ዓራት", "cup": "ቢኬሪ", "key": "መፍትሕ", "door": "ማዕጾ", "bag": "ቦርሳ"}
}
VOCAB_DICT = {k: v for cat in VOCAB_CATEGORIES.values() for k, v in cat.items()}

# Tigrinya Alphabets
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

# --- Handwriting Animation HTML ---
def create_handwriting_animation_html(text, pen_style="Realistic", writing_style="Natural", animation_speed=3.5):
    """Create HTML5 Canvas-based handwriting animation with scrollable canvas"""
    safe_text = json.dumps(text)
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tigrinya Handwriting Animation</title>
            <script src="https://cdn.jsdelivr.net/npm/opentype.js@latest/dist/opentype.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;700&display=swap');
                body {{ margin: 0; font-family: 'Noto Sans Ethiopic', sans-serif; }}
                .container {{ padding: 20px; }}
                .animation-area {{ border: 1px solid #ddd; overflow: auto; max-height: 450px; }}
                #animationCanvas {{ display: block; }}
                .controls {{ margin-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="animation-area" id="scrollContainer">
                    <canvas id="animationCanvas"></canvas>
                </div>
                <div class="controls">
                    <button id="startBtn" onclick="startAnimation()" disabled>Start</button>
                    <button onclick="pauseAnimation()">Pause</button>
                    <button onclick="resetAnimation()">Reset</button>
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
                        document.getElementById('startBtn').textContent = 'Error loading font: ' + err;
                    }} else {{
                        config.font = font;
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
                    animateNextFrame();
                }}
                
                function pauseAnimation() {{
                    config.isPaused = true;
                    if (config.animationFrame) {{
                        cancelAnimationFrame(config.animationFrame);
                    }}
                }}

                function animateNextFrame() {{
                    if (config.isPaused || !config.isAnimating) return;
                    
                    const paths = config.characterPaths;
                    if (!paths || config.currentCharIndex >= paths.length) {{
                        // Animation complete
                        config.isAnimating = false;
                        return;
                    }}
                    
                    const currentPath = paths[config.currentCharIndex];
                    
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
                }}
                
                // Initialize when page loads
                window.onload = function() {{
                    // Initialization will happen after font loads
                }};
            </script>
        </body>
        </html>
    """

# --- Application State and Helper Classes ---

class ImageLoader:
    """Handles image loading from various sources with caching"""
    def __init__(self, images_folder: str = "images"):
        self.images_folder = images_folder
        self._cache = {}

    def get_local_image(self, word: str) -> Optional[bytes]:
        if word in self._cache: return self._cache[word]
        if not os.path.exists(self.images_folder): return None
        for ext in ['.png', '.jpg', '.jpeg', '.gif']:
            path = os.path.join(self.images_folder, f"{word.lower()}{ext}")
            if os.path.exists(path):
                with open(path, "rb") as f:
                    content = f.read()
                    self._cache[word] = content
                    return content
        return None

    def get_image(self, word: str) -> Optional[bytes]:
        local_img = self.get_local_image(word)
        if local_img: return local_img
        try:
            url = f"https://source.unsplash.com/400x300/?{word}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self._cache[word] = response.content
                return response.content
        except Exception:
            pass
        return None

class QuizManager:
    """Manages quiz state and scoring"""
    def __init__(self):
        pass

    def reset_quiz(self):
        app.storage.user.update({
            'score': 0, 'total': 0, 'streak': 0, 'best_streak': 0,
            'current_question': None, 'answered': False
        })

    def generate_question(self, category: str = "all"):
        vocab = VOCAB_DICT if category == "all" else VOCAB_CATEGORIES.get(category, VOCAB_DICT)
        word = random.choice(list(vocab.keys()))
        correct_answer = vocab[word]
        
        wrong_pool = [ans for ans in VOCAB_DICT.values() if ans != correct_answer]
        options = [correct_answer] + random.sample(wrong_pool, min(3, len(wrong_pool)))
        random.shuffle(options)
        
        question = {
            'word': word, 'correct_answer': correct_answer, 'options': options,
            'phonetic': geez_to_latin_syllable(correct_answer)
        }
        app.storage.user['current_question'] = question
        app.storage.user['answered'] = False
        return question

    def submit_answer(self, user_answer: str) -> bool:
        if app.storage.user['answered']: return False
        
        question = app.storage.user['current_question']
        is_correct = user_answer == question['correct_answer']
        
        app.storage.user['total'] += 1
        app.storage.user['answered'] = True
        
        if is_correct:
            app.storage.user['score'] += 1
            app.storage.user['streak'] += 1
            if app.storage.user['streak'] > app.storage.user['best_streak']:
                app.storage.user['best_streak'] = app.storage.user['streak']
        else:
            app.storage.user['streak'] = 0
        return is_correct

# --- UI Pages ---

image_loader = ImageLoader()
quiz_manager = None # Will be initialized on startup

def create_word_card(word: str, translation: str, phonetic: str, show_image: bool = True):
    with ui.card().tight().classes('w-full'):
        with ui.row().classes('w-full items-center'):
            with ui.column().classes('w-1/2 p-4'):
                ui.label(word.title()).classes('text-xl')
                ui.label(translation).classes('text-4xl font-bold')
                ui.label(f"({phonetic})").classes('text-lg')
            if show_image:
                with ui.column().classes('w-1/2'):
                    img_data = image_loader.get_image(word)
                    if img_data:
                        b64_img = base64.b64encode(img_data).decode('utf-8')
                        ui.image(f'data:image/png;base64,{b64_img}')
                    else:
                        ui.label("No image").classes('text-center')

@ui.page('/search')
def search_page():
    with ui.column().classes('w-full items-center'):
        ui.label("Search & Translate").classes('text-2xl font-bold mb-4')
        
        result_area = ui.column().classes('w-full md:w-2/3')
        
        def do_search(word):
            result_area.clear()
            if not word: return
            
            translation = VOCAB_DICT.get(word)
            if translation:
                phonetic = geez_to_latin_syllable(translation)
                with result_area:
                    ui.notify("Found in vocabulary!", type='positive')
                    create_word_card(word, translation, phonetic)
            else:
                ui.notify("Word not in local vocabulary. (Online translation not implemented in this version)", type='warning')

        with ui.row():
            select = ui.select(options=sorted(VOCAB_DICT.keys()), label="Select a word", on_change=lambda e: do_search(e.value))
            ui.input(label="Or type a word", on_change=lambda e: do_search(e.value.lower().strip()))

@ui.page('/browse')
def browse_page():
    with ui.column().classes('w-full items-center'):
        ui.label("Browse Vocabulary").classes('text-2xl font-bold mb-4')
        
        grid = ui.grid(columns=3).classes('w-full gap-4')
        
        def update_view(category):
            grid.clear()
            vocab = VOCAB_DICT if category == "All" else VOCAB_CATEGORIES.get(category.lower(), {})
            with grid:
                for word, translation in vocab.items():
                    with ui.card():
                        ui.label(word.title()).classes('text-lg')
                        ui.label(translation).classes('text-2xl font-bold')
                        ui.label(f"({geez_to_latin_syllable(translation)})")

        ui.select(options=["All"] + [c.title() for c in VOCAB_CATEGORIES.keys()], 
                  value="All",
                  label="Filter by category", 
                  on_change=lambda e: update_view(e.value))
        
        update_view("All")

@ui.page('/quiz')
def quiz_page():
    with ui.column().classes('w-full items-center'):
        ui.label("Vocabulary Quiz").classes('text-2xl font-bold mb-4')

        stats = app.storage.user
        question_area = ui.column().classes('w-full md:w-2/3 items-center')
        
        def show_question():
            question_area.clear()
            quiz_manager.generate_question()
            question = stats['current_question']
            with question_area:
                ui.label(f"What is the Tigrinya for: {question['word'].title()}?").classes('text-xl')
                
                options_group = ui.radio(question['options'], on_change=lambda e: setattr(options_group, 'value', e.value))
                
                def handle_submit():
                    is_correct = quiz_manager.submit_answer(options_group.value)
                    if is_correct:
                        ui.notify("Correct!", type='positive')
                    else:
                        ui.notify(f"Wrong! Correct is: {question['correct_answer']}", type='negative')
                    
                    # Refresh to show updated stats and result
                    ui.navigate.to(quiz_page)

                ui.button("Submit", on_click=handle_submit)

        with ui.row():
            ui.button("New Question", on_click=show_question)
            ui.button("Reset Stats", on_click=lambda: (quiz_manager.reset_quiz(), ui.navigate.to(quiz_page)))

        with ui.row():
            ui.label(f"Score: {stats.get('score',0)}/{stats.get('total',0)}")
            ui.label(f"Streak: {stats.get('streak',0)}")
            ui.label(f"Best Streak: {stats.get('best_streak',0)}")

        if stats.get('current_question') and stats.get('answered'):
            with question_area:
                question = stats['current_question']
                ui.label("Result:").classes('text-lg mt-4')
                create_word_card(question['word'], question['correct_answer'], question['phonetic'])

@ui.page('/alphabet')
def alphabet_page():
    with ui.column().classes('w-full items-center'):
        ui.label("Tigrinya Alphabets (ፊደላት)").classes('text-2xl font-bold mb-4')
        
        animation_area = ui.column().classes('w-full md:w-2/3')
        
        def show_char_details(char_key):
            animation_area.clear()
            char_data = TIGRINYA_ALPHABETS[char_key]
            with animation_area:
                with ui.card():
                    ui.label(f"Details for {char_key}").classes('text-xl')
                    with ui.row():
                        for form, phonetic in zip(char_data['forms'], char_data['phonetic']):
                            with ui.column().classes('items-center'):
                                ui.label(form).classes('text-3xl')
                                ui.label(phonetic)
                    
                    ui.html(create_handwriting_animation_html(char_key)).classes('w-full h-96')

        with ui.grid(columns=8).classes('gap-2'):
            for char_key in TIGRINYA_ALPHABETS:
                ui.button(char_key, on_click=lambda k=char_key: show_char_details(k))

# --- Main App Layout ---
@ui.page('/')
def main_page():
    with ui.header().classes(replace='row items-center justify-between'):
        ui.label('Tigrinya Learning App').classes('text-2xl')
        with ui.row().classes('gap-4'):
            ui.link('Search', '/search').classes('text-white')
            ui.link('Browse', '/browse').classes('text-white')
            ui.link('Quiz', '/quiz').classes('text-white')
            ui.link('Alphabet', '/alphabet').classes('text-white')
    
    with ui.column().classes('w-full items-center p-8'):
        ui.label("Welcome to the Tigrinya Learning App!").classes("text-3xl font-bold")
        ui.label("Select a section from the tabs above to get started.").classes("text-lg")
        with ui.card().classes('mt-8'):
            ui.label("Features:").classes("text-xl font-bold")
            ui.markdown("""
                - **Search:** Find Tigrinya translations for English words.
                - **Browse:** Explore the full vocabulary by category.
                - **Quiz:** Test your knowledge with an interactive quiz.
                - **Alphabet:** Learn the Tigrinya alphabet with handwriting animations.
            """)

def initialize_app_components():
    global quiz_manager
    quiz_manager = QuizManager()
    # Initialize user storage
    app.storage.user.setdefault('score', 0)
    app.storage.user.setdefault('total', 0)
    app.storage.user.setdefault('streak', 0)
    app.storage.user.setdefault('best_streak', 0)
    app.storage.user.setdefault('current_question', None)
    app.storage.user.setdefault('answered', False)

#ui.on_startup(initialize_app_components)
app.on_startup(initialize_app_components)

ui.run(storage_secret='my-secret-key')
