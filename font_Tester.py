# -*- coding: utf-8 -*-
"""
Comprehensive Tigrinya Font Testing Script
Tests font rendering for Tigrinya vocabulary words
"""

import sys
import os
import json
import platform
from datetime import datetime
import subprocess
import traceback

# Set environment variables for better Unicode support
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

# Try to set console to UTF-8 on Windows
if platform.system() == 'Windows':
    try:
        os.system('chcp 65001')
    except:
        pass

def safe_print(text):
    """Safely print Unicode text across different platforms"""
    try:
        print(text, flush=True)
    except UnicodeEncodeError:
        # Fallback for systems with limited Unicode support
        try:
            print(text.encode('utf-8', errors='ignore').decode('utf-8'), flush=True)
        except:
            print("(Unicode display error)", flush=True)

def test_console_unicode():
    """Test if console can display Unicode characters"""
    safe_print("=== CONSOLE UNICODE TEST ===")
    safe_print("Testing basic Unicode support...")
    
    test_chars = [
        ("Latin", "Hello World"),
        ("Tigrinya", "ሰላም"),
        ("Geez numbers", "፩፪፫፬፭"),
        ("Mixed", "Hello ሰላም"),
        ("Emoji fallback", "[OK] [ERROR]")  # Instead of emojis
    ]
    
    for name, text in test_chars:
        try:
            safe_print(f"{name}: {text}")
        except Exception as e:
            safe_print(f"{name}: (display error)")
    
    safe_print("")

def get_vocabulary():
    """Get the Tigrinya vocabulary dictionary"""
    return {
        # Colors
        "red": "ቀይሕ",
        "blue": "ሰማያዊ", 
        "green": "ቀጠልያ",
        "yellow": "ቢጫ",
        "black": "ጸሊም",
        "white": "ጻዕዳ",  # Fixed: was incorrectly "ቀይሕ"
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

def test_manim_fonts():
    """Test font rendering with Manim"""
    safe_print("=== MANIM FONT TESTING ===")
    
    # Test fonts in order of preference
    fonts_to_test = [
        'Noto Sans Ethiopic',
        'NotoSansEthiopic-Regular',
        'Noto Sans Ethiopic Regular', 
        'Ebrima',
        'Nyala',
        'Abyssinica SIL',
        'Kefa',
        'Arial Unicode MS',
        'DejaVu Sans',
        'Liberation Sans',
        'FreeSans',
        'Arial',
        None  # System default
    ]
    
    test_words = ["ሰላም", "ትግርኛ", "ገዛ", "መጽሓፍ", "ኣንበሳ"]
    
    results = {}
    
    for font in fonts_to_test:
        font_name = font if font else "System Default"
        safe_print(f"Testing font: {font_name}")
        
        font_results = {}
        
        for word in test_words:
            try:
                # Create a subprocess to test font rendering
                # This isolates the test to prevent crashes
                test_code = f'''
import sys
import os
os.environ["PYTHONIOENCODING"] = "utf-8"

try:
    from manim import Text, config
    config.disable_caching = True
    
    test_word = "{word}"
    font_kwargs = {{"font_size": 48}}
    if "{font}":
        font_kwargs["font"] = "{font}"
    
    text_obj = Text(test_word, **font_kwargs)
    print("SUCCESS")
except ImportError:
    print("MANIM_NOT_INSTALLED")
except Exception as e:
    print(f"ERROR: {{str(e)}}")
'''
                
                result = subprocess.run(
                    [sys.executable, '-c', test_code],
                    capture_output=True,
                    text=True,
                    timeout=15,
                    encoding='utf-8',
                    errors='replace'
                )
                
                if "SUCCESS" in result.stdout:
                    font_results[word] = "OK"
                elif "MANIM_NOT_INSTALLED" in result.stdout:
                    font_results[word] = "MANIM_NOT_INSTALLED"
                    break
                else:
                    error_msg = result.stdout.strip() or result.stderr.strip()
                    font_results[word] = f"ERROR: {error_msg[:100]}"
                    
            except subprocess.TimeoutExpired:
                font_results[word] = "TIMEOUT"
            except Exception as e:
                font_results[word] = f"EXCEPTION: {str(e)[:100]}"
        
        results[font_name] = font_results
        
        # Print immediate results
        if font_results:
            if "MANIM_NOT_INSTALLED" in str(font_results):
                safe_print("  [ERROR] Manim not installed")
                break
            else:
                success_count = sum(1 for status in font_results.values() if status == "OK")
                total_count = len(font_results)
                safe_print(f"  [RESULT] {success_count}/{total_count} words rendered successfully")
        
        safe_print("")
    
    return results

def test_vocabulary_rendering():
    """Test rendering of all vocabulary words"""
    safe_print("=== VOCABULARY RENDERING TEST ===")
    
    vocab = get_vocabulary()
    
    # Test with the most promising font first
    promising_fonts = ['Noto Sans Ethiopic', 'Ebrima', None]
    
    for font in promising_fonts:
        font_name = font if font else "System Default"
        safe_print(f"Testing vocabulary with {font_name}:")
        
        success_count = 0
        total_count = len(vocab)
        failed_words = []
        
        for english, tigrinya in vocab.items():
            try:
                test_code = f'''
import sys
import os
os.environ["PYTHONIOENCODING"] = "utf-8"

try:
    from manim import Text, config
    config.disable_caching = True
    
    tigrinya_word = "{tigrinya}"
    font_kwargs = {{"font_size": 48}}
    if "{font}":
        font_kwargs["font"] = "{font}"
    
    text_obj = Text(tigrinya_word, **font_kwargs)
    print("SUCCESS")
except ImportError:
    print("MANIM_NOT_INSTALLED")
except Exception as e:
    print(f"ERROR: {{str(e)}}")
'''
                
                result = subprocess.run(
                    [sys.executable, '-c', test_code],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    encoding='utf-8',
                    errors='replace'
                )
                
                if "SUCCESS" in result.stdout:
                    success_count += 1
                elif "MANIM_NOT_INSTALLED" in result.stdout:
                    safe_print("  [ERROR] Manim not installed")
                    return
                else:
                    failed_words.append(f"{english} ({tigrinya})")
                    
            except Exception as e:
                failed_words.append(f"{english} ({tigrinya}) - Exception: {str(e)[:50]}")
        
        safe_print(f"  Success rate: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
        
        if failed_words and len(failed_words) <= 10:  # Show only first 10 failures
            safe_print("  Failed words:")
            for word in failed_words[:10]:
                safe_print(f"    - {word}")
            if len(failed_words) > 10:
                safe_print(f"    ... and {len(failed_words) - 10} more")
        
        safe_print("")
        
        # If we found a working font, we can break
        if success_count > total_count * 0.8:  # 80% success rate
            safe_print(f"[GOOD] {font_name} works well with {success_count/total_count*100:.1f}% success rate")
            break

def test_system_fonts():
    """Test what fonts are available on the system"""
    safe_print("=== SYSTEM FONT DETECTION ===")
    
    system = platform.system()
    safe_print(f"Operating System: {system}")
    
    if system == "Windows":
        try:
            import winreg
            fonts_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                     r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts")
            
            ethiopic_fonts = []
            unicode_fonts = []
            
            i = 0
            try:
                while True:
                    font_name, font_file, _ = winreg.EnumValue(fonts_key, i)
                    font_lower = font_name.lower()
                    
                    if any(keyword in font_lower for keyword in ['ethiopic', 'noto', 'ebrima', 'nyala']):
                        ethiopic_fonts.append(font_name)
                    elif any(keyword in font_lower for keyword in ['unicode', 'arial', 'dejavu']):
                        unicode_fonts.append(font_name)
                    
                    i += 1
            except WindowsError:
                pass
            
            winreg.CloseKey(fonts_key)
            
            if ethiopic_fonts:
                safe_print("Ethiopic-friendly fonts found:")
                for font in ethiopic_fonts[:10]:  # Show first 10
                    safe_print(f"  - {font}")
            else:
                safe_print("No Ethiopic-specific fonts found")
            
            if unicode_fonts:
                safe_print("Unicode-capable fonts found:")
                for font in unicode_fonts[:5]:  # Show first 5
                    safe_print(f"  - {font}")
            
        except ImportError:
            safe_print("Cannot access Windows registry (winreg not available)")
        except Exception as e:
            safe_print(f"Error checking Windows fonts: {e}")
    
    elif system == "Darwin":  # macOS
        try:
            result = subprocess.run(
                ["fc-list", ":lang=am"],  # Amharic language fonts (includes Ethiopic script)
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                fonts = result.stdout.strip().split('\n')
                safe_print(f"Found {len(fonts)} Ethiopic-capable fonts via fc-list")
                for font in fonts[:5]:
                    safe_print(f"  - {font.split(':')[0]}")
            else:
                safe_print("fc-list not available or no Ethiopic fonts found")
                
        except FileNotFoundError:
            safe_print("fc-list command not found")
        except Exception as e:
            safe_print(f"Error checking macOS fonts: {e}")
    
    else:  # Linux
        try:
            result = subprocess.run(
                ["fc-list", ":lang=am"],
                capture_output=True, 
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                fonts = result.stdout.strip().split('\n')
                safe_print(f"Found {len(fonts)} Ethiopic-capable fonts")
                for font in fonts[:5]:
                    safe_print(f"  - {font.split(':')[0]}")
            else:
                safe_print("No Ethiopic fonts found via fc-list")
                
        except FileNotFoundError:
            safe_print("fc-list command not found")
        except Exception as e:
            safe_print(f"Error checking Linux fonts: {e}")
    
    safe_print("")

def generate_report():
    """Generate a comprehensive test report"""
    safe_print("=" * 60)
    safe_print("TIGRINYA HANDWRITING ANIMATION - FONT TEST REPORT")
    safe_print("=" * 60)
    safe_print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    safe_print(f"System: {platform.system()} {platform.release()}")
    safe_print(f"Python: {platform.python_version()}")
    safe_print("")
    
    # Test console Unicode support
    test_console_unicode()
    
    # Test system fonts
    test_system_fonts()
    
    # Test Manim font rendering
    try:
        font_results = test_manim_fonts()
        
        # Find best performing font
        best_font = None
        best_score = 0
        
        for font_name, word_results in font_results.items():
            if word_results and "MANIM_NOT_INSTALLED" not in str(word_results):
                success_count = sum(1 for status in word_results.values() if status == "OK")
                if success_count > best_score:
                    best_score = success_count
                    best_font = font_name
        
        if best_font:
            safe_print(f"[RECOMMENDATION] Best font: {best_font} (success rate: {best_score}/5)")
        else:
            safe_print("[WARNING] No fonts performed well in basic testing")
        
        safe_print("")
        
    except Exception as e:
        safe_print(f"Error during Manim testing: {e}")
        safe_print("")
    
    # Test full vocabulary
    try:
        test_vocabulary_rendering()
    except Exception as e:
        safe_print(f"Error during vocabulary testing: {e}")
        safe_print("")
    
    # Recommendations
    safe_print("=== RECOMMENDATIONS ===")
    safe_print("1. Install Noto Sans Ethiopic from Google Fonts")
    safe_print("2. If on Windows, also try installing Ebrima font")
    safe_print("3. Ensure your terminal/console supports UTF-8")
    safe_print("4. Update Manim to the latest version")
    safe_print("5. Test with shorter words first before full sentences")
    safe_print("")
    
    safe_print("=== FONT INSTALLATION COMMANDS ===")
    
    system = platform.system()
    if system == "Windows":
        safe_print("Windows:")
        safe_print("- Download from: https://fonts.google.com/noto/specimen/Noto+Sans+Ethiopic")
        safe_print("- Extract and double-click .ttf files, click 'Install'")
    elif system == "Darwin":
        safe_print("macOS:")
        safe_print("- brew install --cask font-noto-sans-ethiopic")
        safe_print("- Or download from Google Fonts and double-click to install")
    else:
        safe_print("Linux:")
        safe_print("- sudo apt install fonts-noto")  # Ubuntu/Debian
        safe_print("- sudo dnf install google-noto-sans-ethiopic-fonts")  # Fedora
        safe_print("- sudo pacman -S noto-fonts")  # Arch
    
    safe_print("")
    safe_print("Test completed! Check the output above for detailed results.")

if __name__ == "__main__":
    try:
        generate_report()
    except KeyboardInterrupt:
        safe_print("\nTest interrupted by user")
    except Exception as e:
        safe_print(f"\nUnexpected error: {e}")
        safe_print("Full traceback:")
        traceback.print_exc()