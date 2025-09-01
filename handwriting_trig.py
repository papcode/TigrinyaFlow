import streamlit as st
import subprocess
import os
import sys
import json
from pathlib import Path
from manim import *
import platform

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
    """Create a standalone Manim script with reliable handwriting animation"""
    
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
import numpy as np

# Configure Manim
config.disable_caching = True
config.verbosity = "WARNING"

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
                ("{primary_font}", {{"font": "{primary_font}", "font_size": 84}}),
                ("Noto Sans Ethiopic", {{"font": "Noto Sans Ethiopic", "font_size": 84}}),
                ("NotoSansEthiopic-Regular", {{"font": "NotoSansEthiopic-Regular", "font_size": 84}}),
                ("Ebrima", {{"font": "Ebrima", "font_size": 84}}),
                ("Nyala", {{"font": "Nyala", "font_size": 84}}),
                ("Abyssinica SIL", {{"font": "Abyssinica SIL", "font_size": 84}}),
                ("Kefa", {{"font": "Kefa", "font_size": 84}}),
                ("Arial Unicode MS", {{"font": "Arial Unicode MS", "font_size": 84}}),
                ("DejaVu Sans", {{"font": "DejaVu Sans", "font_size": 84}}),
                ("System Default", {{"font_size": 84}}),
                ("Minimal fallback", {{"font_size": 72, "color": "#FFFFFF"}}),
            ]
        else:
            font_attempts = [
                ("{primary_font}", {{"font": "{primary_font}", "font_size": 84}}),
                ("Comic Sans MS", {{"font": "Comic Sans MS", "font_size": 84}}),
                ("Brush Script MT", {{"font": "Brush Script MT", "font_size": 84}}),
                ("Chalkduster", {{"font": "Chalkduster", "font_size": 84}}),
                ("Marker Felt", {{"font": "Marker Felt", "font_size": 84}}),
                ("System Default", {{"font_size": 84}}),
                ("Minimal fallback", {{"font_size": 72, "color": "#FFFFFF"}}),
            ]
        
        # Try to create text object with font fallback
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
            text = Text("Font Error - Check Console", font_size=36, color=RED)
            used_font = "Error - Check console for details"
        
        print(f"Final font used: {{used_font}}")
        
        # Position text in center
        text.move_to(ORIGIN)
        
        # Create handwriting animation
        self.wait(0.5)
        self.create_handwriting_animation(text, text_to_write)
        
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
    
    def create_handwriting_animation(self, full_text, text_string):
        """Create reliable handwriting animation with pen and text reveal"""
        
        # Create individual characters
        characters = []
        char_positions = []
        
        # Calculate character positions
        temp_text = Text(text_string, 
                        font=full_text.font if hasattr(full_text, 'font') else None,
                        font_size=full_text.font_size if hasattr(full_text, 'font_size') else 84)
        temp_text.move_to(ORIGIN)
        
        # Get character width estimation
        single_char_width = temp_text.width / len(text_string.replace(' ', '')) if text_string.replace(' ', '') else 0.5
        
        # Create character objects and positions
        x_offset = temp_text.get_left()[0]
        y_pos = temp_text.get_center()[1]
        
        for i, char in enumerate(text_string):
            if char == ' ':
                # Space - just move position
                characters.append(None)
                char_positions.append([x_offset, y_pos, 0])
                x_offset += single_char_width * 0.6  # Space width
            else:
                # Create character
                char_obj = Text(char, 
                               font=full_text.font if hasattr(full_text, 'font') else None,
                               font_size=full_text.font_size if hasattr(full_text, 'font_size') else 84,
                               color=full_text.color)
                
                char_width = char_obj.width
                char_obj.move_to([x_offset + char_width/2, y_pos, 0])
                
                characters.append(char_obj)
                char_positions.append([x_offset + char_width/2, y_pos, 0])
                x_offset += char_width + 0.05  # Small gap between characters
        
        # Create pen cursor
        pen = self.create_pen()
        
        # Start pen at beginning
        if characters[0] is not None:
            start_pos = characters[0].get_left() + LEFT * 0.3
        else:
            start_pos = char_positions[0] + LEFT * 0.3
        pen.move_to(start_pos)
        
        # Add pen to scene
        self.add(pen)
        
        # Animate writing each character
        written_chars = []
        
        for i, (char, char_obj, pos) in enumerate(zip(text_string, characters, char_positions)):
            if char_obj is not None:
                print(f"Writing character {{i}}: '{{char}}'")
                
                # Move pen to character start
                char_start = char_obj.get_left() + LEFT * 0.1
                char_end = char_obj.get_right() + RIGHT * 0.1
                
                # Move pen to start of character
                self.play(
                    pen.animate.move_to(char_start),
                    run_time=0.15,
                    rate_func=linear
                )
                
                # Write the character with pen movement
                write_time = max(0.5, len(char) * 0.3)
                
                # Simultaneously: move pen across character AND reveal character
                self.play(
                    AnimationGroup(
                        pen.animate.move_to(char_end),
                        Write(char_obj, stroke_width=4, run_time=write_time),
                        lag_ratio=0.0  # Start both at same time
                    ),
                    run_time=write_time,
                    rate_func=smooth
                )
                
                written_chars.append(char_obj)
                
                # Brief pause between characters
                pause_time = np.random.uniform(0.1, 0.25)
                self.wait(pause_time)
                
            elif char == ' ':
                # Handle space - move pen
                space_end = [pos[0] + single_char_width * 0.6, pos[1], 0]
                self.play(
                    pen.animate.move_to(space_end),
                    run_time=0.1
                )
                self.wait(0.15)
        
        # Remove pen with flourish
        self.play(
            pen.animate.scale(0.5).set_opacity(0.3),
            run_time=0.5
        )
        self.remove(pen)
        
        print(f"Successfully wrote {{len(written_chars)}} characters")
    
    def create_pen(self):
        """Create a visible pen cursor"""
        # Create pen tip (the writing point)
        pen_tip = Dot(radius=0.04, color=BLUE)
        
        # Create pen body
        pen_body = Rectangle(
            width=0.03, 
            height=0.2, 
            color=DARK_BLUE,
            fill_opacity=0.8,
            stroke_width=1,
            stroke_color=BLUE
        )
        
        # Position body above tip
        pen_body.next_to(pen_tip, UP, buff=0.01)
        
        # Create pen group and rotate to writing angle
        pen = VGroup(pen_tip, pen_body)
        pen.rotate(PI/6)  # Slight writing angle
        
        # Add a subtle shadow/trail effect
        pen_shadow = pen.copy().set_color(GRAY).set_opacity(0.3)
        pen_shadow.shift(DOWN * 0.02 + RIGHT * 0.02)
        
        pen_with_shadow = VGroup(pen_shadow, pen)
        
        return pen_with_shadow
    
    def create_simple_handwriting(self, full_text, text_string):
        """Fallback: Simple but reliable handwriting animation"""
        print("Using simple handwriting animation")
        
        # Just use Write with enhanced parameters for handwriting feel
        self.play(
            Write(
                full_text,
                stroke_width=4,
                run_time=max(2.0, len(text_string) * 0.3),
                rate_func=smooth,
                lag_ratio=0.8  # Strong left-to-right progression
            ),
            run_time=max(2.0, len(text_string) * 0.3)
        )
'''
    
    # Write the script with UTF-8 encoding
    try:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        return script_path
    except Exception as e:
        st.error(f"Failed to create Manim script: {e}")
        return None
# -------------------------------
# Enhanced Streamlit UI
# -------------------------------
def main():
    st.set_page_config(
        page_title="Tigrinya Handwriting Animation",
        page_icon="✍️",
        layout="wide"
    )
    
    st.title("✍️ Tigrinya Handwriting Animation Generator")
    st.markdown("*Create beautiful handwritten animations for Tigrinya text*")

    # System info in sidebar
    with st.sidebar:
        st.subheader("🖥️ System Info")
        system_info = get_system_info()
        for key, value in system_info.items():
            st.text(f"{key}: {value}")
        
        st.markdown("---")
        
        # Font status check
        with st.spinner("Checking font support..."):
            font_status = check_font_support()
        
        st.subheader("🔤 Font Status")
        
        if font_status['manim_available']:
            st.success("✅ Manim is working")
        else:
            st.error("❌ Manim not available")
            
        if font_status['basic_text_ok']:
            st.success("✅ Basic text rendering OK")
        else:
            st.error("❌ Basic text rendering failed")
            
        if font_status['working_fonts']:
            st.success(f"✅ {len(font_status['working_fonts'])} fonts work for Tigrinya")
            st.write("Working fonts:")
            for font in font_status['working_fonts']:
                st.text(f"  • {font}")
                
            if font_status['best_font']:
                st.info(f"🎯 Recommended: {font_status['best_font']}")
        else:
            st.warning("⚠️ No fonts found for Tigrinya")
            
        if font_status['errors']:
            st.error("❌ Issues detected:")
            for error in font_status['errors']:
                st.text(f"  • {error}")

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📝 Enter Text to Animate")
        
        # Vocabulary selection
        vocab = get_vocabulary()
        
        # Organize vocabulary by category
        categories = {
            "Colors": {k: v for k, v in vocab.items() if k in ["red", "blue", "green", "yellow", "black", "white", "orange", "purple", "brown"]},
            "Animals": {k: v for k, v in vocab.items() if k in ["dog", "cat", "cow", "lion", "horse", "goat", "chicken", "fish", "sheep", "camel", "elephant", "monkey", "zebra", "giraffe", "snake", "tiger", "bear", "donkey", "rabbit", "mouse"]},
            "Things": {k: v for k, v in vocab.items() if k in ["book", "pen", "chair", "table", "car", "bus", "phone", "hat", "shoe", "house", "apple", "banana", "bed", "cup", "key", "door", "bag"]}
        }
        
        # Category tabs
        tab_colors, tab_animals, tab_things, tab_custom = st.tabs(["🎨 Colors", "🐾 Animals", "🏠 Things", "✏️ Custom"])
        
        # Initialize session state for text input
        if "text_to_animate" not in st.session_state:
            st.session_state.text_to_animate = "ሰላም"

        # --- Tabbed interface for selecting text ---
        tab_colors, tab_animals, tab_things, tab_custom = st.tabs(["🎨 Colors", "🐾 Animals", "🏠 Things", "✏️ Custom"])

        # Function to update text
        def set_text(new_text):
            st.session_state.text_to_animate = new_text

        # --- Category Tabs ---
        with tab_colors:
            st.write("Click a color to animate it:")
            cols = st.columns(3)
            for i, (english, tigrinya) in enumerate(categories["Colors"].items()):
                with cols[i % 3]:
                    st.button(f"{tigrinya}\n({english})", key=f"color_{i}", on_click=set_text, args=(tigrinya,))

        with tab_animals:
            st.write("Click an animal to animate it:")
            cols = st.columns(4)
            for i, (english, tigrinya) in enumerate(categories["Animals"].items()):
                with cols[i % 4]:
                    st.button(f"{tigrinya}\n({english})", key=f"animal_{i}", on_click=set_text, args=(tigrinya,))

        with tab_things:
            st.write("Click an object to animate it:")
            cols = st.columns(4)
            for i, (english, tigrinya) in enumerate(categories["Things"].items()):
                with cols[i % 4]:
                    st.button(f"{tigrinya}\n({english})", key=f"thing_{i}", on_click=set_text, args=(tigrinya,))
        
        with tab_custom:
            custom_text = st.text_input(
                "Enter custom text:",
                value=st.session_state.text_to_animate,
                help="Enter any Tigrinya or English text",
                key="custom_text_input"
            )
            # When custom text is used, it becomes the source of truth
            if custom_text != st.session_state.text_to_animate:
                set_text(custom_text)

        # The definitive text to use for animation
        text_input = st.session_state.text_to_animate
        
        if text_input:
            # Character analysis
            has_ethiopic = any('\u1200' <= char <= '\u137F' for char in text_input)
            char_count = len(text_input)
            
            st.info(f"📊 Text: '{text_input}' | Characters: {char_count} | Script: {'Ethiopic' if has_ethiopic else 'Latin'}")

    with col2:
        st.subheader("⚙️ Settings")
        
        quality = st.selectbox(
            "Video Quality",
            ["Low (480p15)", "Medium (720p30)", "High (1080p60)"],
            index=1
        )
        
        animation_speed = st.slider(
            "Animation Speed",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="1.0 = normal speed"
        )
        
        clear_cache = st.checkbox("Clear cache", value=True)
        debug_mode = st.checkbox("Debug output", value=False)

    # Generation section
    st.markdown("---")
    
    if not font_status['manim_available']:
        st.error("⚠️ Cannot generate animations: Manim is not available")
        st.stop()
    
    if not text_input or not text_input.strip():
        st.warning("📝 Please enter some text to animate")
        st.stop()

    # Generate button
    if st.button("🎬 Generate Animation", type="primary", use_container_width=True):
        with st.spinner("🎨 Creating your handwriting animation..."):
            # Clear cache if requested
            if clear_cache:
                media_cache_dir = Path("media")
                if media_cache_dir.exists():
                    import shutil
                    try:
                        shutil.rmtree(media_cache_dir)
                        st.success("🗑️ Cache cleared")
                    except:
                        st.warning("⚠️ Could not clear all cache files")
            
            # Create script
            best_font = font_status.get('best_font')
            script_path = create_manim_script(text_input, best_font)
            
            if not script_path:
                st.error("Failed to create animation script")
                st.stop()
            
            # Output filename
            import hashlib
            text_hash = hashlib.md5(text_input.encode('utf-8')).hexdigest()[:8]
            output_filename = f"tigrinya_animation_{text_hash}.mp4"
            
            # Quality mapping
            quality_flags = {
                "Low (480p15)": ["-ql"],
                "Medium (720p30)": ["-qm"], 
                "High (1080p60)": ["-qh"]
            }
            
            try:
                # Enhanced environment
                env = os.environ.copy()
                env.update({
                    'PYTHONIOENCODING': 'utf-8',
                    'PYTHONUTF8': '1',
                    'MANIM_DISABLE_CACHING': '1' if clear_cache else '0'
                })
                
                # Build command
                cmd = [
                    "python", "-m", "manim"
                ] + quality_flags[quality] + [
                    script_path, "DynamicHandwriting",
                    "-o", output_filename,
                    "--disable_caching" if clear_cache else "--enable_caching"
                ]
                
                if debug_mode:
                    st.info(f"Command: {' '.join(cmd)}")
                
                # Run Manim
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    env=env,
                    encoding='utf-8',
                    errors='replace',
                    timeout=180  # 3 minute timeout
                )
                
                # Show output if requested or if there was an error
                if debug_mode or result.returncode != 0:
                    if result.stdout:
                        st.expander("📝 Manim Output").code(result.stdout)
                    if result.stderr:
                        st.expander("⚠️ Manim Errors").code(result.stderr)
                
                if result.returncode != 0:
                    st.error(f"❌ Animation generation failed (code {result.returncode})")
                    st.error("Check the debug output above for details")
                    st.stop()
                
                # Find generated video
                quality_paths = {
                    "Low (480p15)": "480p15",
                    "Medium (720p30)": "720p30",
                    "High (1080p60)": "1080p60"
                }
                
                quality_dir = quality_paths[quality]
                
                possible_paths = [
                    Path("media/videos/dynamic_handwriting") / quality_dir / output_filename,
                    Path("media/videos/dynamic_handwriting") / "720p30" / output_filename,
                    Path("media/videos/dynamic_handwriting") / "480p15" / output_filename,
                ]
                
                found_file = None
                for path in possible_paths:
                    if path.exists():
                        found_file = str(path)
                        break
                
                # Also check Manim output for file location
                if not found_file and result.stdout:
                    for line in result.stdout.split('\n'):
                        if "File ready at" in line and "'" in line:
                            try:
                                file_path = line.split("'")[1]
                                if os.path.exists(file_path):
                                    found_file = file_path
                                    break
                            except:
                                continue
                
                # Display results
                if found_file:
                    st.success("🎉 Animation created successfully!")
                    
                    # Show video
                    st.video(found_file)
                    
                    # Show info
                    try:
                        file_size = os.path.getsize(found_file) / (1024 * 1024)
                        st.info(f"📁 File: {Path(found_file).name} ({file_size:.2f} MB)")
                    except:
                        pass
                    
                    # Font info from output
                    if result.stdout:
                        if "SUCCESS: Text created with" in result.stdout:
                            for line in result.stdout.split('\n'):
                                if "SUCCESS: Text created with" in line:
                                    font_used = line.split("SUCCESS: Text created with ")[-1]
                                    st.success(f"🔤 Font used: {font_used}")
                                    break
                    
                    # Download button
                    try:
                        with open(found_file, 'rb') as f:
                            video_bytes = f.read()
                        
                        st.download_button(
                            "⬇️ Download Video",
                            data=video_bytes,
                            file_name=f"tigrinya_handwriting_{text_input[:10]}.mp4",
                            mime="video/mp4"
                        )
                    except Exception as e:
                        st.warning(f"Download button failed: {e}")
                
                else:
                    st.error("❌ Could not find the generated video file")
                    st.error("Enable debug mode and try again for more details")
                
            except subprocess.TimeoutExpired:
                st.error("⏰ Animation generation timed out (3 minutes)")
            except Exception as e:
                st.error(f"💥 Error during generation: {e}")
            finally:
                # Cleanup script
                try:
                    if script_path and os.path.exists(script_path):
                        os.remove(script_path)
                except:
                    pass

    # Help section
    with st.expander("❓ Help & Tips"):
        st.markdown("""
        **🎯 Tips for best results:**
        - Install Noto Sans Ethiopic font for proper Tigrinya rendering
        - Start with short words before trying longer text
        - Use Medium quality for best balance of speed and quality
        - Enable debug mode if you encounter issues
        
        **🔧 Troubleshooting:**
        - If no fonts work: Install Noto Sans Ethiopic from Google Fonts
        - If animations fail: Try clearing cache and using Lower quality
        - If text appears as boxes: Font installation issue
        
        **📚 Supported:**
        - Tigrinya (ትግርኛ), Amharic (አማርኛ), Geez (ግዕዝ)
        - English and other Latin scripts
        - Mixed text (Tigrinya + English)
        """)

if __name__ == "__main__":
    main()   
    
    '''("Minimal fallback", {{"font_size": 72, "color": "#FFFFFF"}}),
            ]
        else:
            # For Latin text
            font_attempts = [
                ("{primary_font}", {{"font": "{primary_font}", "font_size": 84}}),
                ("Comic Sans MS", {{"font": "Comic Sans MS", "font_size": 84}}),
                ("Brush Script MT", {{"font": "Brush Script MT", "font_size": 84}}),
                ("Chalkduster", {{"font": "Chalkduster", "font_size": 84}}),
                ("Marker Felt", {{"font": "Marker Felt", "font_size": 84}}),
                ("System Default", {{"font_size": 84}}),'''