import streamlit as st
import subprocess
import os
import sys
import json
from pathlib import Path
from manim import *
import platform

# -------------------------------
# Font checking and installation helper
# -------------------------------
def check_noto_font_installed():
    """Check if Noto Sans Ethiopic is installed on the system"""
    try:
        # Try to create a test text object to see if font works
        result = subprocess.run([
            "python", "-c", 
            """
from manim import Text
try:
    test = Text('ገ', font='Noto Sans Ethiopic', font_size=48)
    print('FONT_OK')
except Exception as e:
    print(f'FONT_ERROR: {str(e)}')
"""
        ], capture_output=True, text=True, timeout=10)
        
        return "FONT_OK" in result.stdout
    except:
        return False

def get_system_info():
    """Get system information for better font handling"""
    return {
        'system': platform.system(),
        'machine': platform.machine(),
        'python_version': platform.python_version()
    }

# -------------------------------
# Create a more robust Manim script
# -------------------------------
def create_manim_script(text_to_animate, script_path="dynamic_handwriting.py"):
    """Create a standalone Manim script with better font fallback handling"""
    
    # Check if text contains Ethiopic characters
    def contains_ethiopic(text):
        for char in text:
            if '\u1200' <= char <= '\u137F' or '\u1380' <= char <= '\u139F' or '\u2D80' <= char <= '\u2DDF':
                return True
        return False
    
    # Use repr() to safely encode the text with proper escaping
    safe_text_code = repr(text_to_animate)
    is_ethiopic = contains_ethiopic(text_to_animate)
    
    script_content = f'''# -*- coding: utf-8 -*-
from manim import *
import sys
import os

# Configure Manim for better font handling
config.disable_caching = True  # Disable caching to ensure fresh font rendering

class DynamicHandwriting(Scene):
    def construct(self):
        try:
            print("Starting handwriting animation generation...")
            print(f"Text contains {{len({safe_text_code})}} characters")
            print(f"Is Ethiopic script: {is_ethiopic}")
        except UnicodeEncodeError:
            print("Unicode encoding issue detected")
        
        # Text to animate (safely encoded)
        text_to_write = {safe_text_code}
        
        # Comprehensive font fallback strategy for Ethiopic text
        if {is_ethiopic}:
            font_attempts = [
                # Primary Noto fonts (most reliable for Ethiopic)
                ("Noto Sans Ethiopic", {{"font": "Noto Sans Ethiopic", "font_size": 96}}),
                ("NotoSansEthiopic-Regular", {{"font": "NotoSansEthiopic-Regular", "font_size": 96}}),
                ("Noto Sans Ethiopic Regular", {{"font": "Noto Sans Ethiopic Regular", "font_size": 96}}),
                
                # Alternative Ethiopic fonts
                ("Ebrima", {{"font": "Ebrima", "font_size": 96}}),
                ("Nyala", {{"font": "Nyala", "font_size": 96}}),
                ("Abyssinica SIL", {{"font": "Abyssinica SIL", "font_size": 96}}),
                ("Kefa", {{"font": "Kefa", "font_size": 96}}),  # macOS
                
                # System defaults with language hint
                ("Arial Unicode MS", {{"font": "Arial Unicode MS", "font_size": 96}}),
                ("DejaVu Sans", {{"font": "DejaVu Sans", "font_size": 96}}),
                
                # Fallback to system default
                ("System Default", {{"font_size": 96}}),
                
                # Last resort with explicit weight
                ("Fallback Arial", {{"font": "Arial", "weight": "NORMAL", "font_size": 96}})
            ]
        else:
            # For Latin text, use more stylistic fonts
            font_attempts = [
                ("Comic Sans MS", {{"font": "Comic Sans MS", "font_size": 96}}),
                ("Brush Script MT", {{"font": "Brush Script MT", "font_size": 96}}),
                ("Chalkduster", {{"font": "Chalkduster", "font_size": 96}}),  # macOS
                ("System Default", {{"font_size": 96}}),
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
            text = Text("Font rendering failed", font_size=48, color=RED)
            used_font = "Error - Check console for details"
        
        print(f"Final font used: {{used_font}}")
        
        # Check if text is actually renderable (not just boxes)
        try:
            # This will help identify if we're getting box characters
            print(f"Text object created successfully")
            print(f"Text contains {{len(text_to_write)}} characters")
            
            # Add some debugging info about the rendered text
            if hasattr(text, 'text'):
                print(f"Rendered text property: {{repr(text.text)}}")
            
        except Exception as e:
            print(f"Text object inspection failed: {{e}}")
        
        # Create the animation
        self.wait(0.5)
        
        # Use a slower, more dramatic write animation for handwriting effect
        self.play(
            Write(text, stroke_width=2, run_time=5, rate_func=smooth),
            run_time=5
        )
        
        # Add a small fade effect at the end for polish
        self.wait(0.5)
        self.play(text.animate.set_opacity(0.9), run_time=0.5)
        self.wait(1)
        
        print("Animation rendering completed successfully")
        print(f"Final status - Font: {{used_font}}")
'''
    
    # Write the script with UTF-8 encoding and BOM for better compatibility
    with open(script_path, 'w', encoding='utf-8-sig') as f:
        f.write(script_content)
    
    return script_path

# -------------------------------
# Enhanced Streamlit UI
# -------------------------------
st.title("✍️ Enhanced Tigrinya Handwriting Animation")

# System info display
system_info = get_system_info()
with st.expander("🖥️ System Information"):
    st.json(system_info)

# Font status check
font_installed = check_noto_font_installed()
if font_installed:
    st.success("✅ **Noto Sans Ethiopic font is available!**")
else:
    st.warning("⚠️ **Noto Sans Ethiopic font may not be properly installed**")
    
    with st.expander("📥 Font Installation Guide"):
        st.markdown("""
        **To fix Tigrinya character display issues:**
        
        **Windows:**
        1. Download Noto Sans Ethiopic from [Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+Ethiopic)
        2. Extract the .ttf files
        3. Right-click each .ttf file and select "Install"
        4. Restart your application
        
        **macOS:**
        1. Download the font files
        2. Double-click each .ttf file and click "Install Font"
        3. Restart your application
        
        **Linux:**
        ```bash
        # Ubuntu/Debian
        sudo apt install fonts-noto
        
        # Or manually:
        wget https://noto-website-2.storage.googleapis.com/pkgs/NotoSansEthiopic-hinted.zip
        unzip NotoSansEthiopic-hinted.zip
        sudo cp *.ttf /usr/share/fonts/truetype/
        sudo fc-cache -f -v
        ```
        """)

# Input text with better examples
st.subheader("Enter Text to Animate")
text_input = st.text_input(
    "Text:", 
    "ሰላም", 
    help="Try Tigrinya examples: ሰላም (hello), ገዛ (house), ትግርኛ (Tigrinya)"
)

# Provide better examples
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("ሰላም (Hello)"):
        text_input = "ሰላም"
        st.rerun()

with col2:
    if st.button("ትግርኛ (Tigrinya)"):
        text_input = "ትግርኛ"
        st.rerun()

with col3:
    if st.button("ገዛ (House)"):
        text_input = "ገዛ"
        st.rerun()

# Character detection info
if text_input:
    has_ethiopic = any('\u1200' <= char <= '\u137F' for char in text_input)
    if has_ethiopic:
        st.info("🔤 **Ethiopic script detected** - Will use Noto Sans Ethiopic font")
    else:
        st.info("🔤 **Latin script detected** - Will use Comic Sans MS font")

# Advanced options
with st.expander("🔧 Advanced Options"):
    quality = st.selectbox(
        "Video Quality",
        ["Low (480p15)", "Medium (720p30)", "High (1080p60)"],
        index=1
    )
    
    clear_cache = st.checkbox("Clear cache before rendering", value=True)
    
    debug_mode = st.checkbox("Enable debug output", value=False)

# Main generation button
if st.button("🎬 Generate Animation", type="primary"):
    if not text_input.strip():
        st.error("Please enter some text to animate!")
    else:
        with st.spinner("🎨 Creating your handwriting animation..."):
            # Clear cache if requested
            if clear_cache:
                media_cache_dir = Path("media/videos/dynamic_handwriting")
                if media_cache_dir.exists():
                    import shutil
                    shutil.rmtree(media_cache_dir)
                    st.info("🗑️ Cleared animation cache")
            
            # Create dynamic script
            script_path = "dynamic_handwriting.py"
            create_manim_script(text_input, script_path)
            
            # Output filename
            output_filename = f"tigrinya_handwriting_{hash(text_input) % 10000}.mp4"
            
            # Quality mapping
            quality_flags = {
                "Low (480p15)": "-ql",
                "Medium (720p30)": "-qm", 
                "High (1080p60)": "-qh"
            }
            
            try:
                # Enhanced environment setup
                env = os.environ.copy()
                env.update({
                    'PYTHONIOENCODING': 'utf-8',
                    'PYTHONUTF8': '1',
                    'LC_ALL': 'C.UTF-8',
                    'LANG': 'C.UTF-8'
                })
                
                # Run Manim with selected quality
                quality_flag = quality_flags[quality]
                cmd = [
                    "manim", quality_flag, script_path, "DynamicHandwriting", 
                    "-o", output_filename, "--disable_caching"
                ]
                
                st.info(f"Running: {' '.join(cmd)}")
                
                result = subprocess.run(
                    cmd,
                    capture_output=True, 
                    text=True, 
                    env=env, 
                    encoding='utf-8', 
                    errors='replace',
                    timeout=120  # 2 minute timeout
                )
                
                # Display output for debugging
                if debug_mode or result.returncode != 0:
                    if result.stdout:
                        st.info("📝 Manim Output:")
                        st.code(result.stdout)
                    
                    if result.stderr:
                        st.warning("⚠️ Manim Warnings/Errors:")
                        st.code(result.stderr)
                
                if result.returncode != 0:
                    st.error(f"❌ Manim failed with return code {result.returncode}")
                    st.stop()
                
            except subprocess.TimeoutExpired:
                st.error("⏰ Animation generation timed out (2 minutes)")
                st.stop()
            except Exception as e:
                st.error(f"💥 Error running Manim: {e}")
                st.stop()
            
            # Enhanced video file discovery
            found_file = None
            
            # Quality-specific paths
            quality_paths = {
                "Low (480p15)": "480p15",
                "Medium (720p30)": "720p30",
                "High (1080p60)": "1080p60"
            }
            
            quality_path = quality_paths[quality]
            
            possible_paths = [
                Path("media/videos/dynamic_handwriting") / quality_path / output_filename,
                Path("media/videos/dynamic_handwriting") / "720p30" / output_filename,  # fallback
                Path("media/videos/dynamic_handwriting") / "480p15" / output_filename,  # fallback
                Path(output_filename),
            ]
            
            # Search for the video file
            for path in possible_paths:
                if path.exists():
                    found_file = str(path)
                    st.success(f"🎬 Found video at: {path}")
                    break
            
            # Parse Manim output for file location
            if not found_file and result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "File ready at" in line:
                        # Extract path from Manim output
                        parts = line.split("'")
                        if len(parts) >= 2:
                            file_path = parts[1]
                            if os.path.exists(file_path):
                                found_file = file_path
                                st.success(f"🎬 Found video from output: {file_path}")
                                break
            
            # Display results
            if found_file:
                st.success("🎉 **Animation generated successfully!**")
                st.video(found_file)
                
                # Show font information from output
                font_info = "Unknown font used"
                if result.stdout:
                    if "Noto Sans Ethiopic" in result.stdout:
                        font_info = "✅ Used Noto Sans Ethiopic (perfect for Tigrinya!)"
                    elif "Comic Sans MS" in result.stdout:
                        font_info = "✅ Used Comic Sans MS (great for Latin text)"
                    elif "System Default" in result.stdout:
                        font_info = "⚠️ Used system default font"
                    elif "Error" in result.stdout:
                        font_info = "❌ Font error occurred - check debug output"
                
                st.info(font_info)
                
                # File size info
                try:
                    file_size = os.path.getsize(found_file) / (1024 * 1024)  # MB
                    st.caption(f"📁 File size: {file_size:.2f} MB")
                except:
                    pass
                
            else:
                st.error("❌ Failed to locate the generated video file")
                st.error("📋 Check the debug output above for details")
                
                # Show available files for debugging
                if debug_mode:
                    st.subheader("🔍 Debug: Available files")
                    media_dir = Path("media")
                    if media_dir.exists():
                        for item in media_dir.rglob("*"):
                            if item.is_file():
                                st.text(f"  {item}")
            
            # Cleanup
            if os.path.exists(script_path):
                os.remove(script_path)

# Additional information
st.markdown("---")
st.markdown("""
**🎯 Tips for best results:**
- Ensure Noto Sans Ethiopic font is installed for Tigrinya text
- Use shorter text for better animation quality  
- Try different quality settings if one fails
- Enable debug mode if you encounter issues

**📚 Supported scripts:** Latin, Tigrinya (ትግርኛ), Amharic (አማርኛ), Geez (ግዕዝ)
""")

# Font testing utility
if st.checkbox("🧪 Show Font Testing Utility"):
    st.subheader("Font Testing")
    
    test_text = st.text_input("Test text:", "ትግርኛ")
    
    if st.button("Test Font Rendering"):
        with st.spinner("Testing fonts..."):
            test_result = subprocess.run([
                "python", "-c", f"""
import sys
from manim import *

test_text = {repr(test_text)}
fonts = [
    'Noto Sans Ethiopic',
    'NotoSansEthiopic-Regular', 
    'Ebrima',
    'Arial Unicode MS',
    'DejaVu Sans'
]

print("=== FONT TEST RESULTS ===")
for font in fonts:
    try:
        text_obj = Text(test_text, font=font, font_size=48)
        print(f"✅ {{font}}: SUCCESS")
    except Exception as e:
        print(f"❌ {{font}}: {{str(e)}}")

# Test default
try:
    text_obj = Text(test_text, font_size=48)
    print(f"✅ System Default: SUCCESS")
except Exception as e:
    print(f"❌ System Default: {{str(e)}}")
"""
            ], capture_output=True, text=True, timeout=30)
            
            st.code(test_result.stdout)
            if test_result.stderr:
                st.code(test_result.stderr)