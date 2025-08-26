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

class ImageLoader:
    """Handles image loading from various sources with caching"""
    
    def __init__(self, images_folder: str = "images"):
        self.images_folder = images_folder
        self._cache = {}
    
    @st.cache_data
    def get_local_image(_self, word: str) -> Optional[Image.Image]:
        """Load image from local folder with caching"""
        if word in _self._cache:
            return _self._cache[word]
        
        if not os.path.exists(_self.images_folder):
            return None
        
        extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
        
        for ext in extensions:
            for case_word in [word, word.lower(), word.upper(), word.title()]:
                image_path = os.path.join(_self.images_folder, f"{case_word}{ext}")
                if os.path.exists(image_path):
                    try:
                        image = Image.open(image_path)
                        _self._cache[word] = image
                        return image
                    except Exception as e:
                        st.error(f"Error loading {image_path}: {e}")
        
        return None
    
    @st.cache_data
    def get_unsplash_image(_self, query: str, width: int = 400, height: int = 300) -> Optional[Image.Image]:
        """Fetch image from Unsplash with error handling"""
        try:
            url = f"https://source.unsplash.com/{width}x{height}/?{query}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
        except Exception as e:
            st.warning(f"Could not load online image for '{query}': {str(e)}")
        return None
    
    def get_image(self, word: str) -> Optional[Image.Image]:
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
                st.info(f"🖼️ No image available for '{word}'")

def search_page():
    """Search and translation page"""
    st.subheader("🔍 Search for a word")
    
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
                st.success("✅ Found in vocabulary!")
                
                # Find category
                category = "Unknown"
                for cat, words in VOCAB_CATEGORIES.items():
                    if search_word in words:
                        category = cat.title()
                        break
                
                st.info(f"📂 Category: {category}")
                
            else:
                with st.spinner(f"Translating '{search_word}' using Google Translate..."):
                    try:
                        translator = GoogleTranslator(source='auto', target='ti')
                        translation = translator.translate(search_word)
                        
                        if translation and translation.lower() != search_word.lower():
                            phonetic = geez_to_latin_syllable(translation)
                            st.success("✅ Online translation successful!")
                            st.warning("⚠️ Not in local vocabulary - accuracy may vary")
                        else:
                            st.error(f"❌ Could not translate '{search_word}'")
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
    st.subheader("📚 Complete Vocabulary Browser")
    
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
    
    st.write(f"📊 Showing {len(sorted_words)} words")
    
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
    st.subheader("🎯 Vocabulary Quiz")
    
    quiz = QuizManager()
    
    # Quiz controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 New Question", type="primary"):
            quiz.generate_question()
    
    with col2:
        quiz_category = st.selectbox(
            "Quiz category:",
            ["all"] + list(VOCAB_CATEGORIES.keys())
        )
    
    with col3:
        if st.button("🔄 Reset Stats", help="Reset all quiz statistics"):
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
            if st.button("✅ Submit Answer"):
                is_correct = quiz.submit_answer(user_answer)
                st.rerun()
        else:
            # Show result
            if user_answer == question['correct_answer']:
                st.success(f"✅ Correct! Great job!")
                if stats['streak'] > 1:
                    st.balloons()
            else:
                st.error(f"❌ Wrong! The correct answer is: **{question['correct_answer']}** ({question['phonetic']})")
            
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
        st.info("👆 Click 'New Question' to start the quiz!")

def statistics_page():
    """Statistics and progress tracking"""
    st.subheader("📊 Learning Statistics")
    
    # Vocabulary statistics
    st.markdown("### 📚 Vocabulary Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Words", len(VOCAB_DICT))
    
    with col2:
        st.metric("Categories", len(VOCAB_CATEGORIES))
    
    with col3:
        avg_length = sum(len(word) for word in VOCAB_DICT.keys()) / len(VOCAB_DICT)
        st.metric("Avg. Word Length", f"{avg_length:.1f}")
    
    # Category breakdown
    st.markdown("### 📂 Category Breakdown")
    
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
        st.markdown("### 🎯 Quiz Performance")
        
        stats = st.session_state.quiz_state
        
        col1, col2 = st.columns(2)
        
        with col1:
            accuracy = (stats['score'] / stats['total']) * 100
            st.metric("Overall Accuracy", f"{accuracy:.1f}%")
            st.metric("Questions Answered", stats['total'])
        
        with col2:
            st.metric("Correct Answers", stats['score'])
            st.metric("Best Streak", stats['best_streak'])

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
    </style>
    """, unsafe_allow_html=True)
    
    # Main title
    st.title("📚 English-Tigrinya Vocabulary Learning App")
    st.markdown("*Learn Tigrinya vocabulary with visual aids and interactive quizzes*")
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    st.sidebar.markdown("Choose a learning mode:")
    
    page = st.sidebar.radio(
        "Choose a page:",
        ["🔍 Search Translation", "📚 Browse Vocabulary", "🎯 Quiz Mode", "📊 Statistics"],
        label_visibility="collapsed"
    )
    
    # Page routing
    if page == "🔍 Search Translation":
        search_page()
    elif page == "📚 Browse Vocabulary":
        browse_page()
    elif page == "🎯 Quiz Mode":
        quiz_page()
    elif page == "📊 Statistics":
        statistics_page()
    
    # Sidebar information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Tips")
    st.sidebar.info(
        "• Use the search to find specific words\n"
        "• Browse vocabulary by category\n"
        "• Take quizzes to test your knowledge\n"
        "• Check statistics to track progress"
    )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ using Streamlit | Enhanced with better UX and features"
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()