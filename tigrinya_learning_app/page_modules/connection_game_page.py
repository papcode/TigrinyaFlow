"""
Connection Game Page - HTML Canvas Game for Image-Text Matching
"""

import streamlit as st
import streamlit.components.v1 as components
from utils.connection_game import ConnectionGame


def create_connection_game_html(puzzle_data: dict, game_id: str) -> str:
    """Create the HTML content for the connection game"""

    images_html = ""
    texts_html = ""

    # Generate images HTML
    for img_data in puzzle_data["images"]:
        if img_data["image_base64"]:
            images_html += f"""
            <div class="image-item" id="{img_data["id"]}" onclick="selectImage('{img_data["id"]}')">
                <img src="data:image/jpeg;base64,{img_data["image_base64"]}" alt="{img_data["english"]}" />
                <div class="image-label">{img_data["english"].title()}</div>
            </div>
            """

    # Generate texts HTML
    for text_data in puzzle_data["texts"]:
        texts_html += f"""
        <div class="text-item" id="{text_data["id"]}" onclick="selectText('{text_data["id"]}')">
            <div class="tigrinya-text">{text_data["tigrinya"]}</div>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Connection Game</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}

            .game-container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}

            .game-header {{
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                padding: 20px;
                text-align: center;
            }}

            .game-header h1 {{
                margin: 0;
                font-size: 2.5em;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}

            .game-info {{
                background: #f8f9fa;
                padding: 15px;
                text-align: center;
                border-bottom: 2px solid #e9ecef;
            }}

            .score-display {{
                font-size: 1.2em;
                font-weight: bold;
                color: #495057;
            }}

            .game-board {{
                display: grid;
                grid-template-columns: 1fr auto 1fr;
                gap: 20px;
                padding: 30px;
                min-height: {max(600, len(puzzle_data["images"]) * 150)}px;
                position: relative;
            }}

            .images-column, .texts-column {{
                display: flex;
                flex-direction: column;
                gap: 20px;
                justify-content: flex-start;
                padding: 20px 0;
            }}

            .image-item {{
                background: white;
                border: 3px solid #dee2e6;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                min-height: 140px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                margin: 10px 0;
            }}

            .image-item:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            }}

            .image-item.selected {{
                border-color: #007bff;
                background: #e3f2fd;
                box-shadow: 0 0 20px rgba(0,123,255,0.5);
            }}

            .image-item.connected {{
                border-color: #28a745;
                background: #d4edda;
            }}

            .image-item.correct {{
                border-color: #28a745;
                background: #d4edda;
                animation: correctPulse 1s ease-in-out;
            }}

            .image-item.incorrect {{
                border-color: #dc3545;
                background: #f8d7da;
                animation: incorrectShake 0.5s ease-in-out;
            }}

            .image-item img {{
                max-width: 140px;
                max-height: 180px;
                object-fit: contain;
                border-radius: 10px;
            }}

            .image-label {{
                margin-top: 10px;
                font-weight: bold;
                color: #495057;
                font-size: 0.9em;
            }}

            .text-item {{
                background: white;
                border: 3px solid #dee2e6;
                border-radius: 15px;
                padding: 20px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                min-height: 100px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 10px 0;
            }}

            .text-item:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            }}

            .text-item.selected {{
                border-color: #007bff;
                background: #e3f2fd;
                box-shadow: 0 0 20px rgba(0,123,255,0.5);
            }}

            .text-item.connected {{
                border-color: #6c757d;
                background: #e9ecef;
                cursor: not-allowed;
            }}

            .text-item.correct {{
                border-color: #28a745;
                background: #d4edda;
                animation: correctPulse 1s ease-in-out;
            }}

            .text-item.incorrect {{
                border-color: #dc3545;
                background: #f8d7da;
                animation: incorrectShake 0.5s ease-in-out;
            }}

            .tigrinya-text {{
                font-size: 1.8em;
                font-weight: bold;
                color: #495057;
                font-family: 'Noto Sans Ethiopic', serif;
            }}

            .canvas-container {{
                position: relative;
                width: 250px;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: {max(600, len(puzzle_data["images"]) * 150)}px;
            }}

            #connectionCanvas {{
                position: absolute;
                top: 0;
                left: 0;
                pointer-events: none;
                z-index: 1;
            }}

            .controls {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                border-top: 2px solid #e9ecef;
            }}

            .btn {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 25px;
                font-size: 1.1em;
                font-weight: bold;
                cursor: pointer;
                margin: 0 10px;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}

            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            }}

            .btn:active {{
                transform: translateY(0);
            }}

            .btn-success {{
                background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
            }}

            .btn-danger {{
                background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
            }}

            .btn-warning {{
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            }}

            .feedback {{
                margin-top: 20px;
                padding: 15px;
                border-radius: 10px;
                font-weight: bold;
                text-align: center;
            }}

            .feedback.success {{
                background: #d4edda;
                color: #155724;
                border: 2px solid #28a745;
            }}

            .feedback.partial {{
                background: #fff3cd;
                color: #856404;
                border: 2px solid #ffc107;
            }}

            .feedback.error {{
                background: #f8d7da;
                color: #721c24;
                border: 2px solid #dc3545;
            }}

            @keyframes correctPulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}

            @keyframes incorrectShake {{
                0%, 100% {{ transform: translateX(0); }}
                25% {{ transform: translateX(-5px); }}
                75% {{ transform: translateX(5px); }}
            }}

            .instructions {{
                background: #e7f3ff;
                border: 2px solid #2196f3;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
            }}

            .instructions h3 {{
                margin: 0 0 10px 0;
                color: #1565c0;
            }}

            .instructions ol {{
                margin: 0;
                padding-left: 20px;
            }}

            .instructions li {{
                margin: 5px 0;
                color: #333;
            }}

            @media (max-width: 768px) {{
                .game-board {{
                    grid-template-columns: 1fr;
                    gap: 30px;
                }}

                .canvas-container {{
                    width: 100%;
                    min-height: {max(400, len(puzzle_data["images"]) * 140)}px;
                }}

                .tigrinya-text {{
                    font-size: 1.5em;
                }}

                .images-column, .texts-column {{
                    gap: 25px;
                    padding: 15px 0;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="game-container">
            <div class="game-header">
                <h1>🔗 Match the Following</h1>
                <p>Connect images with their Tigrinya names!</p>
            </div>

            <div class="game-info">
                <div class="score-display">
                    Exercise #{puzzle_data.get("current_round", 1)} |
                    Correct: <span id="score">0</span> / <span id="total">{len(puzzle_data["images"])}</span>
                    | Matched: <span id="connections">0</span> / <span id="totalConnections">{len(puzzle_data["images"])}</span>
                </div>
            </div>

            <div class="instructions">
                <h3>📋 Instructions:</h3>
                <ol>
                    <li>Click on an image to select it (it will glow blue)</li>
                    <li>Click on a Tigrinya text label to connect them</li>
                    <li>A line will appear connecting the matched pair</li>
                    <li>Click "Check Answers" when you've made all connections</li>
                    <li>Green = correct, Red = incorrect matches</li>
                </ol>
            </div>

            <div class="game-board">
                <div class="images-column">
                    {images_html}
                </div>

                <div class="canvas-container">
                    <canvas id="connectionCanvas" width="250" height="{max(600, len(puzzle_data["images"]) * 150)}"></canvas>
                </div>

                <div class="texts-column">
                    {texts_html}
                </div>
            </div>

            <div class="controls">
                <button class="btn btn-success" onclick="checkAnswers()">✓ Check Answers</button>
                <button class="btn btn-danger" onclick="resetGame()">🔄 Reset Connections</button>
                <div id="feedback"></div>
                <div style="margin-top: 10px; text-align: center; color: #666; font-size: 0.9em;">
                    💡 To practice with different vocabulary items, click "Start New Exercise" above
                </div>
            </div>
        </div>

        <script>
            // Game state
            let connections = {{}};
            let selectedImage = null;
            let selectedText = null;
            let gameComplete = false;
            let correctAnswers = {puzzle_data["correct_answers"]};

            // Canvas setup
            const canvas = document.getElementById('connectionCanvas');
            const ctx = canvas.getContext('2d');

            // Adjust canvas size to container
            function resizeCanvas() {{
                const container = canvas.parentElement;
                const containerRect = container.getBoundingClientRect();
                canvas.width = containerRect.width;
                canvas.height = containerRect.height;
                // Ensure minimum size for visibility
                if (canvas.width < 250) canvas.width = 250;
                if (canvas.height < 600) canvas.height = 600;
                drawConnections();
            }}

            window.addEventListener('resize', resizeCanvas);
            // Initialize canvas when DOM is loaded
            function initializeCanvas() {{
                // Wait for layout to stabilize
                setTimeout(() => {{
                    resizeCanvas();
                    // Additional resize after a short delay to ensure all elements are positioned
                    setTimeout(resizeCanvas, 200);
                }}, 100);
            }}

            // Initialize on load
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', initializeCanvas);
            }} else {{
                initializeCanvas();
            }}

            function selectImage(imageId) {{
                if (gameComplete) return;

                // Clear previous selection
                if (selectedImage) {{
                    document.getElementById(selectedImage).classList.remove('selected');
                }}

                // If clicking the same image, deselect it
                if (selectedImage === imageId) {{
                    selectedImage = null;
                    return;
                }}

                // Select new image
                selectedImage = imageId;
                document.getElementById(imageId).classList.add('selected');

                // Clear text selection
                if (selectedText) {{
                    document.getElementById(selectedText).classList.remove('selected');
                    selectedText = null;
                }}
            }}

            function selectText(textId) {{
                if (gameComplete) return;

                // Don't allow selection of already connected text
                if (Object.values(connections).includes(textId)) {{
                    return;
                }}

                // If we have a selected image, make connection
                if (selectedImage) {{
                    makeConnection(selectedImage, textId);
                    return;
                }}

                // Clear previous text selection
                if (selectedText) {{
                    document.getElementById(selectedText).classList.remove('selected');
                }}

                // If clicking the same text, deselect it
                if (selectedText === textId) {{
                    selectedText = null;
                    return;
                }}

                // Select new text
                selectedText = textId;
                document.getElementById(textId).classList.add('selected');
            }}

            function makeConnection(imageId, textId) {{
                // Remove any existing connection for this image
                if (connections[imageId]) {{
                    const oldTextId = connections[imageId];
                    document.getElementById(oldTextId).classList.remove('connected');
                }}

                // Create new connection
                connections[imageId] = textId;

                // Update UI
                document.getElementById(imageId).classList.remove('selected');
                document.getElementById(imageId).classList.add('connected');
                document.getElementById(textId).classList.add('connected');

                // Clear selections
                selectedImage = null;
                selectedText = null;

                // Update counters
                updateCounters();

                // Redraw connections
                drawConnections();
            }}

            function drawConnections() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                const gameBoard = document.querySelector('.game-board');
                const imagesColumn = document.querySelector('.images-column');
                const textsColumn = document.querySelector('.texts-column');

                Object.entries(connections).forEach(([imageId, textId]) => {{
                    const imageElement = document.getElementById(imageId);
                    const textElement = document.getElementById(textId);

                    if (imageElement && textElement) {{
                        const imageRect = imageElement.getBoundingClientRect();
                        const textRect = textElement.getBoundingClientRect();
                        const canvasRect = canvas.getBoundingClientRect();

                        // Calculate relative positions with better positioning
                        const startX = 10;
                        const startY = Math.max(0, Math.min(canvas.height, imageRect.top + imageRect.height / 2 - canvasRect.top));
                        const endX = canvas.width - 10;
                        const endY = Math.max(0, Math.min(canvas.height, textRect.top + textRect.height / 2 - canvasRect.top));

                        // Set line style
                        ctx.strokeStyle = imageElement.classList.contains('correct') ? '#28a745' :
                                         imageElement.classList.contains('incorrect') ? '#dc3545' :
                                         '#007bff';
                        ctx.lineWidth = 4;
                        ctx.lineCap = 'round';

                        // Draw connection line with curve
                        ctx.beginPath();
                        ctx.moveTo(startX, startY);

                        // Create a smooth curved line
                        const controlX1 = canvas.width * 0.3;
                        const controlX2 = canvas.width * 0.7;
                        const controlY = (startY + endY) / 2;
                        ctx.bezierCurveTo(controlX1, startY, controlX2, endY, endX, endY);

                        ctx.stroke();

                        // Draw connection points
                        ctx.fillStyle = ctx.strokeStyle;
                        ctx.beginPath();
                        ctx.arc(startX, startY, 6, 0, 2 * Math.PI);
                        ctx.fill();
                        ctx.beginPath();
                        ctx.arc(endX, endY, 6, 0, 2 * Math.PI);
                        ctx.fill();
                    }}
                }});
            }}

            function updateCounters() {{
                document.getElementById('connections').textContent = Object.keys(connections).length;
            }}

            function checkAnswers() {{
                const totalQuestions = {len(puzzle_data["images"])};
                const totalConnections = Object.keys(connections).length;

                if (totalConnections < totalQuestions) {{
                    showFeedback('Please connect all images before checking answers!', 'error');
                    return;
                }}

                let correctCount = 0;

                // Check each connection
                Object.entries(connections).forEach(([imageId, textId]) => {{
                    const isCorrect = correctAnswers[imageId] === textId;
                    const imageElement = document.getElementById(imageId);
                    const textElement = document.getElementById(textId);

                    if (isCorrect) {{
                        imageElement.classList.add('correct');
                        textElement.classList.add('correct');
                        correctCount++;
                    }} else {{
                        imageElement.classList.add('incorrect');
                        textElement.classList.add('incorrect');
                    }}
                }});

                // Update score display
                document.getElementById('score').textContent = correctCount;

                // Show feedback
                if (correctCount === totalQuestions) {{
                    showFeedback('🎉 Perfect! All connections are correct!', 'success');
                    gameComplete = true;
                }} else if (correctCount > totalQuestions / 2) {{
                    showFeedback(`Good job! You got ${{correctCount}} out of ${{totalQuestions}} correct.`, 'partial');
                }} else {{
                    showFeedback(`Keep trying! You got ${{correctCount}} out of ${{totalQuestions}} correct.`, 'error');
                }}

                // Redraw connections with updated colors
                drawConnections();
            }}

            function resetGame() {{
                // Clear connections
                connections = {{}};
                selectedImage = null;
                selectedText = null;
                gameComplete = false;

                // Reset UI
                document.querySelectorAll('.image-item, .text-item').forEach(element => {{
                    element.classList.remove('selected', 'connected', 'correct', 'incorrect');
                }});

                // Update counters
                document.getElementById('score').textContent = '0';
                updateCounters();

                // Clear canvas and feedback
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                document.getElementById('feedback').innerHTML = '';
            }}



            function showFeedback(message, type) {{
                const feedbackDiv = document.getElementById('feedback');
                feedbackDiv.innerHTML = `<div class="feedback ${{type}}">${{message}}</div>`;

                setTimeout(() => {{
                    if (type !== 'error') {{
                        feedbackDiv.innerHTML = '';
                    }}
                }}, 3000);
            }}

            // Initialize counters and canvas
            updateCounters();

            // Final canvas initialization
            setTimeout(() => {{
                resizeCanvas();
            }}, 300);
        </script>
    </body>
    </html>
    """

    return html_content


def render():
    """Main matching exercise page"""
    st.subheader("🔗 Match the Following")
    st.markdown("*Connect images with their corresponding Tigrinya text labels*")

    # Game controls
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        # Category selection
        game = ConnectionGame()
        categories = game.get_available_categories()
        selected_category = st.selectbox(
            "Choose Category:",
            categories,
            format_func=lambda x: x.replace("_", " ").title(),
        )

    with col2:
        # Number of items
        num_items = st.selectbox(
            "Number of Items:",
            [3, 4, 5, 6],
            index=2,  # default to 5
        )

    with col3:
        # New exercise button
        current_round = st.session_state.connection_game_state.get("current_round", 1)
        if st.button(f"📝 Start New Exercise (#{current_round + 1})", type="primary"):
            # Force new puzzle generation and increment round
            st.session_state.connection_game_state["force_new_puzzle"] = True
            game.increment_round()
            game.reset_exercise()
            st.success(
                f"✅ New exercise #{current_round + 1} generated with different items!"
            )
            st.rerun()

    # Exercise info
    st.info(
        """
        🎯 **Instructions:**
        - Click on an image to select it (highlighted in blue)
        - Click on a Tigrinya text label to create a connection
        - A colorful line will connect the matched pair
        - Click 'Check Answers' when all connections are made
        - Green lines = correct matches, Red lines = incorrect matches
        - Use 'Reset' button below to clear connections
        - Use 'Start New Exercise' above to get different vocabulary items
        """
    )

    # Generate and display the exercise
    try:
        # Create a key to track current exercise settings
        current_key = f"{selected_category}_{num_items}"

        # Check if we need to generate a new puzzle
        should_generate_new = (
            game.should_generate_new_puzzle()
            or "current_puzzle" not in st.session_state
            or "current_puzzle_key" not in st.session_state
            or st.session_state.current_puzzle_key != current_key
        )

        if should_generate_new:
            puzzle = game.generate_puzzle(selected_category, num_items)
            # Add current round info to puzzle data for display
            puzzle["current_round"] = st.session_state.connection_game_state.get(
                "current_round", 1
            )
            st.session_state.current_puzzle = puzzle
            st.session_state.current_puzzle_key = current_key
            # Reset the force flag after generating new puzzle
            st.session_state.connection_game_state["force_new_puzzle"] = False
        else:
            puzzle = st.session_state.current_puzzle
            # Update round info in existing puzzle
            puzzle["current_round"] = st.session_state.connection_game_state.get(
                "current_round", 1
            )

        if puzzle["images"]:  # Only show exercise if we have images
            html_content = create_connection_game_html(puzzle, "connection_exercise")
            # Calculate dynamic height based on number of items
            dynamic_height = max(1000, 700 + num_items * 150)
            components.html(html_content, height=dynamic_height, scrolling=True)
        else:
            st.error(
                f"No images found for category '{selected_category}'. Please try another category."
            )
    except Exception as e:
        st.error(f"Error loading exercise: {str(e)}")
        st.info("Please check that image files exist in the vocabulary folder.")

    # Statistics and learning info
    st.markdown("---")

    with st.expander("📊 Exercise Statistics & Learning Tips"):
        stats = game.get_statistics()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Current Score", f"{stats['current_score']}/{stats['total_questions']}"
            )
        with col2:
            st.metric("Exercise", stats["current_round"])
        with col3:
            if stats["exercise_complete"]:
                st.success("✅ Exercise Complete!")
            else:
                st.info("📝 Exercise in Progress")

        st.markdown("""
        ### 🎓 Learning Benefits:
        - **Visual Association**: Connect images with Tigrinya text to build visual memory
        - **Pattern Recognition**: Learn to recognize Tigrinya script characters
        - **Category Learning**: Focus on specific vocabulary categories
        - **Interactive Learning**: Engaging exercises make learning more effective

        ### 💡 Tips for Success:
        - Study the Tigrinya text carefully before making connections
        - Use process of elimination for difficult matches
        - Try different categories to expand your vocabulary
        - Practice regularly to improve recognition speed
        """)
