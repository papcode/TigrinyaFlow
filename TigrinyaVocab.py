import streamlit as st
import subprocess
import os
import sys
import json
from pathlib import Path
from manim import *
import platform
from PIL import Image
import glob
import requests
from io import BytesIO

# -------------------------------
# Environment setup for Unicode support
# -------------------------------
def setup_unicode_environment():
    """Set up environment variables for proper Unicode handling"""
    env_vars = {
        'PYTHONIOENCODING': 'utf-8',
        'PYTHONUTF8': '1',
    }
    
    # On Windows, also try to set console to UTF-8
    if platform.system() == 'Windows':
        env_vars.update({
            'LC_ALL': 'en_US.UTF-8',
            'LANG': 'en_US.UTF-8'
        })
        try:
            os.system('chcp 65001 > nul 2>&1')
        except:
            pass
    else:
        env_vars.update({
            'LC_ALL': 'C.UTF-8',
            'LANG': 'C.UTF-8'
        })
    
    # Update environment
    for key, value in env_vars.items():
        os.environ[key] = value
    
    return env_vars

# Set up Unicode environment
setup_unicode_environment()

# -------------------------------
# Vocabulary dictionary
# -------------------------------
def get_vocabulary():
    """Get the Tigrinya vocabulary dictionary"""
    return {
        # Colors
        "red": "ቀይሕ",
        "blue": "ሰማያዊ", 
        "green": "ቀጠልያ",
        "yellow": "ቢጫ",
        "black": "ጸሊም",
        "white": "ጻዕዳ",
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

# -------------------------------
# Improved font checking
# -------------------------------
def check_font_support():
    """Check font support with better error handling"""
    try:
        # Test basic Manim functionality first
        test_code = '''
import os
os.environ["PYTHONIOENCODING"] = "utf-8"

try:
    from manim import Text, config
    config.disable_caching = True
    
    # Test basic text
    test_basic = Text("Hello", font_size=48)
    print("BASIC_OK")
    
    # Test Tigrinya text with different fonts
    test_text = "ሰላም"
    
    fonts_to_test = [
        "Noto Sans Ethiopic",
        "Ebrima", 
        "Nyala",
        "Arial Unicode MS",
        None  # System default
    ]
    
    working_fonts = []
    
    for font in fonts_to_test:
        try:
            font_kwargs = {"font_size": 48}
            if font:
                font_kwargs["font"] = font
            
            text_obj = Text(test_text, **font_kwargs)
            font_name = font if font else "System Default"
            working_fonts.append(font_name)
            print(f"FONT_OK:{font_name}")
            
        except Exception as e:
            font_name = font if font else "System Default"
            print(f"FONT_ERROR:{font_name}:{str(e)[:100]}")
    
    if working_fonts:
        print(f"BEST_FONT:{working_fonts[0]}")
    else:
        print("NO_WORKING_FONTS")
        
except ImportError as e:
    print(f"MANIM_IMPORT_ERROR:{str(e)}")
except Exception as e:
    print(f"GENERAL_ERROR:{str(e)}")
'''
        
        result = subprocess.run(
            [sys.executable, '-c', test_code],
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8',
            errors='replace',
            env=os.environ
        )
        
        output_lines = result.stdout.strip().split('\n')
        
        status = {
            'manim_available': False,
            'basic_text_ok': False,
            'working_fonts': [],
            'best_font': None,
            'errors': []
        }
        
        for line in output_lines:
            if 'BASIC_OK' in line:
                status['basic_text_ok'] = True
                status['manim_available'] = True
            elif line.startswith('FONT_OK:'):
                font_name = line.split(':', 1)[1]
                status['working_fonts'].append(font_name)
            elif line.startswith('BEST_FONT:'):
                status['best_font'] = line.split(':', 1)[1]
            elif line.startswith('FONT_ERROR:'):
                error_info = line.split(':', 2)
                if len(error_info) >= 3:
                    status['errors'].append(f"{error_info[1]}: {error_info[2]}")
            elif 'MANIM_IMPORT_ERROR' in line:
                status['errors'].append("Manim import failed")
            elif 'NO_WORKING_FONTS' in line:
                status['errors'].append("No fonts can render Tigrinya text")
        
        if result.stderr:
            status['errors'].append(f"Process error: {result.stderr[:200]}")
        
        return status
        
    except subprocess.TimeoutExpired:
        return {
            'manim_available': False,
            'basic_text_ok': False,
            'working_fonts': [],
            'best_font': None,
            'errors': ['Font check timed out']
        }
    except Exception as e:
        return {
            'manim_available': False,
            'basic_text_ok': False,
            'working_fonts': [],
            'best_font': None,
            'errors': [f'Font check failed: {str(e)}']
        }

def get_system_info():
    """Get system information for better font handling"""
    return {
        'system': platform.system(),
        'machine': platform.machine(),
        'python_version': platform.python_version(),
        'encoding': sys.getdefaultencoding(),
        'fs_encoding': sys.getfilesystemencoding(),
    }

# -------------------------------
# Improved Manim script creation
# -------------------------------
def create_manim_script(text_to_animate, best_font=None, script_path="dynamic_handwriting.py"):
    """Create a standalone Manim script with improved font handling"""
    
    # Check if text contains Ethiopic characters
    def contains_ethiopic(text):
        for char in text:
            if '\u1200' <= char <= '\u137F' or '\u1380' <= char <= '\u139F' or '\u2D80' <= char <= '\u2DDF':
                return True
        return False
    
    # Use repr() to safely encode the text with proper escaping
    safe_text_code = repr(text_to_animate)
    is_ethiopic = contains_ethiopic(text_to_animate)
    
    # Font strategy based on detection results
    if best_font:
        primary_font = best_font
    else:
        primary_font = "Noto Sans Ethiopic" if is_ethiopic else "Comic Sans MS"
    
    script_content = f'''# -*- coding: utf-8 -*-
import os
import sys

# Set up Unicode environment
os.environ.update({{
    "PYTHONIOENCODING": "utf-8",
    "PYTHONUTF8": "1",
    "LC_ALL": "C.UTF-8" if os.name != "nt" else "en_US.UTF-8",
    "LANG": "C.UTF-8" if os.name != "nt" else "en_US.UTF-8"
}})

from manim import *

# Configure Manim
config.disable_caching = True
config.verbosity = "WARNING"  # Reduce output noise

class DynamicHandwriting(Scene):
    def construct(self):
        # Text to animate (safely encoded)
        text_to_write = {safe_text_code}
        
        print(f"Animating text: {{repr(text_to_write)}}")
        print(f"Character count: {{len(text_to_write)}}")
        print(f"Contains Ethiopic script: {is_ethiopic}")
        print(f"Primary font target: {primary_font}")
        
        # Comprehensive font fallback strategy
        if {is_ethiopic}:
            font_attempts = [
                # Best font first if detected
                ("{primary_font}", {{"font": "{primary_font}", "font_size": 150}}),
                
                # Other Ethiopic fonts
                ("Noto Sans Ethiopic", {{"font": "Noto Sans Ethiopic", "font_size": 150}}),
                ("NotoSansEthiopic-Regular", {{"font": "NotoSansEthiopic-Regular", "font_size": 150}}),
                ("Ebrima", {{"font": "Ebrima", "font_size": 150}}),
                ("Nyala", {{"font": "Nyala", "font_size": 150}}),
                ("Abyssinica SIL", {{"font": "Abyssinica SIL", "font_size": 150}}),
                ("Kefa", {{"font": "Kefa", "font_size": 150}}),
                ("Arial Unicode MS", {{"font": "Arial Unicode MS", "font_size": 150}}),
                ("DejaVu Sans", {{"font": "DejaVu Sans", "font_size": 150}}),
                
                # System fallbacks
                ("System Default", {{"font_size": 150}}),
                ("Minimal fallback", {{"font_size": 150, "color": "#FFFFFF"}}),
            ]



        
        text = None
        used_font = "Unknown"
        font_error_details = []
        
        for font_name, font_kwargs in font_attempts:
            try:
                print(f"Attempting font: {{font_name}}")
                text = Text(text_to_write, **font_kwargs)
                used_font = font_name
                print(f"SUCCESS: Text created with {{font_name}}")
                break
            except Exception as e:
                error_msg = str(e)
                print(f"FAILED {{font_name}}: {{error_msg}}")
                font_error_details.append(f"{{font_name}}: {{error_msg}}")
                continue
        
        if text is None:
            print("All font attempts failed!")
            print("Font errors:", font_error_details)
            # Create a simple error message
            text = Text("Font Error - Check Console", font_size=36, color=RED)
            used_font = "Error - Check console for details"
        
        print(f"Final font used: {{used_font}}")
        
        # Position text in center
        text.move_to(ORIGIN)
        
        # Create the handwriting animation
        self.wait(0.5)
        
        # Use Write animation with handwriting-like parameters
        self.play(
            Write(
                text, 
                stroke_width=3,
                run_time=max(3, len(text_to_write) * 0.5),  # Dynamic timing
                rate_func=smooth,
                lag_ratio=0.1  # Slight delay between characters
            ),
            run_time=max(3, len(text_to_write) * 0.5)
        )
        
        # Add a subtle finishing touch
        self.wait(0.5)
        self.play(
            text.animate.set_stroke(width=2).scale(1.05), 
            run_time=0.8,
            rate_func=there_and_back
        )
        self.wait(1.5)
        
        print("Animation completed successfully")
        print(f"Final status - Font: {{used_font}}, Characters: {{len(text_to_write)}}")
'''
    
    # Write the script with UTF-8 encoding
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        return script_path
    except Exception as e:
        st.error(f"Failed to create Manim script: {e}")
        return None

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

def main():
    st.set_page_config(
        page_title="Tigrinya Vocabulary Learning App",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 English-Tigrinya Vocabulary Learning App")
    st.markdown("*Learn Tigrinya vocabulary with visual aids and handwriting animations*")

    vocab_dict = get_vocabulary()

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    mode = st.sidebar.radio(
        "Choose mode:",
        ["Search Translation", "Browse All Words", "Quiz Mode"]
    )

    if mode == "Search Translation":
        st.subheader("🔍 Search for a word")
        
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
            
            # Display image
            
            image = get_local_image(search_word) or get_image_from_unsplash(search_word)
            if image:
                st.image(
                    image,
                    width=400
                )
            else:
                st.warning("Could not load image.")

            

            # Generate animation
            with st.spinner("loading Tigrinya Translation"):
                font_status = check_font_support()
                best_font = font_status.get('best_font')
                script_path = create_manim_script(translation, best_font)
                
                if not script_path:
                    st.error("Failed to create animation script")
                    st.stop()

                import hashlib
                text_hash = hashlib.md5(translation.encode('utf-8')).hexdigest()[:8]
                output_filename = f"tigrinya_animation_{text_hash}.mp4"
                
                quality_flags = ["-qm"] # Medium quality

                try:
                    env = os.environ.copy()
                    env.update({
                        'PYTHONIOENCODING': 'utf-8',
                        'PYTHONUTF8': '1',
                        'MANIM_DISABLE_CACHING': '1'
                    })
                    
                    cmd = [
                        "python", "-m", "manim"
                    ] + quality_flags + [
                        script_path, "DynamicHandwriting",
                        "-o", output_filename,
                        "--disable_caching"
                    ]
                    
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        env=env,
                        encoding='utf-8',
                        errors='replace',
                        timeout=180
                    )
                    
                    if result.returncode != 0:
                        st.error(f"❌ Animation generation failed (code {result.returncode})")
                        st.expander("⚠️ Manim Errors").code(result.stderr)
                        st.stop()
                    
                    quality_dir = "720p30"
                    
                    possible_paths = [
                        Path("media/videos/dynamic_handwriting") / quality_dir / output_filename,
                    ]
                    
                    found_file = None
                    for path in possible_paths:
                        if path.exists():
                            found_file = str(path)
                            break
                    
                    if found_file:
                            st.video(found_file, width=400, autoplay=True)
                    else:
                        st.error("❌ Could not find the generated video file")
                        
                except subprocess.TimeoutExpired:
                    st.error("⏰ Animation generation timed out (3 minutes)")
                except Exception as e:
                    st.error(f"💥 Error during generation: {e}")
                finally:
                    try:
                        if script_path and os.path.exists(script_path):
                            os.remove(script_path)
                    except:
                        pass
        elif search_word:
            st.error(f"❌ '{search_word}' not found in vocabulary.")

    elif mode == "Browse All Words":
        st.subheader("📋 Complete Vocabulary List")
        
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
        
        import random
        
        if st.button("🎲 Generate New Question"):
            word = random.choice(list(vocab_dict.keys()))
            correct_translation = vocab_dict[word]
            
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
                
                with st.spinner("Loading image..."):
                    image = get_image_from_unsplash(st.session_state.current_word)
                    if image:
                        st.image(image, caption=f"{st.session_state.current_word.title()}", width=300)
        
        if st.session_state.quiz_total > 0:
            accuracy = (st.session_state.quiz_score / st.session_state.quiz_total) * 100
            st.metric("Quiz Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}", f"{accuracy:.1f}% accuracy")

    st.markdown("---")
    st.markdown("*Built with ❤️ using Streamlit*")

if __name__ == "__main__":
    main()
