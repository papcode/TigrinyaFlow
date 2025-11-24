import streamlit as st
import random
from typing import List, Dict, Tuple
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

class DragDropGame:
    """Manages drag and drop word building game state"""
    
    def __init__(self):
        if 'drag_drop_state' not in st.session_state:
            self.reset_game()
    
    def reset_game(self):
        """Reset game state"""
        st.session_state.drag_drop_state = {
            'current_word': None,
            'missing_positions': [],
            'missing_characters': [],
            'user_answers': {},
            'is_solved': False,
            'attempts': 0,
            'correct_count': 0,
            'total_count': 0,
            'difficulty': 'easy'
        }
    
    def generate_puzzle(self, difficulty: str = 'easy') -> Dict:
        """Generate a new drag-and-drop puzzle"""
        # Select random word
        word = random.choice(list(DRAG_DROP_WORDS.keys()))
        word_info = DRAG_DROP_WORDS[word]
        
        # Convert to list of characters
        characters = list(word)
        
        # Determine number of missing characters based on difficulty
        if difficulty == 'easy':
            num_missing = 1
        elif difficulty == 'medium':
            num_missing = min(2, len(characters) - 1)
        else:  # hard
            num_missing = min(3, len(characters) - 1)
        
        # Randomly select positions to hide
        missing_positions = random.sample(range(len(characters)), num_missing)
        missing_positions.sort()
        
        # Extract missing characters
        missing_characters = [characters[pos] for pos in missing_positions]
        
        # Add some wrong options
        all_chars = list(set(''.join(DRAG_DROP_WORDS.keys())))
        wrong_options = [c for c in all_chars if c not in missing_characters]
        random.shuffle(wrong_options)
        
        # Create options pool (correct + wrong)
        num_wrong = min(3, len(wrong_options))
        options = missing_characters + wrong_options[:num_wrong]
        random.shuffle(options)
        
        puzzle = {
            'word': word,
            'translation': word_info['translation'],
            'category': word_info['category'],
            'characters': characters,
            'missing_positions': missing_positions,
            'missing_characters': missing_characters,
            'options': options,
            'phonetic': geez_to_latin_syllable(word)
        }
        
        st.session_state.drag_drop_state.update({
            'current_word': word,
            'missing_positions': missing_positions,
            'missing_characters': missing_characters,
            'user_answers': {pos: None for pos in missing_positions},
            'is_solved': False,
            'attempts': 0
        })
        
        return puzzle
    
    def check_answer(self) -> bool:
        """Check if the user's answer is correct"""
        state = st.session_state.drag_drop_state
        user_answers = state['user_answers']
        missing_chars = state['missing_characters']
        missing_positions = state['missing_positions']
        
        # Check if all positions are filled
        if any(user_answers[pos] is None for pos in missing_positions):
            return False
        
        # Check if answers are correct
        is_correct = all(
            user_answers[pos] == missing_chars[i]
            for i, pos in enumerate(missing_positions)
        )
        
        state['attempts'] += 1
        state['total_count'] += 1
        
        if is_correct:
            state['is_solved'] = True
            state['correct_count'] += 1
        
        return is_correct
    
    def get_statistics(self) -> Dict:
        """Get game statistics"""
        state = st.session_state.drag_drop_state
        total = state['total_count']
        correct = state['correct_count']
        
        return {
            'total': total,
            'correct': correct,
            'accuracy': (correct / total * 100) if total > 0 else 0
        }

def render_word_display(puzzle: Dict):
    """Render the word display with blanks"""
    characters = puzzle['characters']
    missing_positions = puzzle['missing_positions']
    user_answers = st.session_state.drag_drop_state['user_answers']
    
    st.markdown("### 🎯 Fill in the missing characters:")
    
    # Display word with blanks
    cols = st.columns(len(characters))
    
    for i, char in enumerate(characters):
        with cols[i]:
            if i in missing_positions:
                # Show blank or user's answer
                answer = user_answers.get(i)
                if answer:
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                        font-size: 2.5em;
                        color: white;
                        font-family: "Noto Sans Ethiopic", serif;
                        min-height: 80px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                    '>
                        {answer}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #e0e0e0 0%, #bdbdbd 100%);
                        padding: 20px;
                        border-radius: 10px;
                        text-align: center;
                        font-size: 2.5em;
                        color: #666;
                        font-family: "Noto Sans Ethiopic", serif;
                        min-height: 80px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border: 2px dashed #999;
                    '>
                        _
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Show actual character
                st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    font-size: 2.5em;
                    color: white;
                    font-family: "Noto Sans Ethiopic", serif;
                    min-height: 80px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                '>
                    {char}
                </div>
                """, unsafe_allow_html=True)

def render_options(puzzle: Dict):
    """Render draggable character options"""
    options = puzzle['options']
    missing_positions = puzzle['missing_positions']
    
    st.markdown("### 📝 Available Characters:")
    st.markdown("Click on a character, then click on a blank position to place it")
    
    # Character selection
    if 'selected_char' not in st.session_state:
        st.session_state.selected_char = None
    
    # Display options in a grid
    cols_per_row = 4
    for i in range(0, len(options), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(options):
                char = options[i + j]
                with col:
                    is_selected = st.session_state.selected_char == char
                    button_style = "primary" if is_selected else "secondary"
                    
                    if st.button(
                        char,
                        key=f"option_{char}_{i}_{j}",
                        use_container_width=True,
                        type=button_style
                    ):
                        st.session_state.selected_char = char
                        st.rerun()
    
    # Position selection
    if st.session_state.selected_char:
        st.markdown(f"**Selected character:** {st.session_state.selected_char}")
        st.markdown("**Click on a blank position to place it:**")
        
        position_cols = st.columns(len(missing_positions))
        for idx, pos in enumerate(missing_positions):
            with position_cols[idx]:
                current_answer = st.session_state.drag_drop_state['user_answers'][pos]
                label = f"Position {pos + 1}" if not current_answer else f"Replace {current_answer}"
                
                if st.button(
                    label,
                    key=f"pos_{pos}",
                    use_container_width=True
                ):
                    st.session_state.drag_drop_state['user_answers'][pos] = st.session_state.selected_char
                    st.session_state.selected_char = None
                    st.rerun()

def render():
    """Main drag and drop learning page"""
    st.subheader("🎮 Drag & Drop Word Builder")
    
    game = DragDropGame()
    
    # Game controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🎲 New Puzzle", type="primary", use_container_width=True):
            game.reset_game()
            st.rerun()
    
    with col2:
        difficulty = st.selectbox(
            "Difficulty:",
            ["easy", "medium", "hard"],
            index=0
        )
        st.session_state.drag_drop_state['difficulty'] = difficulty
    
    with col3:
        if st.button("🔄 Reset Current", use_container_width=True):
            for pos in st.session_state.drag_drop_state['user_answers']:
                st.session_state.drag_drop_state['user_answers'][pos] = None
            st.session_state.drag_drop_state['is_solved'] = False
            st.rerun()
    
    with col4:
        stats = game.get_statistics()
        st.metric("Accuracy", f"{stats['accuracy']:.0f}%")
    
    # Display statistics
    if stats['total'] > 0:
        st.info(f"📊 Solved: {stats['correct']} / {stats['total']} puzzles")
    
    st.markdown("---")
    
    # Generate or display current puzzle
    if st.session_state.drag_drop_state['current_word'] is None:
        puzzle = game.generate_puzzle(difficulty)
    else:
        # Reconstruct puzzle from state
        word = st.session_state.drag_drop_state['current_word']
        word_info = DRAG_DROP_WORDS[word]
        characters = list(word)
        missing_positions = st.session_state.drag_drop_state['missing_positions']
        missing_characters = st.session_state.drag_drop_state['missing_characters']
        
        # Recreate options
        all_chars = list(set(''.join(DRAG_DROP_WORDS.keys())))
        wrong_options = [c for c in all_chars if c not in missing_characters]
        random.shuffle(wrong_options)
        num_wrong = min(3, len(wrong_options))
        options = missing_characters + wrong_options[:num_wrong]
        random.shuffle(options)
        
        puzzle = {
            'word': word,
            'translation': word_info['translation'],
            'category': word_info['category'],
            'characters': characters,
            'missing_positions': missing_positions,
            'missing_characters': missing_characters,
            'options': options,
            'phonetic': geez_to_latin_syllable(word)
        }
    
    # Display puzzle info
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Category:** {puzzle['category'].title()}")
        st.markdown(f"**Translation:** {puzzle['translation']}")
        st.markdown(f"**Phonetic:** {puzzle['phonetic']}")
    
    with col2:
        st.markdown(f"**Attempts:** {st.session_state.drag_drop_state['attempts']}")
    
    st.markdown("---")
    
    # Main game area
    if not st.session_state.drag_drop_state['is_solved']:
        # Display word with blanks
        render_word_display(puzzle)
        
        st.markdown("---")
        
        # Display options
        render_options(puzzle)
        
        st.markdown("---")
        
        # Check answer button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("✅ Check Answer", use_container_width=True, type="primary"):
                is_correct = game.check_answer()
                if is_correct:
                    st.success("🎉 Correct! Well done!")
                    st.balloons()
                else:
                    # Check if all positions are filled
                    if all(st.session_state.drag_drop_state['user_answers'][pos] is not None 
                           for pos in puzzle['missing_positions']):
                        st.error("❌ Not quite right. Try again!")
                    else:
                        st.warning("⚠️ Please fill in all blank positions first!")
    
    else:
        # Show completed puzzle
        st.success("🎉 Puzzle Solved!")
        
        # Display complete word
        cols = st.columns(len(puzzle['characters']))
        for i, char in enumerate(puzzle['characters']):
            with cols[i]:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    padding: 20px;
                    border-radius: 10px;
                    text-align: center;
                    font-size: 2.5em;
                    color: white;
                    font-family: "Noto Sans Ethiopic", serif;
                    min-height: 80px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                '>
                    {char}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"""
        <div style='
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #e8f4fd 0%, #f0f8ff 100%);
            border-radius: 10px;
            margin: 20px 0;
        '>
            <h2 style='color: #2c3e50; margin: 0;'>{puzzle['word']}</h2>
            <h3 style='color: #666; margin: 10px 0;'>{puzzle['translation']}</h3>
            <p style='color: #888; margin: 0;'>({puzzle['phonetic']})</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("➡️ Next Puzzle", use_container_width=True, type="primary"):
                game.reset_game()
                st.rerun()
    
    # Instructions
    with st.expander("ℹ️ How to Play"):
        st.markdown("""
        ### Instructions:
        1. **Look at the word** with some characters missing (shown as blanks)
        2. **See the translation** and category for hints
        3. **Click on a character** from the available options
        4. **Click on a blank position** to place the character
        5. **Fill all blanks** and click "Check Answer"
        6. **Get immediate feedback** on your answer
        
        ### Difficulty Levels:
        - **Easy:** 1 missing character
        - **Medium:** 2 missing characters
        - **Hard:** 3 missing characters
        
        ### Tips:
        - Use the phonetic transliteration to help you
        - Pay attention to the word category
        - Don't worry about mistakes - you can try again!
        """)

if __name__ == "__main__":
    drag_drop_page()