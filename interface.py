import streamlit as st
import os
from PIL import Image
import glob
import requests
from io import BytesIO

# Vocabulary dictionary from your PDF
vocab_dict = {
    # Colors
    "red": "ቀይሕ",
    "blue": "ሰማያዊ",
    "green": "ቀጠልያ",
    "yellow": "ቢጫ",
    "black": "ጸሊም",
    "white": "ቀይሕ",
    "orange": "ኣራንቾኒ",
    "purple": "ሊላ",
    "brown": "ቡናዊ",
    
    # Animals
    "dog": "ከልቢ",
    "cat": "ድሙ",
    "cow": "ላም",
    "lion": "ኣንበሳ",
    "horse": "ፈረስ",
    "goat": "ጤል",
    "chicken": "ዶርሆ",
    "fish": "ዓሳ",
    "sheep": "በጊዕ",
    "camel": "ገመል",
    "elephant": "ሓርማዝ",
    "monkey": "ህበይ",
    "zebra": "ኣድጊ በረኻ",
    "giraffe": "ዘራፍ",
    "snake": "ተመን",
    "tiger": "ነብሪ",
    "bear": "ድቢ",
    "donkey": "ኣድጊ",
    "rabbit": "ማንቲለ",
    "mouse": "ኣንጭዋ",
    
    # Things
    "book": "መጽሓፍ",
    "pen": "ብርዒ",
    "chair": "ኩርሲ",
    "table": "ጣውላ",
    "car": "መኪና",
    "bus": "ኣውቶቡስ",
    "phone": "ተሌፎን",
    "hat": "ቆብዕ",
    "shoe": "ሳእኒ",
    "house": "ገዛ",
    "apple": "ቱፋሕ",
    "banana": "ባናና",
    "bed": "ዓራት",
    "cup": "ቢኬሪ",
    "key": "መፍትሕ",
    "door": "ማዕጾ",
    "bag": "ቦርሳ",
}

def get_image_from_unsplash(query, width=400, height=300):
    """
    Fetch image from Unsplash API (free tier)
    You'll need to sign up at https://unsplash.com/developers and get an access key
    """
    # For demo purposes, using a placeholder service
    # Replace with actual Unsplash API when you have a key
    placeholder_url = f"https://source.unsplash.com/{width}x{height}/?{query}"
    try:
        response = requests.get(placeholder_url, timeout=10)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"Error loading image: {e}")
    return None

def get_image_from_picsum(query, width=400, height=300):
    """
    Fallback to Lorem Picsum for placeholder images
    """
    try:
        # Using a hash of the query to get consistent images
        seed = hash(query) % 1000
        url = f"https://picsum.photos/{width}/{height}?random={seed}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"Error loading fallback image: {e}")
    return None

def get_local_image(word, images_folder="images"):
    """
    Load image from local images folder
    Supports common image formats: png, jpg, jpeg, gif, bmp, webp
    """
    if not os.path.exists(images_folder):
        st.warning(f"Images folder '{images_folder}' not found!")
        return None
    
    # Common image extensions to check
    extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.webp', 
                  '*.PNG', '*.JPG', '*.JPEG', '*.GIF', '*.BMP', '*.WEBP']
    
    # Look for image file with the word name
    for ext in extensions:
        pattern = os.path.join(images_folder, f"{word}{ext[1:]}")  # Remove the *
        if os.path.exists(pattern):
            try:
                return Image.open(pattern)
            except Exception as e:
                st.error(f"Error loading image {pattern}: {e}")
                continue
    
    # If exact match not found, try pattern matching
    for ext in extensions:
        pattern = os.path.join(images_folder, f"{word}.*")
        matches = glob.glob(pattern)
        if matches:
            try:
                return Image.open(matches[0])  # Use first match
            except Exception as e:
                st.error(f"Error loading image {matches[0]}: {e}")
                continue
    
    return None

def list_available_images(images_folder="images"):
    """
    List all available images in the folder for debugging
    """
    if not os.path.exists(images_folder):
        return []
    
    extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.webp', 
                  '*.PNG', '*.JPG', '*.JPEG', '*.GIF', '*.BMP', '*.WEBP']
    
    all_images = []
    for ext in extensions:
        pattern = os.path.join(images_folder, ext)
        all_images.extend(glob.glob(pattern))
    
    # Extract just the filename without extension
    image_names = [os.path.splitext(os.path.basename(img))[0].lower() for img in all_images]
    return image_names

def main():
    st.set_page_config(
        page_title="Tigrinya Vocabulary Learning App",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 English-Tigrinya Vocabulary Learning App")
    st.markdown("*Learn Tigrinya vocabulary with visual aids*")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    mode = st.sidebar.radio(
        "Choose mode:",
        ["Search Translation", "Browse All Words", "Quiz Mode"]
    )
    
    if mode == "Search Translation":
        # Main search interface
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔍 Search for a word")
            
            # Input methods
            input_method = st.radio("Input method:", ["Type word", "Select from dropdown"])
            
            if input_method == "Type word":
                search_word = st.text_input(
                    "Enter English word:",
                    placeholder="e.g., house, cat, red..."
                ).lower().strip()
            else:
                search_word = st.selectbox(
                    "Select English word:",
                    options=[""] + sorted(vocab_dict.keys())
                )
            
            if search_word and search_word in vocab_dict:
                translation = vocab_dict[search_word]
                
                st.success(f"✅ Translation found!")
                
                # Display translation with larger font
                st.markdown(f"""
                <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 10px 0;'>
                    <h2 style='color: #1f77b4; margin: 0;'>{search_word.title()}</h2>
                    <h1 style='color: #ff6347; margin: 10px 0; font-size: 4.2em;'>{translation}</h1>
                </div>
                """, unsafe_allow_html=True)
                
                # Audio pronunciation placeholder
                # st.info("🔊 Audio pronunciation feature coming soon!")
                
            elif search_word and search_word not in vocab_dict:
                st.error(f"❌ '{search_word}' not found in vocabulary.")
                st.info("💡 Try one of these words: " + ", ".join(list(vocab_dict.keys())[:10]) + "...")
        
        with col2:
            if search_word and search_word in vocab_dict:                
                with st.spinner("Loading image..."):
                    image = get_local_image(search_word)
                    
                    if image:
                        st.image(
                            image,
                            use_container_width=True
                        )
                        st.markdown(f"<div style='text-align: center; font-size: 2em;'>{search_word.title()} - {vocab_dict[search_word]}</div>", unsafe_allow_html=True)
                    else:
                        st.warning("Could not load image. Please try again.")
    
    elif mode == "Browse All Words":
        st.subheader("📋 Complete Vocabulary List")
        
        # Category filter
        categories = {
            "All": vocab_dict.keys(),
            "Colors": ["red", "blue", "green", "yellow", "black", "white", "orange", "purple", "brown"],
            "Animals": ["dog", "cat", "cow", "lion", "horse", "goat", "chicken", "fish", "sheep", 
                       "camel", "elephant", "monkey", "zebra", "giraffe", "snake", "tiger", 
                       "bear", "donkey", "rabbit", "mouse"],
            "Things": ["book", "pen", "chair", "table", "car", "bus", "phone", "hat", "shoe", 
                      "house", "apple", "banana", "bed", "cup", "key", "door", "bag"]
        }
        
        selected_category = st.selectbox("Filter by category:", categories.keys())
        words_to_show = categories[selected_category]
        
        # Display in a nice table format
        cols = st.columns(3)
        for i, word in enumerate(sorted(words_to_show)):
            if word in vocab_dict:
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style='background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin: 5px 0; border-left: 4px solid #1f77b4;'>
                        <strong style='color: #1f77b4;'>{word.title()}</strong><br>
                        <span style='font-size: 1.5em; color: #ff6347;'>{vocab_dict[word]}</span>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif mode == "Quiz Mode":
        st.subheader("🎯 Test Your Knowledge")
        
        if 'quiz_score' not in st.session_state:
            st.session_state.quiz_score = 0
            st.session_state.quiz_total = 0
        
        # Simple quiz implementation
        import random
        
        if st.button("🎲 Generate New Question"):
            word = random.choice(list(vocab_dict.keys()))
            correct_translation = vocab_dict[word]
            
            # Create multiple choice options
            wrong_answers = random.sample([v for k, v in vocab_dict.items() if k != word], 3)
            options = [correct_translation] + wrong_answers
            random.shuffle(options)
            
            st.session_state.current_word = word
            st.session_state.correct_answer = correct_translation
            st.session_state.options = options
        
        if hasattr(st.session_state, 'current_word'):
            st.markdown(f"### What is the Tigrinya translation for: **{st.session_state.current_word.title()}**?")
            
            user_answer = st.radio("Choose the correct translation:", st.session_state.options)
            
            if st.button("Submit Answer"):
                st.session_state.quiz_total += 1
                if user_answer == st.session_state.correct_answer:
                    st.success("✅ Correct!")
                    st.session_state.quiz_score += 1
                else:
                    st.error(f"❌ Wrong! The correct answer is: {st.session_state.correct_answer}")
                
                # Show image for the word
                with st.spinner("Loading image..."):
                    image = get_image_from_unsplash(st.session_state.current_word)
                    if image:
                        st.image(image, caption=f"{st.session_state.current_word.title()}", width=300)
        
        # Display score
        if st.session_state.quiz_total > 0:
            accuracy = (st.session_state.quiz_score / st.session_state.quiz_total) * 100
            st.metric("Quiz Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}", f"{accuracy:.1f}% accuracy")
    
    # Footer
    st.markdown("---")
    st.markdown("*Built with ❤️ using Streamlit | Images from Unsplash*")

if __name__ == "__main__":
    main()