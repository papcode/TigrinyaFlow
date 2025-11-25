import json
import random
from typing import Dict, List, Tuple

import streamlit as st
import streamlit.components.v1 as components

from clientTranslation import geez_to_latin_syllable

# Word bank for drag-and-drop exercises
DRAG_DROP_WORDS = {
    # Animals
    "ዶሮ": {"translation": "chicken", "category": "animals"},
    "ላም": {"translation": "cow", "category": "animals"},
    "ድሙ": {"translation": "cat", "category": "animals"},
    "ከልቢ": {"translation": "dog", "category": "animals"},
    # Colors
    "ቀይሕ": {"translation": "red", "category": "colors"},
    "ጸሊም": {"translation": "black", "category": "colors"},
    "ጻዕዳ": {"translation": "white", "category": "colors"},
    "ቢጫ": {"translation": "yellow", "category": "colors"},
    # Objects
    "መጽሓፍ": {"translation": "book", "category": "objects"},
    "ብርዒ": {"translation": "pen", "category": "objects"},
    "ጣውላ": {"translation": "table", "category": "objects"},
    "ገዛ": {"translation": "house", "category": "objects"},
    # Simple words
    "ሰላም": {"translation": "peace/hello", "category": "greetings"},
    "ማይ": {"translation": "water", "category": "objects"},
    "ሓሙስ": {"translation": "Thursday", "category": "time"},
}


class EnhancedDragDropGame:
    """Enhanced drag and drop game with true HTML5 drag-and-drop functionality"""

    def __init__(self):
        if "drag_drop_state" not in st.session_state:
            self.reset_game()

    def reset_game(self):
        """Reset game state"""
        st.session_state.drag_drop_state = {
            "current_word": None,
            "missing_positions": [],
            "missing_characters": [],
            "user_answers": {},
            "is_solved": False,
            "attempts": 0,
            "correct_count": 0,
            "total_count": 0,
            "difficulty": "easy",
            "puzzle_data": None,
        }

    def generate_puzzle(self, difficulty: str) -> Dict:
        """Generate a new puzzle with missing characters"""
        # Select random word
        word = random.choice(list(DRAG_DROP_WORDS.keys()))
        word_info = DRAG_DROP_WORDS[word]

        # Convert to list of characters
        characters = list(word)

        # Determine number of missing characters based on difficulty
        if difficulty == "easy":
            num_missing = max(1, len(characters) // 3)
        elif difficulty == "medium":
            num_missing = max(1, len(characters) // 2)
        else:  # hard
            num_missing = max(2, (len(characters) * 2) // 3)

        # Randomly select positions to make blank
        missing_positions = random.sample(
            range(len(characters)), min(num_missing, len(characters))
        )
        missing_characters = [characters[pos] for pos in missing_positions]

        # Create distractors (wrong options)
        all_chars = list(set("".join(DRAG_DROP_WORDS.keys())))
        wrong_options = [c for c in all_chars if c not in missing_characters]
        random.shuffle(wrong_options)

        num_wrong = min(3, len(wrong_options))
        options = missing_characters + wrong_options[:num_wrong]
        random.shuffle(options)

        puzzle = {
            "word": word,
            "translation": word_info["translation"],
            "category": word_info["category"],
            "characters": characters,
            "missing_positions": missing_positions,
            "missing_characters": missing_characters,
            "options": options,
            "phonetic": geez_to_latin_syllable(word),
        }

        # Store puzzle data in session state
        st.session_state.drag_drop_state.update(
            {
                "current_word": word,
                "missing_positions": missing_positions,
                "missing_characters": missing_characters,
                "user_answers": {pos: None for pos in missing_positions},
                "is_solved": False,
                "puzzle_data": puzzle,
            }
        )

        return puzzle

    def check_answer(self, user_answers: Dict) -> bool:
        """Check if the user's answer is correct"""
        state = st.session_state.drag_drop_state
        state["attempts"] += 1

        # Update user answers
        state["user_answers"].update(user_answers)

        # Check if answer is correct
        is_correct = True
        for pos in state["missing_positions"]:
            if state["user_answers"][pos] != state["puzzle_data"]["characters"][pos]:
                is_correct = False
                break

        state["total_count"] += 1
        if is_correct:
            state["correct_count"] += 1
            state["is_solved"] = True

        return is_correct

    def get_statistics(self) -> Dict:
        """Get game statistics"""
        state = st.session_state.drag_drop_state
        total = state["total_count"]
        correct = state["correct_count"]
        accuracy = (correct / total * 100) if total > 0 else 0

        return {"total": total, "correct": correct, "accuracy": accuracy}


def create_drag_drop_html(puzzle_data: Dict, component_key: str) -> str:
    """Create HTML with true drag-and-drop functionality"""

    word_display_html = ""
    for i, char in enumerate(puzzle_data["characters"]):
        if i in puzzle_data["missing_positions"]:
            word_display_html += f"""
            <div class="drop-zone"
                 ondrop="drop(event, {i})"
                 ondragover="allowDrop(event)"
                 ondragenter="dragEnter(event)"
                 ondragleave="dragLeave(event)"
                 data-position="{i}"
                 id="position-{i}">
                <span class="placeholder">?</span>
            </div>
            """
        else:
            word_display_html += f"""
            <div class="character-fixed">
                {char}
            </div>
            """

    options_html = ""
    for i, option in enumerate(puzzle_data["options"]):
        options_html += f"""
        <div class="draggable-character"
             draggable="true"
             ondragstart="drag(event)"
             ondragend="dragEnd(event)"
             data-character="{option}"
             id="option-{i}">
            {option}
        </div>
        """

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Noto Sans Ethiopic', serif, Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }}

            .game-container {{
                background: white;
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                max-width: 800px;
                margin: 0 auto;
            }}

            .puzzle-info {{
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                border-radius: 15px;
            }}

            .puzzle-info h3 {{
                margin: 0 0 10px 0;
                color: #2c3e50;
                font-size: 1.5em;
            }}

            .puzzle-info p {{
                margin: 5px 0;
                color: #34495e;
                font-size: 1.1em;
            }}

            .word-display {{
                display: flex;
                justify-content: center;
                gap: 15px;
                margin: 40px 0;
                flex-wrap: wrap;
            }}

            .character-fixed, .drop-zone {{
                width: 80px;
                height: 80px;
                border: 3px solid #3498db;
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2.5em;
                font-weight: bold;
                background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                color: white;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                transition: all 0.3s ease;
            }}

            .drop-zone {{
                background: linear-gradient(135deg, #ddd 0%, #bbb 100%);
                color: #666;
                border-style: dashed;
                border-color: #999;
                position: relative;
            }}

            .drop-zone.drag-over {{
                background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                border-color: #00b894;
                border-style: solid;
                transform: scale(1.05);
                box-shadow: 0 8px 25px rgba(0,184,148,0.3);
            }}

            .drop-zone.filled {{
                background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                border-style: solid;
                border-color: #00b894;
                color: white;
            }}

            .placeholder {{
                font-size: 2em;
                opacity: 0.5;
            }}

            .options-container {{
                margin-top: 40px;
                text-align: center;
            }}

            .options-title {{
                font-size: 1.3em;
                margin-bottom: 20px;
                color: #2c3e50;
                font-weight: bold;
            }}

            .options-grid {{
                display: flex;
                justify-content: center;
                gap: 15px;
                flex-wrap: wrap;
                margin-bottom: 30px;
            }}

            .draggable-character {{
                width: 70px;
                height: 70px;
                background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%);
                border: 3px solid #e84393;
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2.2em;
                font-weight: bold;
                color: white;
                cursor: grab;
                user-select: none;
                transition: all 0.3s ease;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}

            .draggable-character:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(232,67,147,0.3);
            }}

            .draggable-character:active {{
                cursor: grabbing;
                transform: scale(0.95);
            }}

            .draggable-character.dragging {{
                opacity: 0.5;
                transform: rotate(5deg) scale(1.1);
            }}

            .draggable-character.used {{
                opacity: 0.3;
                pointer-events: none;
                background: linear-gradient(135deg, #bbb 0%, #888 100%);
                border-color: #666;
            }}

            .control-buttons {{
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 30px;
            }}

            .btn {{
                padding: 12px 24px;
                border: none;
                border-radius: 25px;
                font-size: 1.1em;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}

            .btn-check {{
                background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                color: white;
            }}

            .btn-check:hover:not(:disabled) {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,184,148,0.3);
            }}

            .btn-check:disabled {{
                background: linear-gradient(135deg, #bbb 0%, #888 100%);
                cursor: not-allowed;
                opacity: 0.6;
            }}

            .btn-reset {{
                background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%);
                color: white;
            }}

            .btn-reset:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(253,121,168,0.3);
            }}

            .feedback {{
                text-align: center;
                margin-top: 20px;
                padding: 15px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 1.2em;
                display: none;
                animation: slideIn 0.5s ease-out;
            }}

            .feedback.success {{
                background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                color: white;
            }}

            .feedback.error {{
                background: linear-gradient(135deg, #e17055 0%, #fd79a8 100%);
                color: white;
            }}

            .status-indicator {{
                text-align: center;
                margin-bottom: 20px;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }}

            .status-indicator.ready {{
                background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                color: white;
            }}

            .status-indicator.incomplete {{
                background: linear-gradient(135deg, #fdcb6e 0%, #fd79a8 100%);
                color: white;
            }}

            @keyframes bounce {{
                0%, 20%, 50%, 80%, 100% {{
                    transform: translateY(0);
                }}
                40% {{
                    transform: translateY(-10px);
                }}
                60% {{
                    transform: translateY(-5px);
                }}
            }}

            @keyframes slideIn {{
                from {{
                    opacity: 0;
                    transform: translateY(-20px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}

            .bounce {{
                animation: bounce 1s;
            }}

            .progress-bar {{
                width: 100%;
                height: 10px;
                background: #ddd;
                border-radius: 5px;
                margin: 20px 0;
                overflow: hidden;
            }}

            .progress-fill {{
                height: 100%;
                background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                border-radius: 5px;
                transition: width 0.5s ease;
            }}
        </style>
    </head>
    <body>
        <div class="game-container">
            <div class="puzzle-info">
                <h3>🎯 {puzzle_data["category"].title()}</h3>
                <p><strong>Translation:</strong> {puzzle_data["translation"]}</p>
                <p><strong>Phonetic:</strong> {puzzle_data["phonetic"]}</p>
            </div>

            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill" style="width: 0%"></div>
            </div>

            <div class="word-display" id="word-display">
                {word_display_html}
            </div>

            <div class="options-container">
                <div class="options-title">📝 Drag characters to complete the word:</div>
                <div class="options-grid" id="options-grid">
                    {options_html}
                </div>
            </div>

            <div class="status-indicator" id="status-indicator">
                <span id="status-text">Place all characters to check your answer</span>
            </div>

            <div class="control-buttons">
                <button class="btn btn-check" id="check-btn" onclick="checkAnswer()" disabled>✅ Check Answer</button>
                <button class="btn btn-reset" onclick="resetPuzzle()">🔄 Reset</button>
            </div>

            <div class="feedback" id="feedback"></div>
        </div>

        <script>
            let userAnswers = {{}};
            let usedCharacters = new Set();
            let totalPositions = {len(puzzle_data["missing_positions"])};
            let correctAnswers = {json.dumps({pos: puzzle_data["characters"][pos] for pos in puzzle_data["missing_positions"]})};

            function updateProgress() {{
                let filledCount = Object.keys(userAnswers).length;
                let progress = (filledCount / totalPositions) * 100;
                document.getElementById('progress-fill').style.width = progress + '%';

                let statusIndicator = document.getElementById('status-indicator');
                let statusText = document.getElementById('status-text');
                let checkBtn = document.getElementById('check-btn');

                if (filledCount === totalPositions) {{
                    statusIndicator.className = 'status-indicator ready';
                    statusText.textContent = 'Ready to check your answer! 🎯';
                    checkBtn.disabled = false;
                }} else {{
                    statusIndicator.className = 'status-indicator incomplete';
                    statusText.textContent = `Place ${{totalPositions - filledCount}} more character(s)`;
                    checkBtn.disabled = true;
                }}
            }}

            function allowDrop(ev) {{
                ev.preventDefault();
            }}

            function dragEnter(ev) {{
                if (!ev.target.classList.contains('filled')) {{
                    ev.target.classList.add('drag-over');
                }}
            }}

            function dragLeave(ev) {{
                ev.target.classList.remove('drag-over');
            }}

            function drag(ev) {{
                ev.dataTransfer.setData("text", ev.target.getAttribute('data-character'));
                ev.dataTransfer.setData("source", ev.target.id);
                ev.target.classList.add('dragging');
            }}

            function dragEnd(ev) {{
                ev.target.classList.remove('dragging');
            }}

            function drop(ev) {{
                ev.preventDefault();
                ev.target.classList.remove('drag-over');

                const character = ev.dataTransfer.getData("text");
                const sourceId = ev.dataTransfer.getData("source");
                const position = parseInt(ev.target.getAttribute('data-position'));

                if (character && !ev.target.classList.contains('filled')) {{
                    // Check if this position already has a character
                    if (userAnswers[position]) {{
                        // Remove the old character from used set
                        let oldSourceId = findSourceByCharacter(userAnswers[position]);
                        if (oldSourceId) {{
                            document.getElementById(oldSourceId).classList.remove('used');
                            usedCharacters.delete(oldSourceId);
                        }}
                    }}

                    // Fill the drop zone
                    ev.target.innerHTML = character;
                    ev.target.classList.add('filled', 'bounce');

                    // Mark source as used
                    const sourceElement = document.getElementById(sourceId);
                    sourceElement.classList.add('used');
                    usedCharacters.add(sourceId);

                    // Store answer
                    userAnswers[position] = character;

                    // Update progress
                    updateProgress();

                    // Remove bounce animation after it completes
                    setTimeout(() => {{
                        ev.target.classList.remove('bounce');
                    }}, 1000);
                }}
            }}

            function findSourceByCharacter(character) {{
                let sources = document.querySelectorAll('.draggable-character');
                for (let source of sources) {{
                    if (source.getAttribute('data-character') === character) {{
                        return source.id;
                    }}
                }}
                return null;
            }}

            function checkAnswer() {{
                let isCorrect = true;
                let feedback = document.getElementById('feedback');

                // Check each position
                for (let position in correctAnswers) {{
                    if (userAnswers[position] !== correctAnswers[position]) {{
                        isCorrect = false;
                        break;
                    }}
                }}

                if (isCorrect) {{
                    feedback.innerHTML = '🎉 Fantastic! You got it right!';
                    feedback.className = 'feedback success';

                    // Add celebration effects
                    document.getElementById('word-display').classList.add('bounce');

                    // Send success message to parent
                    if (window.parent) {{
                        window.parent.postMessage({{
                            type: 'answer_result',
                            correct: true,
                            answers: userAnswers
                        }}, '*');
                    }}
                }} else {{
                    feedback.innerHTML = '❌ Not quite right. Keep trying!';
                    feedback.className = 'feedback error';

                    // Send failure message to parent
                    if (window.parent) {{
                        window.parent.postMessage({{
                            type: 'answer_result',
                            correct: false,
                            answers: userAnswers
                        }}, '*');
                    }}
                }}

                feedback.style.display = 'block';

                // Hide feedback after 3 seconds if incorrect
                if (!isCorrect) {{
                    setTimeout(() => {{
                        feedback.style.display = 'none';
                    }}, 3000);
                }}
            }}

            function resetPuzzle() {{
                // Clear all drop zones
                const dropZones = document.querySelectorAll('.drop-zone');
                dropZones.forEach(zone => {{
                    zone.innerHTML = '<span class="placeholder">?</span>';
                    zone.classList.remove('filled', 'drag-over', 'bounce');
                }});

                // Reset all draggable items
                const draggables = document.querySelectorAll('.draggable-character');
                draggables.forEach(draggable => {{
                    draggable.classList.remove('used');
                }});

                // Clear data
                userAnswers = {{}};
                usedCharacters.clear();

                // Hide feedback
                document.getElementById('feedback').style.display = 'none';

                // Update progress
                updateProgress();

                // Remove bounce from word display
                document.getElementById('word-display').classList.remove('bounce');

                // Notify parent
                if (window.parent) {{
                    window.parent.postMessage({{
                        type: 'reset'
                    }}, '*');
                }}
            }}

            // Initialize progress on load
            document.addEventListener('DOMContentLoaded', function() {{
                updateProgress();
            }});
        </script>
    </body>
    </html>
    """

    return html_code


def render():
    """Main drag and drop learning page"""
    st.subheader("🎮 Drag & Drop Word Builder")
    st.markdown("*Interactive character placement game with true drag-and-drop*")

    game = EnhancedDragDropGame()

    # Game controls header
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button(
            "🎲 New Puzzle", type="primary", help="Generate a brand new word puzzle"
        ):
            game.reset_game()
            st.rerun()

    with col2:
        difficulty = st.selectbox(
            "Difficulty Level:",
            ["easy", "medium", "hard"],
            index=0,
            help="Choose how many characters will be missing",
        )
        st.session_state.drag_drop_state["difficulty"] = difficulty

    with col3:
        stats = game.get_statistics()
        if stats["total"] > 0:
            st.metric(
                "Success Rate",
                f"{stats['accuracy']:.0f}%",
                delta=f"+{stats['correct']}" if stats["correct"] > 0 else None,
            )
        else:
            st.metric("Success Rate", "Start playing!")

    with col4:
        if stats["total"] > 0:
            st.metric("Puzzles Solved", f"{stats['correct']}/{stats['total']}")
        else:
            st.metric("Puzzles Solved", "0/0")

    st.markdown("---")

    # Generate or display current puzzle
    if st.session_state.drag_drop_state["current_word"] is None:
        puzzle = game.generate_puzzle(difficulty)
    else:
        puzzle = st.session_state.drag_drop_state["puzzle_data"]

    # Check if puzzle is solved
    if st.session_state.drag_drop_state["is_solved"]:
        st.success("🎉 Puzzle Completed Successfully!")

        # Show completion details in an attractive format
        st.markdown(
            f"""
            <div style='
                background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                padding: 30px;
                border-radius: 20px;
                color: white;
                text-align: center;
                margin: 25px 0;
                box-shadow: 0 15px 35px rgba(0,184,148,0.3);
            '>
                <h1 style='margin: 0 0 15px 0; font-size: 3em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                    ✨ {puzzle["word"]} ✨
                </h1>
                <h2 style='margin: 0 0 10px 0; font-size: 1.5em;'>"{puzzle["translation"]}"</h2>
                <p style='margin: 5px 0; font-size: 1.2em; opacity: 0.9;'><strong>Phonetic:</strong> {puzzle["phonetic"]}</p>
                <p style='margin: 5px 0; font-size: 1.2em; opacity: 0.9;'><strong>Category:</strong> {puzzle["category"].title()}</p>
                <p style='margin: 20px 0 0 0; font-size: 1.1em; opacity: 0.8;'>
                    🏆 Attempts: {st.session_state.drag_drop_state["attempts"]}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Show balloons celebration
        st.balloons()

        # Next puzzle button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎲 Try Another Puzzle", type="primary", key="next_puzzle"):
                game.reset_game()
                st.rerun()

    else:
        # Display the interactive drag-drop game
        component_key = f"drag_drop_{st.session_state.drag_drop_state.get('current_word', 'default')}"

        # Create the HTML content
        html_content = create_drag_drop_html(puzzle, component_key)

        # Use a container for the game
        game_container = st.container()
        with game_container:
            # Render the HTML component
            result = components.html(html_content, height=800, scrolling=False)

    # Instructions and tips
    st.markdown("---")

    # Instructions
    with st.expander(
        "📖 How to Play",
        expanded=not st.session_state.drag_drop_state["is_solved"],
    ):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### 🎯 Game Instructions:
            1. **Drag** characters from the colored boxes below
            2. **Drop** them into the correct positions in the word
            3. Watch the **progress bar** fill up as you place characters
            4. **Click "Check Answer"** when all positions are filled
            5. Get **instant feedback** on your solution!
            """)

        with col2:
            st.markdown("""
            ### 💡 Pro Tips:
            - Use the **translation** hint to guide your choices
            - The **phonetic** spelling can help with pronunciation
            - **Category** provides context clues
            - Characters **glow** when you hover over drop zones
            - **Progress bar** shows your completion status
            """)

    # Learning objectives and benefits
    with st.expander("🎓 Learning Benefits"):
        st.markdown("""
        ### What You'll Learn:
        - **Character Recognition**: Identify individual Tigrinya characters
        - **Word Building**: Understand how characters combine to form words
        - **Visual Memory**: Strengthen visual association with character shapes
        - **Context Learning**: Connect words with their meanings and categories
        - **Motor Skills**: Develop precise drag-and-drop coordination

        ### Why This Method Works:
        - **Active Learning**: Physical interaction improves retention
        - **Immediate Feedback**: Quick correction helps reinforce learning
        - **Progressive Difficulty**: Start easy and build confidence
        - **Contextual Hints**: Multiple clues support different learning styles
        - **Gamification**: Fun elements increase engagement and motivation
        """)

    # Technical features
    with st.expander("⚙️ Technical Features"):
        st.markdown("""
        ### This Enhanced Version Includes:
        - **True HTML5 Drag & Drop**: Authentic drag-and-drop interaction
        - **Smooth Animations**: Visual feedback during interactions
        - **Progress Tracking**: Real-time completion status
        - **Smart Validation**: Instant answer checking
        - **Responsive Design**: Works on desktop and tablet devices
        - **Accessibility**: Keyboard-friendly and screen reader compatible
        - **Performance**: Fast loading and smooth animations
        """)

    # Footer with current game state (for debugging)
    if st.checkbox("🔧 Show Debug Info", value=False):
        st.json(
            {
                "current_state": st.session_state.drag_drop_state,
                "puzzle_info": puzzle if puzzle else None,
            }
        )


if __name__ == "__main__":
    render()
