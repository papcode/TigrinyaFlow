import json
import random
from typing import Dict, List, Tuple

import streamlit as st
import streamlit.components.v1 as components

from clientTranslation import geez_to_latin_syllable

# Word bank for drag-and-drop exercises
DRAG_DROP_WORDS = {
    # Animals
    "ዶሮ": { "translation": "chicken", "category": "animals" },
    "ላም": { "translation": "cow", "category": "animals" },
    "ድሙ": { "translation": "cat", "category": "animals" },
    "ከልቢ": { "translation": "dog", "category": "animals" },

    # Colors
    "ቀይሕ": { "translation": "red", "category": "colors" },
    "ጸሊም": { "translation": "black", "category": "colors" },
    "ጻዕዳ": { "translation": "white", "category": "colors" },
    "ቢጫ": { "translation": "yellow", "category": "colors" },

    # Objects
    "መጽሓፍ": { "translation": "book", "category": "objects" },
    "ብርዒ": { "translation": "pen", "category": "objects" },
    "ጣውላ": { "translation": "table", "category": "objects" },
    "ገዛ": { "translation": "house", "category": "objects" },

    # Greetings / Simple words
    "ሰላም": { "translation": "peace/hello", "category": "greetings" },

    # Nature / Time
    "ማይ": { "translation": "water", "category": "objects" },
    "ሓሙስ": { "translation": "Thursday", "category": "time" },
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
            num_missing = max(1, min(2, len(characters) // 3))  # 1-2 characters missing
        elif difficulty == "medium":
            num_missing = max(2, min(3, len(characters) // 2))  # 2-3 characters missing
        else:  # hard
            num_missing = max(3, len(characters) - 1)  # Most characters missing

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

        return {
            "total": total,
            "correct": correct,
            "accuracy": accuracy,
        }


def create_drag_drop_html(puzzle_data: Dict, component_key: str) -> str:
    """Create HTML with true drag-and-drop functionality and complete game system"""

    # Complete word bank with more words
    all_words = {
    # Animals
    "ዶሮ": { "translation": "chicken", "category": "animals", "phonetic": "doro" },
    "ላም": { "translation": "cow", "category": "animals", "phonetic": "lam" },
    "ድሙ": { "translation": "cat", "category": "animals", "phonetic": "dimu" },
    "ከልቢ": { "translation": "dog", "category": "animals", "phonetic": "kelbi" },
    "ጊደር": { "translation": "donkey", "category": "animals", "phonetic": "gider" },
    "ፈረስ": { "translation": "horse", "category": "animals", "phonetic": "feres" },

    # Colors
    "ቀይሕ": { "translation": "red", "category": "colors", "phonetic": "qeyiH" },
    "ጸሊም": { "translation": "black", "category": "colors", "phonetic": "Selim" },
    "ጻዕዳ": { "translation": "white", "category": "colors", "phonetic": "Sa'ida" },
    "ቢጫ": { "translation": "yellow", "category": "colors", "phonetic": "bicha" },
    "ሰማያዊ": { "translation": "blue", "category": "colors", "phonetic": "semayawi" },

    # Objects
    "መጽሓፍ": { "translation": "book", "category": "objects", "phonetic": "meShaf" },
    "ብርዒ": { "translation": "pen", "category": "objects", "phonetic": "biri" },
    "ጣውላ": { "translation": "table", "category": "objects", "phonetic": "tawila" },
    "ገዛ": { "translation": "house", "category": "objects", "phonetic": "geza" },
    "መኪና": { "translation": "car", "category": "objects", "phonetic": "mekina" },
    "ፀሓይ": { "translation": "sun", "category": "objects", "phonetic": "SaHay" },

    # Greetings
    "ሰላም": {
        "translation": "peace/hello",
        "category": "greetings",
        "phonetic": "selam",
    },
    "ጥዕና": { "translation": "health", "category": "greetings", "phonetic": "Tiina" },

    # Nature / Time
    "ማይ": { "translation": "water", "category": "nature", "phonetic": "may" },
    "ሓሙስ": { "translation": "Thursday", "category": "time", "phonetic": "Hamus" },
}



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

            .game-header {{
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px;
                color: white;
            }}

            .game-stats {{
                display: flex;
                justify-content: space-around;
                margin-bottom: 20px;
                flex-wrap: wrap;
                gap: 10px;
            }}

            .stat-item {{
                text-align: center;
                padding: 10px;
                background: rgba(255,255,255,0.2);
                border-radius: 10px;
                min-width: 100px;
            }}

            .puzzle-info {{
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                border-radius: 15px;
            }}

            .difficulty-selector {{
                text-align: center;
                margin-bottom: 20px;
            }}

            .difficulty-btn {{
                margin: 5px;
                padding: 8px 16px;
                border: none;
                border-radius: 20px;
                cursor: pointer;
                font-weight: bold;
                transition: all 0.3s ease;
            }}

            .difficulty-btn.active {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                transform: scale(1.1);
            }}

            .difficulty-btn:not(.active) {{
                background: #ddd;
                color: #666;
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

            .options-grid {{
                display: flex;
                justify-content: center;
                gap: 15px;
                flex-wrap: wrap;
                margin: 30px 0;
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

            .draggable-character.used {{
                opacity: 0.3;
                pointer-events: none;
                background: linear-gradient(135deg, #bbb 0%, #888 100%);
            }}

            .control-buttons {{
                display: flex;
                justify-content: center;
                gap: 20px;
                margin: 30px 0;
            }}

            .btn {{
                padding: 12px 24px;
                border: none;
                border-radius: 25px;
                font-size: 1.1em;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            }}

            .btn-check {{
                background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                color: white;
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

            .feedback {{
                text-align: center;
                margin: 20px 0;
                padding: 15px;
                border-radius: 10px;
                font-weight: bold;
                font-size: 1.2em;
                display: none;
            }}

            .feedback.success {{
                background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
                color: white;
            }}

            .feedback.error {{
                background: linear-gradient(135deg, #e17055 0%, #fd79a8 100%);
                color: white;
            }}

            @keyframes bounce {{
                0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
                40% {{ transform: translateY(-10px); }}
                60% {{ transform: translateY(-5px); }}
            }}

            @keyframes balloon-float {{
                0% {{ transform: translateY(0px); opacity: 1; }}
                100% {{ transform: translateY(-100vh); opacity: 0; }}
            }}

            .bounce {{ animation: bounce 1s; }}
        </style>
    </head>
    <body>
        <div class="game-container">
            <div class="game-header">
                <h1>🎮 Tigrinya Word Builder</h1>
                <div class="game-stats">
                    <div class="stat-item">
                        <div>Level</div>
                        <div id="level-display">1</div>
                    </div>
                    <div class="stat-item">
                        <div>Score</div>
                        <div id="score-display">0</div>
                    </div>
                    <div class="stat-item">
                        <div>Correct</div>
                        <div id="correct-display">0</div>
                    </div>
                    <div class="stat-item">
                        <div>Total</div>
                        <div id="total-display">0</div>
                    </div>
                </div>
                <div class="difficulty-selector">
                    <button class="difficulty-btn active" onclick="setDifficulty('easy')">🟢 Easy</button>
                    <button class="difficulty-btn" onclick="setDifficulty('medium')">🟡 Medium</button>
                    <button class="difficulty-btn" onclick="setDifficulty('hard')">🔴 Hard</button>
                </div>
            </div>

            <div class="puzzle-info" id="puzzle-info">
                <h3 id="category-display">Loading...</h3>
                <p><strong>Translation:</strong> <span id="translation-display">Loading...</span></p>
                <p><strong>Phonetic:</strong> <span id="phonetic-display">Loading...</span></p>
            </div>

            <div class="word-display" id="word-display"></div>

            <div class="options-grid" id="options-grid"></div>

            <div class="control-buttons">
                <button class="btn btn-check" id="check-btn" onclick="checkAnswer()" disabled>✅ Check Answer</button>
                <button class="btn btn-reset" onclick="resetCurrentPuzzle()">🔄 Reset</button>
                <button class="btn btn-reset" onclick="newPuzzle()">🎲 New Puzzle</button>
            </div>

            <div class="feedback" id="feedback"></div>
        </div>

        <script>
            // Game state
            let gameState = {{
                level: 1,
                score: 0,
                correct: 0,
                total: 0,
                difficulty: 'easy',
                currentPuzzle: null,
                userAnswers: {{}},
                usedCharacters: new Set()
            }};

            // Word bank
            const WORDS = {json.dumps(all_words, ensure_ascii=False)};


                    function generatePuzzle(word, wordInfo) {{
                        const characters = Array.from(word);
                        let numMissing;

                        // Determine missing characters based on difficulty
                        if (gameState.difficulty === 'easy') {{
                            numMissing = Math.max(1, Math.min(2, Math.floor(characters.length / 3)));
                        }} else if (gameState.difficulty === 'medium') {{
                            numMissing = Math.max(2, Math.min(3, Math.floor(characters.length / 2)));
                        }} else {{
                            numMissing = Math.max(3, characters.length - 1);
                        }}

                        // Randomly select positions to make blank
                        const missingPositions = [];
                        while (missingPositions.length < numMissing && missingPositions.length < characters.length) {{
                            const pos = Math.floor(Math.random() * characters.length);
                            if (!missingPositions.includes(pos)) {{
                                missingPositions.push(pos);
                            }}
                        }}

                        const missingCharacters = missingPositions.map(pos => characters[pos]);

                        // Create distractors
                        const allChars = Array.from(new Set(Object.keys(WORDS).join('')));
                        const wrongOptions = allChars.filter(c => !missingCharacters.includes(c));
                        const shuffledWrong = wrongOptions.sort(() => Math.random() - 0.5);
                        const options = [...missingCharacters, ...shuffledWrong.slice(0, 3)].sort(() => Math.random() - 0.5);

                        return {{
                            word: word,
                            characters: characters,
                            missingPositions: missingPositions,
                            missingCharacters: missingCharacters,
                            options: options,
                            correctAnswers: Object.fromEntries(missingPositions.map(pos => [pos, characters[pos]]))
                        }};
                    }}

                    function newPuzzle() {{
                        // Select random word
                        const wordKeys = Object.keys(WORDS);
                        const randomWord = wordKeys[Math.floor(Math.random() * wordKeys.length)];
                        const wordInfo = WORDS[randomWord];

                        // Generate puzzle
                        gameState.currentPuzzle = generatePuzzle(randomWord, wordInfo);
                        gameState.userAnswers = {{}};
                        gameState.usedCharacters.clear();

                        // Update puzzle info
                        document.getElementById('category-display').textContent = '🎯 ' + wordInfo.category.charAt(0).toUpperCase() + wordInfo.category.slice(1);
                        document.getElementById('translation-display').textContent = wordInfo.translation;
                        document.getElementById('phonetic-display').textContent = wordInfo.phonetic;

                        // Render word display
                        const wordDisplay = document.getElementById('word-display');
                        wordDisplay.innerHTML = '';
                        gameState.currentPuzzle.characters.forEach((char, i) => {{
                            if (gameState.currentPuzzle.missingPositions.includes(i)) {{
                                wordDisplay.innerHTML += `
                                    <div class="drop-zone" ondrop="drop(event, ${{i}})" ondragover="allowDrop(event)"
                                         ondragenter="dragEnter(event)" ondragleave="dragLeave(event)"
                                         data-position="${{i}}" id="position-${{i}}">
                                        <span style="font-size: 2em; opacity: 0.5;">?</span>
                                    </div>
                                `;
                            }} else {{
                                wordDisplay.innerHTML += `
                                    <div class="character-fixed">${{char}}</div>
                                `;
                            }}
                        }});

                        // Render options
                        const optionsGrid = document.getElementById('options-grid');
                        optionsGrid.innerHTML = '';
                        gameState.currentPuzzle.options.forEach((option, i) => {{
                            optionsGrid.innerHTML += `
                                <div class="draggable-character" draggable="true" ondragstart="drag(event)"
                                     ondragend="dragEnd(event)" data-character="${{option}}" id="option-${{i}}">
                                    ${{option}}
                                </div>
                            `;
                        }});

                        // Reset button state
                        document.getElementById('check-btn').disabled = true;
                        document.getElementById('feedback').style.display = 'none';
                        updateStats();
                    }}

                    function setDifficulty(level) {{
                        gameState.difficulty = level;
                        document.querySelectorAll('.difficulty-btn').forEach(btn => btn.classList.remove('active'));
                        event.target.classList.add('active');
                        newPuzzle(); // Generate new puzzle with new difficulty
                    }}

                    function updateStats() {{
                        document.getElementById('level-display').textContent = gameState.level;
                        document.getElementById('score-display').textContent = gameState.score;
                        document.getElementById('correct-display').textContent = gameState.correct;
                        document.getElementById('total-display').textContent = gameState.total;
                    }}

                    function allowDrop(ev) {{ ev.preventDefault(); }}
                    function dragEnter(ev) {{ if (!ev.target.classList.contains('filled')) ev.target.classList.add('drag-over'); }}
                    function dragLeave(ev) {{ ev.target.classList.remove('drag-over'); }}
                    function drag(ev) {{
                        ev.dataTransfer.setData("text", ev.target.getAttribute('data-character'));
                        ev.dataTransfer.setData("source", ev.target.id);
                        ev.target.style.opacity = '0.5';
                    }}
                    function dragEnd(ev) {{ ev.target.style.opacity = '1'; }}

                    function drop(ev) {{
                        ev.preventDefault();
                        ev.target.classList.remove('drag-over');
                        const character = ev.dataTransfer.getData("text");
                        const sourceId = ev.dataTransfer.getData("source");
                        const position = parseInt(ev.target.getAttribute('data-position'));

                        if (character) {{
                            // If position already has a character, free up the old one
                            if (ev.target.classList.contains('filled') && gameState.userAnswers[position]) {{
                                const oldCharacter = gameState.userAnswers[position];
                                // Find and free the old character's source
                                document.querySelectorAll('.draggable-character').forEach(draggable => {{
                                    if (draggable.getAttribute('data-character') === oldCharacter && draggable.classList.contains('used')) {{
                                        draggable.classList.remove('used');
                                        return;
                                    }}
                                }});
                            }}

                            // Place new character
                            ev.target.innerHTML = character;
                            ev.target.classList.add('filled', 'bounce');
                            document.getElementById(sourceId).classList.add('used');
                            gameState.userAnswers[position] = character;

                            setTimeout(() => ev.target.classList.remove('bounce'), 1000);

                            // Check if all positions filled
                            if (Object.keys(gameState.userAnswers).length === gameState.currentPuzzle.missingPositions.length) {{
                                document.getElementById('check-btn').disabled = false;
                            }}
                        }}
                    }}

                    function checkAnswer() {{
                        let isCorrect = true;
                        for (let position in gameState.currentPuzzle.correctAnswers) {{
                            if (gameState.userAnswers[position] !== gameState.currentPuzzle.correctAnswers[position]) {{
                                isCorrect = false;
                                break;
                            }}
                        }}

                        gameState.total++;
                        const feedback = document.getElementById('feedback');

                        if (isCorrect) {{
                            gameState.correct++;
                            const points = {{easy: 10, medium: 20, hard: 30}}[gameState.difficulty];
                            gameState.score += points;

                            if (gameState.correct % 5 === 0) gameState.level++;

                            feedback.innerHTML = `🎉 Correct! +${{points}} points! 🎊`;
                            feedback.className = 'feedback success';

                            // Create balloons
                            for (let i = 0; i < 8; i++) {{
                                const balloon = document.createElement('div');
                                balloon.innerHTML = ['🎈', '🎊', '🎉', '✨'][Math.floor(Math.random() * 4)];
                                balloon.style.cssText = `position:fixed; left:${{Math.random() * window.innerWidth}}px; top:100%; font-size:2em; z-index:1000; pointer-events:none; animation:balloon-float 3s ease-out forwards;`;
                                document.body.appendChild(balloon);
                                setTimeout(() => balloon.remove(), 3000);
                            }}

                            setTimeout(() => newPuzzle(), 2500);
                        }} else {{
                            feedback.innerHTML = '❌ Try again! Check your character placement.';
                            feedback.className = 'feedback error';
                            setTimeout(() => feedback.style.display = 'none', 3000);
                        }}

                        feedback.style.display = 'block';
                        updateStats();
                    }}

                    function resetCurrentPuzzle() {{
                        // Clear all drop zones
                        const dropZones = document.querySelectorAll('.drop-zone');
                        dropZones.forEach(zone => {{
                            if (zone.classList.contains('filled')) {{
                                zone.innerHTML = '<span style="font-size: 2em; opacity: 0.5;">?</span>';
                                zone.classList.remove('filled', 'bounce');
                            }}
                        }});

                        // Reset all draggable items
                        const draggables = document.querySelectorAll('.draggable-character');
                        draggables.forEach(draggable => {{
                            draggable.classList.remove('used');
                        }});

                        // Clear user answers
                        gameState.userAnswers = {{}};
                        gameState.usedCharacters.clear();

                        // Reset button state
                        document.getElementById('check-btn').disabled = true;
                        document.getElementById('feedback').style.display = 'none';

                        // Show reset message
                        const feedback = document.getElementById('feedback');
                        feedback.innerHTML = '🔄 Puzzle reset! Try again.';
                        feedback.className = 'feedback success';
                        feedback.style.display = 'block';
                        setTimeout(() => {{
                            feedback.style.display = 'none';
                        }}, 1500);
                    }}

                    // Initialize game
                    document.addEventListener('DOMContentLoaded', function() {{
                        newPuzzle();
                    }});
        </script>
    </body>
    </html>
    """

    return html_code


def render():
    """Main drag and drop learning page"""
    st.subheader("🎮 Drag & Drop Word Builder")
    st.markdown("*Complete self-contained Tigrinya learning game*")

    # Simple info about the game
    st.info(
        """
        🎯 **How to Play:**
        - All game controls, scoring, and difficulty settings are inside the game below
        - Drag characters to complete words
        - Click 'Check Answer' when ready
        - Game automatically progresses to new puzzles
        - Try different difficulty levels for more challenge!
        """
    )

    # Create the HTML content with initial puzzle data
    game = EnhancedDragDropGame()
    puzzle = game.generate_puzzle("easy")  # Start with easy
    html_content = create_drag_drop_html(puzzle, "self_contained_game")

    # Render the self-contained game
    components.html(html_content, height=1200, scrolling=False)

    # Learning information
    st.markdown("---")

    with st.expander("🎓 About This Learning Game"):
        st.markdown("""
        ### 🎯 Learning Objectives:
        - **Character Recognition**: Master individual Tigrinya characters
        - **Word Building**: Learn how characters combine to form words
        - **Contextual Learning**: Connect words with meanings and categories
        - **Progressive Difficulty**: Build skills from easy to challenging levels

        ### 🎮 Game Features:
        - **Complete Self-Contained Game**: All controls inside the game canvas
        - **Multiple Difficulty Levels**: Easy, Medium, Hard with different challenges
        - **Auto-Progression**: Automatic new puzzles after success
        - **Real-Time Scoring**: Points, levels, and statistics tracking
        - **Balloon Celebrations**: Fun animations for successful completions
        - **True Drag & Drop**: Authentic HTML5 drag-and-drop interaction

        ### 💡 Tips for Success:
        - Use translation and phonetic hints to guide your choices
        - Try different difficulty levels to challenge yourself
        - Pay attention to word categories for context clues
        - Practice regularly to build character recognition skills
        """)


if __name__ == "__main__":
    render()
