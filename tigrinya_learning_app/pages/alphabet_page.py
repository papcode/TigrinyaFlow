"""
Alphabet page module - Enhanced with auto-starting handwriting animations
Complete implementation with exact flow from interface_reference.py
"""

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from utils.image_loader import ImageLoader

from clientTranslation import alef_row, feedel_rows, geez_to_latin_syllable


# Create TIGRINYA_ALPHABETS data structure from existing feedel_rows and alef_row
def create_tigrinya_alphabets():
    """Create the alphabet data structure matching interface_reference.py format"""
    tigrinya_alphabets = {}

    # Add alef row (vowel-only characters)
    vowel_names = ["a", "u", "i", "ā", "ē", "ə", "o"]
    for i, char in enumerate(alef_row):
        tigrinya_alphabets[char] = {
            "forms": [char],  # Vowel characters have only one form
            "phonetic": [vowel_names[i]],
        }

    # Add consonant rows
    vowel_sounds = ["e", "u", "i", "a", "ē", "ə", "o"]
    for consonant, forms in feedel_rows.items():
        # Use the first form (6th order - base form) as the key
        base_char = forms[5]  # 6th form is the base consonant
        tigrinya_alphabets[base_char] = {
            "forms": list(forms),
            "phonetic": [f"{consonant}{vowel}" for vowel in vowel_sounds],
        }

    return tigrinya_alphabets


TIGRINYA_ALPHABETS = create_tigrinya_alphabets()


def create_auto_start_handwriting_html(
    text,
    pen_style="Realistic",
    writing_style="Natural",
    animation_speed=4.0,
    step_size=2,
):
    """
    Create HTML5 Canvas-based fluid handwriting animation with continuous path system

    Args:
        text (str): Text to animate
        pen_style (str): Style of pen rendering ("Realistic", "Simple", "Brush")
        writing_style (str): Writing characteristics ("Natural", "Formal", "Cursive")
        animation_speed (float): Animation speed multiplier
        step_size (int): Point sampling density in pixels (1-3 for smooth animation)

    Returns:
        str: Complete HTML content with fluid handwriting animation
    """

    import json

    # Escape text for JavaScript
    safe_text = json.dumps(text)

    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Fluid Handwriting Animation - Enhanced</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/opentype.js/1.3.4/opentype.min.js"></script>
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
                    max-width: 1200px;
                    width: 100%;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 15px 40px rgba(0,0,0,0.12);
                    padding: 40px;
                    margin: 20px;
                }}

                .text-display {{
                    font-size: 1.6em;
                    text-align: center;
                    margin: 20px 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #e8f4fd 0%, #f0f8ff 100%);
                    border-radius: 12px;
                    border: 2px solid rgba(102, 126, 234, 0.2);
                    color: #2c3e50;
                    font-weight: 500;
                }}

                .animation-area {{
                    position: relative;
                    background: #fefefe;
                    border: 2px solid #e1e8ed;
                    border-radius: 15px;
                    margin: 25px 0;
                    min-height: 350px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 15px;
                    box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
                }}

                .scroll-container {{
                    width: 100%;
                    max-width: 1000px;
                    max-height: 450px;
                    overflow: auto;
                    border-radius: 10px;
                    border: 1px solid #ddd;
                    background: white;
                    position: relative;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}

                #animationCanvas {{
                    display: block;
                    background: white;
                    border-radius: 8px;
                }}

                .progress-container {{
                    margin: 20px 0;
                }}

                .progress-bar {{
                    width: 100%;
                    height: 8px;
                    background: #ecf0f1;
                    border-radius: 4px;
                    overflow: hidden;
                    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
                }}

                .progress-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #667eea, #764ba2);
                    border-radius: 4px;
                    width: 0%;
                    transition: width 0.3s ease;
                    box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
                }}

                .status {{
                    text-align: center;
                    margin: 15px 0;
                    font-weight: 600;
                    font-size: 1.1em;
                    color: #2c3e50;
                }}

                .scroll-container::-webkit-scrollbar {{
                    width: 10px;
                    height: 10px;
                }}

                .scroll-container::-webkit-scrollbar-track {{
                    background: #f1f1f1;
                    border-radius: 5px;
                }}

                .scroll-container::-webkit-scrollbar-thumb {{
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 5px;
                }}

                .scroll-container::-webkit-scrollbar-thumb:hover {{
                    background: linear-gradient(135deg, #5a67d8, #6b46c1);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="text-display">
                    <strong>Animating:</strong> {text}
                </div>

                <div class="animation-area">
                    <div class="scroll-container" id="scrollContainer">
                        <canvas id="animationCanvas"></canvas>
                    </div>
                </div>

                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <div class="status" id="status">Loading font and preparing animation...</div>
                </div>
            </div>

            <script>
                // Enhanced animation configuration with fluid path system
                const config = {{
                    text: {safe_text},
                    penStyle: "{pen_style}",
                    writingStyle: "{writing_style}",
                    animationSpeed: {animation_speed},
                    stepSize: {step_size},

                    // Canvas elements
                    canvas: null,
                    ctx: null,
                    glyphCanvas: null,
                    glyphCtx: null,
                    maskCanvas: null,
                    maskCtx: null,

                    // Animation state
                    isAnimating: false,
                    currentCharIndex: 0,
                    currentPointIndex: 0,

                    // Font and layout
                    font: null,
                    fontSize: 120,
                    characters: [],
                    scrollContainer: null,
                    canvasWidth: 2400,
                    canvasHeight: 400,

                    // Fluid path settings
                    revealMode: 'ink-mask',
                    nibRadius: 0,
                    inkColor: '#2c3e50',

                    // Animation state
                    penX: 0,
                    penY: 0,
                    penPressure: 1.0,
                    penSpeed: 0,
                    animationFrame: null,

                    // Performance tracking
                    lastFrameTime: 0,
                    frameCount: 0
                }};

                // Load font and initialize with auto-start
                opentype.load('https://fonts.gstatic.com/s/notosansethiopic/v49/7cHPv50vjIepfJVOZZgcpQ5B9FBTH9KGNfhSTgtoow1KVnIvyBoMSzUMacb-T35OK6Dj.ttf', function (err, font) {{
                    if (err) {{
                        console.error('Font loading error:', err);
                        document.getElementById('status').textContent = 'Error loading font. Using fallback - Starting animation...';
                        initWithoutFont();
                        setTimeout(startAnimation, 800);
                    }} else {{
                        config.font = font;
                        document.getElementById('status').textContent = 'Font loaded successfully - Starting animation...';
                        initCanvas();
                        prepareCharacterPaths();
                        setTimeout(startAnimation, 500);
                    }}
                }});

                // Initialize without font (fallback)
                function initWithoutFont() {{
                    config.font = null;
                    initCanvas();
                    prepareCharacterPaths();
                }}

                // Initialize canvas system
                function initCanvas() {{
                    config.canvas = document.getElementById('animationCanvas');
                    config.scrollContainer = document.getElementById('scrollContainer');

                    // Calculate optimal canvas dimensions
                    const textLength = config.text.length;
                    const estimatedWidth = Math.max(900, textLength * 130);
                    config.canvasWidth = estimatedWidth;
                    config.canvas.width = config.canvasWidth;
                    config.canvas.height = config.canvasHeight;
                    config.ctx = config.canvas.getContext('2d');

                    // Create offscreen canvases for compositing
                    config.glyphCanvas = document.createElement('canvas');
                    config.glyphCanvas.width = config.canvasWidth;
                    config.glyphCanvas.height = config.canvasHeight;
                    config.glyphCtx = config.glyphCanvas.getContext('2d');

                    config.maskCanvas = document.createElement('canvas');
                    config.maskCanvas.width = config.canvasWidth;
                    config.maskCanvas.height = config.canvasHeight;
                    config.maskCtx = config.maskCanvas.getContext('2d');

                    // Configure rendering contexts for quality
                    [config.ctx, config.glyphCtx, config.maskCtx].forEach(ctx => {{
                        ctx.imageSmoothingEnabled = true;
                        ctx.imageSmoothingQuality = 'high';
                        ctx.lineCap = 'round';
                        ctx.lineJoin = 'round';
                    }});

                    // Calculate nib size based on font size
                    config.nibRadius = config.fontSize * 0.04;

                    config.scrollContainer.scrollLeft = 0;
                }}

                // Prepare character paths using fluid continuous path system
                function prepareCharacterPaths() {{
                    const baseY = config.canvasHeight / 2 + config.fontSize / 4;

                    // Calculate total text width to center it
                    let totalTextWidth = 0;
                    for (let i = 0; i < config.text.length; i++) {{
                        const char = config.text[i];
                        if (char === ' ') {{
                            const spaceWidth = config.font ?
                                config.font.getAdvanceWidth(' ', config.fontSize) :
                                config.fontSize * 0.3;
                            totalTextWidth += spaceWidth;
                        }} else {{
                            const charWidth = config.font ?
                                config.font.getAdvanceWidth(char, config.fontSize) :
                                config.fontSize * 0.6;
                            totalTextWidth += charWidth;
                        }}
                    }}

                    // Calculate centered starting X position with some padding
                    const padding = 50;
                    const availableWidth = config.canvasWidth - (2 * padding);
                    const startX = padding + (availableWidth - totalTextWidth) / 2;
                    let currentX = Math.max(padding, startX);

                    config.characters = [];

                    // Clear and prepare glyph canvas
                    config.glyphCtx.fillStyle = 'white';
                    config.glyphCtx.fillRect(0, 0, config.canvasWidth, config.canvasHeight);

                    for (let i = 0; i < config.text.length; i++) {{
                        const char = config.text[i];

                        if (char === ' ') {{
                            const spaceWidth = config.font ?
                                config.font.getAdvanceWidth(' ', config.fontSize) :
                                config.fontSize * 0.3;
                            currentX += spaceWidth;
                            config.characters.push({{
                                char: ' ',
                                type: 'space',
                                x: currentX,
                                y: baseY,
                                width: spaceWidth,
                                points: []
                            }});
                            continue;
                        }}

                        // Render glyph to offscreen canvas
                        if (config.font) {{
                            config.glyphCtx.font = `${{config.fontSize}}px 'Noto Sans Ethiopic'`;
                        }} else {{
                            config.glyphCtx.font = `${{config.fontSize}}px 'Noto Sans Ethiopic', serif`;
                        }}
                        config.glyphCtx.fillStyle = config.inkColor;
                        config.glyphCtx.fillText(char, currentX, baseY);

                        // Generate continuous path for character
                        const continuousPath = generateContinuousPath(char, currentX, baseY);

                        config.characters.push({{
                            char: char,
                            type: 'character',
                            x: currentX,
                            y: baseY,
                            points: continuousPath
                        }});

                        // Advance to next character position
                        const charWidth = config.font ?
                            config.font.getAdvanceWidth(char, config.fontSize) :
                            config.fontSize * 0.7;
                        currentX += charWidth;
                    }}

                    updateStatus(`Prepared ${{config.characters.length}} characters - Animation will start soon...`);
                }}

                // Generate continuous path for a character (CORE FLUID ALGORITHM)
                function generateContinuousPath(char, offsetX, offsetY) {{
                    if (!config.font) {{
                        return generateFallbackPath(char, offsetX, offsetY);
                    }}

                    try {{
                        const fontPath = config.font.getPath(char, offsetX, offsetY, config.fontSize);
                        return convertToFluidPath(fontPath, offsetX, offsetY);
                    }} catch (error) {{
                        console.warn(`Error generating path for '${{char}}':`, error);
                        return generateFallbackPath(char, offsetX, offsetY);
                    }}
                }}

                // Convert OpenType path to fluid continuous path
                function convertToFluidPath(path, offsetX, offsetY) {{
                    const contours = extractPathContours(path);
                    if (contours.length === 0) return [];

                    const entryPoint = findOptimalEntryPoint(contours);
                    const fluidPath = createFluidContourPath(contours, entryPoint);
                    return resamplePath(fluidPath, config.stepSize);
                }}

                // Extract contours from OpenType path commands
                function extractPathContours(path) {{
                    const contours = [];
                    let currentContour = [];

                    for (const cmd of path.commands) {{
                        switch (cmd.type) {{
                            case 'M':
                                if (currentContour.length > 0) {{
                                    contours.push([...currentContour]);
                                }}
                                currentContour = [{{x: cmd.x, y: cmd.y}}];
                                break;

                            case 'L':
                                currentContour.push({{x: cmd.x, y: cmd.y}});
                                break;

                            case 'Q':
                                const qStart = currentContour[currentContour.length - 1];
                                const qCurve = sampleQuadraticBezier(qStart, {{x: cmd.x1, y: cmd.y1}}, {{x: cmd.x, y: cmd.y}}, 0.1);
                                currentContour.push(...qCurve.slice(1));
                                break;

                            case 'C':
                                const cStart = currentContour[currentContour.length - 1];
                                const cCurve = sampleCubicBezier(cStart, {{x: cmd.x1, y: cmd.y1}}, {{x: cmd.x2, y: cmd.y2}}, {{x: cmd.x, y: cmd.y}}, 0.1);
                                currentContour.push(...cCurve.slice(1));
                                break;

                            case 'Z':
                                if (currentContour.length > 0) {{
                                    contours.push([...currentContour]);
                                    currentContour = [];
                                }}
                                break;
                        }}
                    }}

                    if (currentContour.length > 0) {{
                        contours.push(currentContour);
                    }}

                    return contours;
                }}

                function sampleQuadraticBezier(p0, p1, p2, step) {{
                    const points = [];
                    for (let t = 0; t <= 1; t += step) {{
                        const x = Math.pow(1-t, 2) * p0.x + 2*(1-t)*t * p1.x + Math.pow(t, 2) * p2.x;
                        const y = Math.pow(1-t, 2) * p0.y + 2*(1-t)*t * p1.y + Math.pow(t, 2) * p2.y;
                        points.push({{x, y}});
                    }}
                    return points;
                }}

                function sampleCubicBezier(p0, p1, p2, p3, step) {{
                    const points = [];
                    for (let t = 0; t <= 1; t += step) {{
                        const x = Math.pow(1-t, 3) * p0.x + 3 * Math.pow(1-t, 2) * t * p1.x +
                                3 * (1-t) * Math.pow(t, 2) * p2.x + Math.pow(t, 3) * p3.x;
                        const y = Math.pow(1-t, 3) * p0.y + 3 * Math.pow(1-t, 2) * t * p1.y +
                                3 * (1-t) * Math.pow(t, 2) * p2.y + Math.pow(t, 3) * p3.y;
                        points.push({{x, y}});
                    }}
                    return points;
                }}

                function findOptimalEntryPoint(contours) {{
                    if (contours.length === 0) return null;

                    let leftmostPoint = null;
                    let minX = Infinity;

                    contours.forEach((contour, contourIndex) => {{
                        contour.forEach((point, pointIndex) => {{
                            if (point.x < minX) {{
                                minX = point.x;
                                leftmostPoint = {{contourIndex, pointIndex, point}};
                            }}
                        }});
                    }});

                    return leftmostPoint;
                }}

                function createFluidContourPath(contours, entryPoint) {{
                    if (!entryPoint || contours.length === 0) return [];

                    const fluidPath = [];
                    const processedContours = new Set();

                    const startContour = contours[entryPoint.contourIndex];
                    const reorderedStartContour = reorderContourFromPoint(startContour, entryPoint.pointIndex);
                    fluidPath.push(...reorderedStartContour);
                    processedContours.add(entryPoint.contourIndex);

                    while (processedContours.size < contours.length) {{
                        const lastPoint = fluidPath[fluidPath.length - 1];
                        let nearestContour = null;
                        let nearestDistance = Infinity;
                        let nearestStartIndex = 0;

                        contours.forEach((contour, index) => {{
                            if (processedContours.has(index)) return;

                            contour.forEach((point, pointIndex) => {{
                                const distance = Math.sqrt(
                                    Math.pow(point.x - lastPoint.x, 2) +
                                    Math.pow(point.y - lastPoint.y, 2)
                                );
                                if (distance < nearestDistance) {{
                                    nearestDistance = distance;
                                    nearestContour = index;
                                    nearestStartIndex = pointIndex;
                                }}
                            }});
                        }});

                        if (nearestContour !== null) {{
                            if (nearestDistance > config.stepSize * 2) {{
                                const connectPoint = contours[nearestContour][nearestStartIndex];
                                fluidPath.push(...interpolatePoints(lastPoint, connectPoint, config.stepSize));
                            }}

                            const nextContour = reorderContourFromPoint(contours[nearestContour], nearestStartIndex);
                            fluidPath.push(...nextContour);
                            processedContours.add(nearestContour);
                        }} else {{
                            break;
                        }}
                    }}

                    return fluidPath;
                }}

                function reorderContourFromPoint(contour, startIndex) {{
                    if (startIndex === 0) return [...contour];
                    return [...contour.slice(startIndex), ...contour.slice(0, startIndex)];
                }}

                function interpolatePoints(start, end, stepSize) {{
                    const points = [];
                    const distance = Math.sqrt(Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2));
                    const steps = Math.ceil(distance / stepSize);

                    for (let i = 1; i <= steps; i++) {{
                        const t = i / steps;
                        points.push({{
                            x: start.x + (end.x - start.x) * t,
                            y: start.y + (end.y - start.y) * t
                        }});
                    }}

                    return points;
                }}

                function resamplePath(path, stepSize) {{
                    if (path.length < 2) return path;

                    const resampled = [path[0]];
                    let currentDistance = 0;

                    for (let i = 1; i < path.length; i++) {{
                        const prev = path[i - 1];
                        const curr = path[i];
                        const segmentLength = Math.sqrt(
                            Math.pow(curr.x - prev.x, 2) + Math.pow(curr.y - prev.y, 2)
                        );

                        currentDistance += segmentLength;

                        while (currentDistance >= stepSize) {{
                            const t = (stepSize - (currentDistance - segmentLength)) / segmentLength;
                            const interpolated = {{
                                x: prev.x + (curr.x - prev.x) * t,
                                y: prev.y + (curr.y - prev.y) * t
                            }};
                            resampled.push(interpolated);
                            currentDistance -= stepSize;
                        }}
                    }}

                    if (path.length > 0) {{
                        resampled.push(path[path.length - 1]);
                    }}

                    return resampled;
                }}

                function generateFallbackPath(char, offsetX, offsetY) {{
                    const charWidth = config.fontSize * 0.6;
                    const charHeight = config.fontSize * 0.8;

                    return [
                        {{x: offsetX, y: offsetY - charHeight * 0.7}},
                        {{x: offsetX + charWidth, y: offsetY - charHeight * 0.7}},
                        {{x: offsetX + charWidth, y: offsetY}},
                        {{x: offsetX, y: offsetY}},
                        {{x: offsetX, y: offsetY - charHeight * 0.7}}
                    ];
                }}

                function paintNib(x, y, pressure = 1.0) {{
                    config.maskCtx.save();
                    config.maskCtx.translate(x, y);

                    const radius = config.nibRadius * pressure;

                    if (config.penStyle === "Brush") {{
                        const gradient = config.maskCtx.createRadialGradient(0, 0, 0, 0, 0, radius);
                        gradient.addColorStop(0, 'black');
                        gradient.addColorStop(0.7, 'rgba(0,0,0,0.8)');
                        gradient.addColorStop(1, 'rgba(0,0,0,0.3)');
                        config.maskCtx.fillStyle = gradient;
                    }} else {{
                        config.maskCtx.fillStyle = 'black';
                    }}

                    config.maskCtx.beginPath();
                    config.maskCtx.arc(0, 0, radius, 0, Math.PI * 2);
                    config.maskCtx.fill();

                    config.maskCtx.restore();
                }}

                function drawPen(x, y, angle = 0, pressure = 1.0) {{
                    const ctx = config.ctx;
                    ctx.save();
                    ctx.translate(x, y);
                    ctx.rotate(angle);

                    const scale = 0.8 + pressure * 0.4;
                    ctx.scale(scale, scale);

                    ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
                    ctx.fillRect(-4, 4, 8, 35);

                    const gradient = ctx.createLinearGradient(0, 0, 0, 30);
                    gradient.addColorStop(0, '#4169E1');
                    gradient.addColorStop(0.5, '#6495ED');
                    gradient.addColorStop(1, '#1E3A8A');
                    ctx.fillStyle = gradient;
                    ctx.fillRect(-3.5, 0, 7, 30);

                    ctx.fillStyle = '#696969';
                    ctx.fillRect(-4, 10, 8, 10);

                    ctx.fillStyle = '#000080';
                    ctx.beginPath();
                    ctx.arc(0, -2, 2.5, 0, Math.PI * 2);
                    ctx.fill();

                    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
                    ctx.fillRect(-1, 2, 2, 15);

                    ctx.restore();
                }}

                function scrollToPosition(x) {{
                    if (!config.scrollContainer) return;

                    const containerWidth = config.scrollContainer.clientWidth;
                    const scrollLeft = config.scrollContainer.scrollLeft;
                    const scrollRight = scrollLeft + containerWidth;
                    const padding = 120;

                    if (x < scrollLeft + padding) {{
                        config.scrollContainer.scrollLeft = Math.max(0, x - padding);
                    }} else if (x > scrollRight - padding) {{
                        config.scrollContainer.scrollLeft = x - containerWidth + padding;
                    }}
                }}

                function compositeFrame() {{
                    const ctx = config.ctx;

                    ctx.clearRect(0, 0, config.canvas.width, config.canvas.height);
                    ctx.fillStyle = 'white';
                    ctx.fillRect(0, 0, config.canvas.width, config.canvas.height);
                    ctx.drawImage(config.glyphCanvas, 0, 0);
                    ctx.globalCompositeOperation = 'destination-in';
                    ctx.drawImage(config.maskCanvas, 0, 0);
                    ctx.globalCompositeOperation = 'source-over';

                    if (config.isAnimating) {{
                        drawPen(config.penX, config.penY - 40, 0, config.penPressure);
                    }}
                }}

                function calculatePenPressure(speed, pointIndex, totalPoints) {{
                    let pressure = 1.0;

                    if (speed > 0) {{
                        pressure *= Math.max(0.5, 2.0 - speed / 10);
                    }}

                    const progress = pointIndex / totalPoints;
                    if (progress < 0.1) {{
                        pressure *= 0.7 + progress * 3;
                    }} else if (progress > 0.9) {{
                        pressure *= 0.7 + (1 - progress) * 3;
                    }}

                    pressure *= 0.9 + Math.random() * 0.2;

                    return Math.max(0.3, Math.min(1.5, pressure));
                }}

                function startAnimation() {{
                    if (config.isAnimating) return;

                    resetAnimationState();
                    config.isAnimating = true;

                    config.maskCtx.clearRect(0, 0, config.canvasWidth, config.canvasHeight);

                    updateStatus('Animation starting...');

                    config.lastFrameTime = performance.now();
                    animateNextFrame();
                }}

                function resetAnimationState() {{
                    config.currentCharIndex = 0;
                    config.currentPointIndex = 0;
                    config.penX = 0;
                    config.penY = 0;
                    config.penPressure = 1.0;
                    config.penSpeed = 0;
                    config.frameCount = 0;
                }}

                function animateNextFrame() {{
                    if (!config.isAnimating) return;

                    const currentTime = performance.now();
                    const deltaTime = currentTime - config.lastFrameTime;
                    config.lastFrameTime = currentTime;
                    config.frameCount++;

                    if (config.currentCharIndex >= config.characters.length) {{
                        completeAnimation();
                        return;
                    }}

                    const character = config.characters[config.currentCharIndex];

                    const totalPoints = config.characters.reduce((sum, char) => sum + char.points.length, 0);
                    const currentPoints = config.characters.slice(0, config.currentCharIndex).reduce((sum, char) => sum + char.points.length, 0) + config.currentPointIndex;
                    const progress = totalPoints > 0 ? (currentPoints / totalPoints) * 100 : 0;
                    document.getElementById('progressFill').style.width = progress + '%';

                    if (character.type === 'space') {{
                        config.penX = character.x;
                        config.penY = character.y;
                        scrollToPosition(config.penX);
                        compositeFrame();

                        setTimeout(() => {{
                            config.currentCharIndex++;
                            config.currentPointIndex = 0;
                            config.animationFrame = requestAnimationFrame(animateNextFrame);
                        }}, 200 / config.animationSpeed);
                        return;
                    }}

                    if (config.currentPointIndex >= character.points.length) {{
                        config.currentCharIndex++;
                        config.currentPointIndex = 0;
                        setTimeout(() => {{
                            config.animationFrame = requestAnimationFrame(animateNextFrame);
                        }}, 100 / config.animationSpeed);
                        return;
                    }}

                    const point = character.points[config.currentPointIndex];
                    if (!point) {{
                        config.currentPointIndex++;
                        config.animationFrame = requestAnimationFrame(animateNextFrame);
                        return;
                    }}

                    if (config.currentPointIndex > 0) {{
                        const prevPoint = character.points[config.currentPointIndex - 1];
                        config.penSpeed = Math.sqrt(
                            Math.pow(point.x - prevPoint.x, 2) +
                            Math.pow(point.y - prevPoint.y, 2)
                        );
                    }}

                    config.penX = point.x;
                    config.penY = point.y;
                    config.penPressure = calculatePenPressure(config.penSpeed, config.currentPointIndex, character.points.length);

                    paintNib(config.penX, config.penY, config.penPressure);

                    compositeFrame();
                    scrollToPosition(config.penX);

                    config.currentPointIndex++;

                    const baseDelay = 20;
                    const speedAdjustedDelay = Math.max(5, baseDelay / config.animationSpeed);

                    setTimeout(() => {{
                        config.animationFrame = requestAnimationFrame(animateNextFrame);
                    }}, speedAdjustedDelay);
                }}

                function completeAnimation() {{
                    config.isAnimating = false;

                    document.getElementById('progressFill').style.width = '100%';

                    updateStatus(`Animation complete! (${{config.frameCount}} frames rendered)`);

                    config.ctx.clearRect(0, 0, config.canvas.width, config.canvas.height);
                    config.ctx.fillStyle = 'white';
                    config.ctx.fillRect(0, 0, config.canvas.width, config.canvas.height);
                    config.ctx.drawImage(config.glyphCanvas, 0, 0);
                    config.ctx.globalCompositeOperation = 'destination-in';
                    config.ctx.drawImage(config.maskCanvas, 0, 0);
                    config.ctx.globalCompositeOperation = 'source-over';
                }}

                function updateStatus(message) {{
                    document.getElementById('status').textContent = message;
                }}
            </script>
        </body>
        </html>
    """
    return html_content


def render():
    """Enhanced alphabets page with automatic handwriting animation - exact replica of interface_reference.py"""
    st.subheader("ፊደላት (Tigrinya Alphabets)")

    # Initialize session state for selected character and animation character
    if "selected_character" not in st.session_state:
        st.session_state.selected_character = None
    if "animation_character" not in st.session_state:
        st.session_state.animation_character = None

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
                        use_container_width=True,
                    ):
                        st.session_state.selected_character = alphabet_key
                        st.session_state.animation_character = alphabet_key
                        st.rerun()

    # Display selected character details and animation
    if st.session_state.selected_character:
        selected_char = st.session_state.selected_character
        char_data = TIGRINYA_ALPHABETS[selected_char]

        st.markdown("---")

        # Character information
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(
                f"""
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
            """,
                unsafe_allow_html=True,
            )

            # Character forms table
            st.markdown("#### All Forms:")
            forms_df = []
            for i, (form, phonetic) in enumerate(
                zip(char_data["forms"], char_data["phonetic"])
            ):
                forms_df.append({"Form": form, "Sound": phonetic, "Order": i + 1})

            df = pd.DataFrame(forms_df)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Related characters or similar forms - Click to animate on same canvas
            st.markdown("#### Related Forms - Click to animate")
            related_forms = char_data["forms"]
            related_phonetics = char_data["phonetic"]

            # Display related forms as buttons in a 2x2 grid
            for i in range(0, len(related_forms), 2):
                form_cols = st.columns(2)

                # First form in the row
                with form_cols[0]:
                    form = related_forms[i]
                    phonetic = related_phonetics[i]
                    if st.button(
                        f"{form}",
                        key=f"related_{form}_{selected_char}_{i}",
                        help=f"Animate {form} ({phonetic})",
                        use_container_width=True,
                    ):
                        # Set this form to be animated on main canvas
                        st.session_state.animation_character = form
                        st.rerun()

                # Second form in the row (if exists)
                if i + 1 < len(related_forms):
                    with form_cols[1]:
                        form = related_forms[i + 1]
                        phonetic = related_phonetics[i + 1]
                        if st.button(
                            f"{form}",
                            key=f"related_{form}_{selected_char}_{i + 1}",
                            help=f"Animate {form} ({phonetic})",
                            use_container_width=True,
                        ):
                            # Set this form to be animated on main canvas
                            st.session_state.animation_character = form
                            st.rerun()

        with col2:
            # Main handwriting animation canvas
            st.markdown("#### Handwriting Animation")

            # Show what character is being animated
            character_to_animate = st.session_state.get(
                "animation_character", selected_char
            )

            if (
                st.session_state.get("animation_character")
                and st.session_state.animation_character != selected_char
            ):
                st.info(f"Now animating: {st.session_state.animation_character}")
            else:
                st.info("Animation starting automatically...")

            # Generate and display handwriting animation that auto-starts
            animation_html = create_auto_start_handwriting_html(
                text=character_to_animate,
                pen_style="Realistic",
                writing_style="Natural",
                animation_speed=4.0,
            )

            # Use st.empty() to ensure proper refresh
            animation_placeholder = st.empty()
            with animation_placeholder.container():
                components.html(animation_html, height=600, scrolling=True)

            # Character practice section
            st.markdown("#### Practice Writing")
            st.info("Try writing this character on paper while watching the animation!")

    else:
        st.info(
            "Select a character above to see its automatic handwriting animation and details!"
        )

    # Traditional alphabet table for reference
    st.markdown("---")
    st.markdown("### Traditional Alphabet Reference")

    # Show traditional grid format using our data
    sample_alphabets = [
        ["በ (be)", "ቡ (bu)", "ቢ (bi)", "ባ (ba)", "ቤ (bie)", "ብ (b)", "ቦ (bo)"],
        ["ከ (ke)", "ኩ (ku)", "ኪ (ki)", "ካ (ka)", "ኬ (kie)", "ክ (k)", "ኮ (ko)"],
        ["ሰ (se)", "ሱ (su)", "ሲ (si)", "ሳ (sa)", "ሴ (sie)", "ስ (s)", "ሶ (so)"],
        ["ሸ (Se)", "ሹ (Su)", "ሺ (Si)", "ሻ (Sa)", "ሼ (Sie)", "ሽ (S)", "ሾ (So)"],
    ]

    table_header = """
| 1st Order | 2nd Order | 3rd Order | 4th Order | 5th Order | 6th Order | 7th Order |
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
"""

    table_rows = ""
    for row in sample_alphabets:
        table_rows += f"| {' | '.join(row)} |\n"

    st.markdown(table_header + table_rows, unsafe_allow_html=True)


if __name__ == "__main__":
    render()
