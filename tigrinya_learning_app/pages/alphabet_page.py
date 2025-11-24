"""
Alphabet page module - Enhanced with auto-starting handwriting animations
Replicates the exact flow from interface_reference.py for proper character animation
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
    text, pen_style="Realistic", writing_style="Natural", animation_speed=4.0
):
    """
    Create HTML5 Canvas-based fluid handwriting animation with auto-start
    Exact copy from interface_reference.py
    """
    import json

    safe_text = json.dumps(text)

    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Fluid Handwriting Animation</title>
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

                .progress-bar {{
                    width: 100%;
                    height: 8px;
                    background: #ecf0f1;
                    border-radius: 4px;
                    overflow: hidden;
                    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
                    margin: 20px 0;
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

                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="status" id="status">Loading font and preparing animation...</div>
            </div>

            <script>
                const config = {{
                    text: {safe_text},
                    penStyle: "{pen_style}",
                    animationSpeed: {animation_speed},
                    canvas: null,
                    ctx: null,
                    glyphCanvas: null,
                    glyphCtx: null,
                    maskCanvas: null,
                    maskCtx: null,
                    isAnimating: false,
                    currentCharIndex: 0,
                    currentPointIndex: 0,
                    font: null,
                    fontSize: 120,
                    characters: [],
                    scrollContainer: null,
                    canvasWidth: 2400,
                    canvasHeight: 400,
                    nibRadius: 0,
                    inkColor: '#2c3e50',
                    penX: 0,
                    penY: 0,
                    penPressure: 1.0,
                    animationFrame: null,
                    lastFrameTime: 0,
                    frameCount: 0
                }};

                // Load font and auto-start animation
                opentype.load('https://fonts.gstatic.com/s/notosansethiopic/v49/7cHPv50vjIepfJVOZZgcpQ5B9FBTH9KGNfhSTgtoow1KVnIvyBoMSzUMacb-T35OK6Dj.ttf', function (err, font) {{
                    if (err) {{
                        console.error('Font loading error:', err);
                        document.getElementById('status').textContent = 'Using fallback font - Starting animation...';
                        initWithoutFont();
                        setTimeout(startAnimation, 800);
                    }} else {{
                        config.font = font;
                        document.getElementById('status').textContent = 'Font loaded - Starting animation...';
                        initCanvas();
                        prepareCharacterPaths();
                        setTimeout(startAnimation, 500);
                    }}
                }});

                function initWithoutFont() {{
                    config.font = null;
                    initCanvas();
                    prepareCharacterPaths();
                }}

                function initCanvas() {{
                    config.canvas = document.getElementById('animationCanvas');
                    config.scrollContainer = document.getElementById('scrollContainer');

                    const textLength = config.text.length;
                    const estimatedWidth = Math.max(900, textLength * 130);
                    config.canvasWidth = estimatedWidth;
                    config.canvas.width = config.canvasWidth;
                    config.canvas.height = config.canvasHeight;
                    config.ctx = config.canvas.getContext('2d');

                    config.glyphCanvas = document.createElement('canvas');
                    config.glyphCanvas.width = config.canvasWidth;
                    config.glyphCanvas.height = config.canvasHeight;
                    config.glyphCtx = config.glyphCanvas.getContext('2d');

                    config.maskCanvas = document.createElement('canvas');
                    config.maskCanvas.width = config.canvasWidth;
                    config.maskCanvas.height = config.canvasHeight;
                    config.maskCtx = config.maskCanvas.getContext('2d');

                    [config.ctx, config.glyphCtx, config.maskCtx].forEach(ctx => {{
                        ctx.imageSmoothingEnabled = true;
                        ctx.imageSmoothingQuality = 'high';
                        ctx.lineCap = 'round';
                        ctx.lineJoin = 'round';
                    }});

                    config.nibRadius = config.fontSize * 0.04;
                    config.scrollContainer.scrollLeft = 0;
                }}

                function prepareCharacterPaths() {{
                    const baseY = config.canvasHeight / 2 + config.fontSize / 4;
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

                    const padding = 50;
                    const availableWidth = config.canvasWidth - (2 * padding);
                    const startX = padding + (availableWidth - totalTextWidth) / 2;
                    let currentX = Math.max(padding, startX);

                    config.characters = [];
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
                                points: []
                            }});
                            continue;
                        }}

                        if (config.font) {{
                            config.glyphCtx.font = `${{config.fontSize}}px 'Noto Sans Ethiopic'`;
                        }} else {{
                            config.glyphCtx.font = `${{config.fontSize}}px 'Noto Sans Ethiopic', serif`;
                        }}
                        config.glyphCtx.fillStyle = config.inkColor;
                        config.glyphCtx.fillText(char, currentX, baseY);

                        const continuousPath = generateContinuousPath(char, currentX, baseY);

                        config.characters.push({{
                            char: char,
                            type: 'character',
                            x: currentX,
                            y: baseY,
                            points: continuousPath
                        }});

                        const charWidth = config.font ?
                            config.font.getAdvanceWidth(char, config.fontSize) :
                            config.fontSize * 0.7;
                        currentX += charWidth;
                    }}

                    updateStatus(`Prepared ${{config.characters.length}} characters - Starting animation...`);
                }}

                function generateContinuousPath(char, offsetX, offsetY) {{
                    if (!config.font) {{
                        return generateFallbackPath(char, offsetX, offsetY);
                    }}

                    try {{
                        const fontPath = config.font.getPath(char, offsetX, offsetY, config.fontSize);
                        return convertToFluidPath(fontPath);
                    }} catch (error) {{
                        return generateFallbackPath(char, offsetX, offsetY);
                    }}
                }}

                function convertToFluidPath(path) {{
                    const points = [];
                    let currentPoint = null;

                    for (const cmd of path.commands) {{
                        switch (cmd.type) {{
                            case 'M':
                                currentPoint = {{x: cmd.x, y: cmd.y}};
                                points.push(currentPoint);
                                break;
                            case 'L':
                                points.push({{x: cmd.x, y: cmd.y}});
                                break;
                            case 'Q':
                                if (currentPoint) {{
                                    for (let t = 0.1; t <= 1; t += 0.1) {{
                                        const x = Math.pow(1-t, 2) * currentPoint.x + 2*(1-t)*t * cmd.x1 + Math.pow(t, 2) * cmd.x;
                                        const y = Math.pow(1-t, 2) * currentPoint.y + 2*(1-t)*t * cmd.y1 + Math.pow(t, 2) * cmd.y;
                                        points.push({{x, y}});
                                    }}
                                    currentPoint = {{x: cmd.x, y: cmd.y}};
                                }}
                                break;
                            case 'C':
                                if (currentPoint) {{
                                    for (let t = 0.1; t <= 1; t += 0.1) {{
                                        const x = Math.pow(1-t, 3) * currentPoint.x + 3 * Math.pow(1-t, 2) * t * cmd.x1 +
                                                3 * (1-t) * Math.pow(t, 2) * cmd.x2 + Math.pow(t, 3) * cmd.x;
                                        const y = Math.pow(1-t, 3) * currentPoint.y + 3 * Math.pow(1-t, 2) * t * cmd.y1 +
                                                3 * (1-t) * Math.pow(t, 2) * cmd.y2 + Math.pow(t, 3) * cmd.y;
                                        points.push({{x, y}});
                                    }}
                                    currentPoint = {{x: cmd.x, y: cmd.y}};
                                }}
                                break;
                        }}
                    }}

                    return points;
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
                    config.maskCtx.fillStyle = 'black';
                    config.maskCtx.beginPath();
                    config.maskCtx.arc(0, 0, radius, 0, Math.PI * 2);
                    config.maskCtx.fill();

                    config.maskCtx.restore();
                }}

                function drawPen(x, y, pressure = 1.0) {{
                    const ctx = config.ctx;
                    ctx.save();
                    ctx.translate(x, y);

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
                        drawPen(config.penX, config.penY - 40, config.penPressure);
                    }}
                }}

                function startAnimation() {{
                    if (config.isAnimating) return;

                    config.currentCharIndex = 0;
                    config.currentPointIndex = 0;
                    config.isAnimating = true;

                    config.maskCtx.clearRect(0, 0, config.canvasWidth, config.canvasHeight);
                    updateStatus('Animating...');

                    animateNextFrame();
                }}

                function animateNextFrame() {{
                    if (!config.isAnimating) return;

                    if (config.currentCharIndex >= config.characters.length) {{
                        config.isAnimating = false;
                        document.getElementById('progressFill').style.width = '100%';
                        updateStatus('Animation complete!');
                        compositeFrame();
                        return;
                    }}

                    const character = config.characters[config.currentCharIndex];

                    // Update progress
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
                            animateNextFrame();
                        }}, 200 / config.animationSpeed);
                        return;
                    }}

                    if (config.currentPointIndex >= character.points.length) {{
                        config.currentCharIndex++;
                        config.currentPointIndex = 0;
                        setTimeout(() => {{
                            animateNextFrame();
                        }}, 100 / config.animationSpeed);
                        return;
                    }}

                    const point = character.points[config.currentPointIndex];
                    if (!point) {{
                        config.currentPointIndex++;
                        animateNextFrame();
                        return;
                    }}

                    config.penX = point.x;
                    config.penY = point.y;
                    config.penPressure = 0.8 + Math.random() * 0.4;

                    paintNib(config.penX, config.penY, config.penPressure);
                    compositeFrame();
                    scrollToPosition(config.penX);

                    config.currentPointIndex++;

                    const delay = Math.max(5, 20 / config.animationSpeed);
                    setTimeout(() => {{
                        animateNextFrame();
                    }}, delay);
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
