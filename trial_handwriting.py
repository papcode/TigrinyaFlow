import streamlit as st
import subprocess
import os
import sys
import json
from pathlib import Path
from manim import *

# -------------------------------
# Define the Manim scene
# -------------------------------
class Handwriting(Scene):
    def construct(self):
        # Try to get text from command line arguments first
        text_to_write = "Hello"  # default
        
        # Look for a temporary file with the text
        temp_file = "temp_text.json"
        if os.path.exists(temp_file):
            try:
                with open(temp_file, 'r') as f:
                    data = json.load(f)
                    text_to_write = data.get("text", "Hello")
            except:
                text_to_write = "Hello"
        
        # Also check command line args (alternative method)
        if len(sys.argv) > 1:
            # Look for --text argument
            for i, arg in enumerate(sys.argv):
                if arg == "--text" and i + 1 < len(sys.argv):
                    text_to_write = sys.argv[i + 1]
                    break
        
        text = Text(text_to_write, font="Comic Sans MS", font_size=96)
        self.play(Write(text), run_time=4)
        self.wait(1)


# -------------------------------
# Streamlit UI
# -------------------------------
st.title("✍️ Handwriting Animation Demo")

# Input text
text_input = st.text_input("Enter text to animate:", "House")

if st.button("Generate Animation"):
    if not text_input.strip():
        st.error("Please enter some text to animate!")
    else:
        with st.spinner("Generating animation..."):
            # Method 1: Save text to a temporary JSON file
            temp_data = {"text": text_input}
            temp_file = "temp_text.json"
            with open(temp_file, 'w') as f:
                json.dump(temp_data, f)
            
            # Get the current script name without extension
            script_name = Path(__file__).stem
            
            # Output file name
            output_filename = "handwriting.mp4"
            
            try:
                # Run manim programmatically
                result = subprocess.run([
                    "manim", "-ql", __file__, "Handwriting", "-o", output_filename
                ], capture_output=True, text=True)
                
            except Exception as e:
                st.error(f"Error running Manim: {e}")
                # Clean up temp file even if there's an error
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                st.stop()
            
            # Clean up temp file after successful execution
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Method 1: Parse the Manim output to find the actual file path
            found_file = None
            if result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if "File ready at" in line:
                        path_start = line.find("'") + 1
                        path_end = line.rfind("'")
                        if path_start > 0 and path_end > path_start:
                            file_path = line[path_start:path_end]
                            if os.path.exists(file_path):
                                found_file = file_path
                                break
            
            # Method 2: Try expected locations based on your actual directory structure
            if not found_file:
                # Based on your logs, the exact path should be:
                expected_path = os.path.join("media", "videos", "trial_handwriting", "480p15", output_filename)
                if os.path.exists(expected_path):
                    found_file = expected_path
                else:
                    # Try other common locations
                    possible_paths = [
                        os.path.join("media", "videos", script_name, "480p15", output_filename),
                        os.path.join("media", "videos", script_name, "720p30", output_filename),
                        output_filename,  # Current directory
                    ]
                    
                    for path in possible_paths:
                        if os.path.exists(path):
                            found_file = path
                            break
            
            # Display the result
            if found_file:
                st.success("Animation generated successfully!")
                st.video(found_file)
            else:
                st.error("Failed to generate animation.")
                st.error("Subprocess output:")
                st.code(result.stdout)
                if result.stderr:
                    st.error("Subprocess errors:")
                    st.code(result.stderr)

# Add some helpful information
st.markdown("---")
st.markdown("**Note:** This app uses Manim to generate handwriting animations. Make sure you have Manim installed and properly configured.")

# Display current working directory for debugging
if st.checkbox("Show debug info"):
    st.write(f"Current working directory: {os.getcwd()}")
    st.write(f"Script file: {__file__}")
    
    # List media directory contents if it exists
    media_dir = Path("media")
    if media_dir.exists():
        st.write("Media directory contents:")
        for item in media_dir.rglob("*"):
            if item.is_file():
                st.write(f"  {item}")