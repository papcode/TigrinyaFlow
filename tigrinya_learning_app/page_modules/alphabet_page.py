"""
Tigrinya Alphabet Learning Page - Traditional Three-Column Layout
Complete implementation matching traditional Tigrinya alphabet educational materials
"""

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from utils.image_loader import ImageLoader

from clientTranslation import alef_row, feedel_rows, geez_to_latin_syllable


def create_traditional_alphabet_structure():
    """Create the traditional three-column alphabet structure with corrected data."""
    
    alphabet_data = {
      "column1": [
        {
          "family": "be",
          "familyName": "Be Family",
          "baseName": "በ",
          "baseChar": "በ",
          "exampleWord": "በለ (fruit)",
          "icon": "🍎",
          "color": "#ff6b8a",
          "characters": [
            { "char": "በ", "sound": "be" },
            { "char": "ቡ", "sound": "bu" },
            { "char": "ቢ", "sound": "bi" },
            { "char": "ባ", "sound": "ba" },
            { "char": "ቤ", "sound": "bie" },
            { "char": "ብ", "sound": "b" },
            { "char": "ቦ", "sound": "bo" }
          ]
        },
        {
          "family": "se",
          "familyName": "Se Family",
          "baseName": "ሰ",
          "baseChar": "ሰ",
          "exampleWord": "ሰዓት (clock)",
          "icon": "🕐",
          "color": "#5dd9d2",
          "characters": [
            { "char": "ሰ", "sound": "se" },
            { "char": "ሱ", "sound": "su" },
            { "char": "ሲ", "sound": "si" },
            { "char": "ሳ", "sound": "sa" },
            { "char": "ሴ", "sound": "sie" },
            { "char": "ስ", "sound": "s" },
            { "char": "ሶ", "sound": "so" }
          ]
        },
        {
          "family": "she",
          "familyName": "She Family",
          "baseName": "ሸ",
          "baseChar": "ሸ",
          "exampleWord": "ሽበጥ (shoe)",
          "icon": "👞",
          "color": "#4db8e8",
          "characters": [
            { "char": "ሸ", "sound": "she" },
            { "char": "ሹ", "sound": "shu" },
            { "char": "ሺ", "sound": "shi" },
            { "char": "ሻ", "sound": "sha" },
            { "char": "ሼ", "sound": "shie" },
            { "char": "ሽ", "sound": "sh" },
            { "char": "ሾ", "sound": "sho" }
          ]
        },
        {
          "family": "ke",
          "familyName": "Ke Family",
          "baseName": "ከ",
          "baseChar": "ከ",
          "exampleWord": "ከልቢ (dog)",
          "icon": "🐕",
          "color": "#90d890",
          "characters": [
            { "char": "ከ", "sound": "ke" },
            { "char": "ኩ", "sound": "ku" },
            { "char": "ኪ", "sound": "ki" },
            { "char": "ካ", "sound": "ka" },
            { "char": "ኬ", "sound": "kie" },
            { "char": "ክ", "sound": "k" },
            { "char": "ኮ", "sound": "ko" }
          ]
        },
        {
          "family": "khe",
          "familyName": "Khe Family",
          "baseName": "ኸ",
          "baseChar": "ኸ",
          "exampleWord": "ኮኾብ (star)",
          "icon": "⭐",
          "color": "#ffd966",
          "characters": [
            { "char": "ኸ", "sound": "khe" },
            { "char": "ኹ", "sound": "khu" },
            { "char": "ኺ", "sound": "khi" },
            { "char": "ኻ", "sound": "kha" },
            { "char": "ኼ", "sound": "khie" },
            { "char": "ኽ", "sound": "kh" },
            { "char": "ኾ", "sound": "kho" }
          ]
        },
        {
          "family": "le",
          "familyName": "Le Family",
          "baseName": "ለ",
          "baseChar": "ለ",
          "exampleWord": "ለምን (lemon)",
          "icon": "🍋",
          "color": "#ffe680",
          "characters": [
            { "char": "ለ", "sound": "le" },
            { "char": "ሉ", "sound": "lu" },
            { "char": "ሊ", "sound": "li" },
            { "char": "ላ", "sound": "la" },
            { "char": "ሌ", "sound": "lie" },
            { "char": "ል", "sound": "l" },
            { "char": "ሎ", "sound": "lo" }
          ]
        },
        {
          "family": "e",
          "familyName": "E Family",
          "baseName": "እ",
          "baseChar": "እ",
          "exampleWord": "አንበሳ (lion)",
          "icon": "🦁",
          "color": "#ff9999",
          "characters": [
            { "char": "እ", "sound": "e" },
            { "char": "ኡ", "sound": "u" },
            { "char": "ኢ", "sound": "i" },
            { "char": "ኣ", "sound": "a" },
            { "char": "ኤ", "sound": "ie" },
            { "char": "እ", "sound": "i" },
            { "char": "ኦ", "sound": "o" }
          ]
        },
        {
          "family": "tse",
          "familyName": "Tse Family",
          "baseName": "ጸ",
          "baseChar": "ጸ",
          "exampleWord": "ጸሃ (door)",
          "icon": "🚪",
          "color": "#c9a0dc",
          "characters": [
            { "char": "ጸ", "sound": "tse" },
            { "char": "ጹ", "sound": "tsu" },
            { "char": "ጺ", "sound": "tsi" },
            { "char": "ጻ", "sound": "tsa" },
            { "char": "ጼ", "sound": "tsie" },
            { "char": "ጽ", "sound": "ts" },
            { "char": "ጾ", "sound": "tso" }
          ]
        },
        {
          "family": "de",
          "familyName": "De Family",
          "baseName": "ደ",
          "baseChar": "ደ",
          "exampleWord": "ድማው (cat)",
          "icon": "🐱",
          "color": "#ffa07a",
          "characters": [
            { "char": "ደ", "sound": "de" },
            { "char": "ዱ", "sound": "du" },
            { "char": "ዲ", "sound": "di" },
            { "char": "ዳ", "sound": "da" },
            { "char": "ዴ", "sound": "die" },
            { "char": "ድ", "sound": "d" },
            { "char": "ዶ", "sound": "do" }
          ]
        },
        {
          "family": "je",
          "familyName": "Je Family",
          "baseName": "ጀ",
          "baseChar": "ጀ",
          "exampleWord": "ጀሪካን (jerrycan)",
          "icon": "🛢️",
          "color": "#98d8c8",
          "characters": [
            { "char": "ጀ", "sound": "je" },
            { "char": "ጁ", "sound": "ju" },
            { "char": "ጂ", "sound": "ji" },
            { "char": "ጃ", "sound": "ja" },
            { "char": "ጄ", "sound": "jie" },
            { "char": "ጅ", "sound": "j" },
            { "char": "ጆ", "sound": "jo" }
          ]
        },
        {
          "family": "ze",
          "familyName": "Ze Family",
          "baseName": "ዘ",
          "baseChar": "ዘ",
          "exampleWord": "ዘይቲ (oil)",
          "icon": "🍯",
          "color": "#f6e58d",
          "characters": [
            { "char": "ዘ", "sound": "ze" },
            { "char": "ዙ", "sound": "zu" },
            { "char": "ዚ", "sound": "zi" },
            { "char": "ዛ", "sound": "za" },
            { "char": "ዜ", "sound": "zie" },
            { "char": "ዝ", "sound": "z" },
            { "char": "ዞ", "sound": "zo" }
          ]
        }
      ],
      "column2": [
        {
          "family": "He",
          "familyName": "He Family",
          "baseName": "ሀ",
          "baseChar": "ሀ",
          "exampleWord": "ሓዊ (fire)",
          "icon": "🔥",
          "color": "#ff6b8a",
          "characters": [
            { "char": "ሀ", "sound": "He" },
            { "char": "ሁ", "sound": "Hu" },
            { "char": "ሂ", "sound": "Hi" },
            { "char": "ሃ", "sound": "Ha" },
            { "char": "ሄ", "sound": "Hie" },
            { "char": "ህ", "sound": "H" },
            { "char": "ሆ", "sound": "Ho" }
          ]
        },
        {
          "family": "Te",
          "familyName": "Te Family",
          "baseName": "ተ",
          "baseChar": "ተ",
          "exampleWord": "ጠራሙዝ (bottle)",
          "icon": "🍾",
          "color": "#6495ed",
          "characters": [
            { "char": "ተ", "sound": "Te" },
            { "char": "ቱ", "sound": "Tu" },
            { "char": "ቲ", "sound": "Ti" },
            { "char": "ታ", "sound": "Ta" },
            { "char": "ቴ", "sound": "Tie" },
            { "char": "ት", "sound": "T" },
            { "char": "ቶ", "sound": "To" }
          ]
        },
        {
          "family": "Ṭe",
          "familyName": "Ṭe Family",
          "baseName": "ጠ",
          "baseChar": "ጠ",
          "exampleWord": "ጠመን (thirsty)",
          "icon": "💧",
          "color": "#4fc3f7",
          "characters": [
            { "char": "ጠ", "sound": "Ṭe" },
            { "char": "ጡ", "sound": "Ṭu" },
            { "char": "ጢ", "sound": "Ṭi" },
            { "char": "ጣ", "sound": "Ṭa" },
            { "char": "ጤ", "sound": "Ṭie" },
            { "char": "ጥ", "sound": "Ṭ" },
            { "char": "ጦ", "sound": "Ṭo" }
          ]
        },
        {
          "family": "Che",
          "familyName": "Che Family",
          "baseName": "ቸ",
          "baseChar": "ቸ",
          "exampleWord": "ጨቋዊት (hen)",
          "icon": "🐔",
          "color": "#87ceeb",
          "characters": [
            { "char": "ቸ", "sound": "Che" },
            { "char": "ቹ", "sound": "Chu" },
            { "char": "ቺ", "sound": "Chi" },
            { "char": "ቻ", "sound": "Cha" },
            { "char": "ቼ", "sound": "Chie" },
            { "char": "ች", "sound": "Ch" },
            { "char": "ቾ", "sound": "Cho" }
          ]
        },
        {
          "family": "qe",
          "familyName": "Qe Family",
          "baseName": "ቀ",
          "baseChar": "ቀ",
          "exampleWord": "ቀሺ (priest)",
          "icon": "⛪",
          "color": "#e76f51",
          "characters": [
            { "char": "ቀ", "sound": "qe" },
            { "char": "ቁ", "sound": "qu" },
            { "char": "ቂ", "sound": "qi" },
            { "char": "ቃ", "sound": "qa" },
            { "char": "ቄ", "sound": "qie" },
            { "char": "ቅ", "sound": "q" },
            { "char": "ቆ", "sound": "qo" }
          ]
        },
        {
          "family": "ghe",
          "familyName": "Ghe Family",
          "baseName": "ቐ",
          "baseChar": "ቐ",
          "exampleWord": "መቐሻ (scissors)",
          "icon": "✂️",
          "color": "#5dd9d2",
          "characters": [
            { "char": "ቐ", "sound": "ghe" },
            { "char": "ቑ", "sound": "ghu" },
            { "char": "ቒ", "sound": "ghi" },
            { "char": "ቓ", "sound": "gha" },
            { "char": "ቔ", "sound": "ghie" },
            { "char": "ቕ", "sound": "gh" },
            { "char": "ቖ", "sound": "gho" }
          ]
        },
        {
          "family": "ge",
          "familyName": "Ge Family",
          "baseName": "ገ",
          "baseChar": "ገ",
          "exampleWord": "ገዛ (house)",
          "icon": "🏠",
          "color": "#6eb5ff",
          "characters": [
            { "char": "ገ", "sound": "ge" },
            { "char": "ጉ", "sound": "gu" },
            { "char": "ጊ", "sound": "gi" },
            { "char": "ጋ", "sound": "ga" },
            { "char": "ጌ", "sound": "gie" },
            { "char": "ግ", "sound": "g" },
            { "char": "ጎ", "sound": "go" }
          ]
        },
        {
          "family": "ne",
          "familyName": "Ne Family",
          "baseName": "ነ",
          "baseChar": "ነ",
          "exampleWord": "ነብሪ (tiger)",
          "icon": "🐯",
          "color": "#ffb84d",
          "characters": [
            { "char": "ነ", "sound": "ne" },
            { "char": "ኑ", "sound": "nu" },
            { "char": "ኒ", "sound": "ni" },
            { "char": "ና", "sound": "na" },
            { "char": "ኔ", "sound": "nie" },
            { "char": "ን", "sound": "n" },
            { "char": "ኖ", "sound": "no" }
          ]
        },
        {
          "family": "ye",
          "familyName": "Ye Family",
          "baseName": "የ",
          "baseChar": "የ",
          "exampleWord": "የማነ (man)",
          "icon": "👨",
          "color": "#c8b6ff",
          "characters": [
            { "char": "የ", "sound": "ye" },
            { "char": "ዩ", "sound": "yu" },
            { "char": "ዪ", "sound": "yi" },
            { "char": "ያ", "sound": "ya" },
            { "char": "ዬ", "sound": "yie" },
            { "char": "ይ", "sound": "y" },
            { "char": "ዮ", "sound": "yo" }
          ]
        },
        {
          "family": "re",
          "familyName": "Re Family",
          "baseName": "ረ",
          "baseChar": "ረ",
          "exampleWord": "ረጋቢት (doves)",
          "icon": "🕊️",
          "color": "#ff9eb3",
          "characters": [
            { "char": "ረ", "sound": "re" },
            { "char": "ሩ", "sound": "ru" },
            { "char": "ሪ", "sound": "ri" },
            { "char": "ራ", "sound": "ra" },
            { "char": "ሬ", "sound": "rie" },
            { "char": "ር", "sound": "r" },
            { "char": "ሮ", "sound": "ro" }
          ]
        },
        {
          "family": "fe",
          "familyName": "Fe Family",
          "baseName": "ፈ",
          "baseChar": "ፈ",
          "exampleWord": "ፈረስ (horse)",
          "icon": "🐴",
          "color": "#dda15e",
          "characters": [
            { "char": "ፈ", "sound": "fe" },
            { "char": "ፉ", "sound": "fu" },
            { "char": "ፊ", "sound": "fi" },
            { "char": "ፋ", "sound": "fa" },
            { "char": "ፌ", "sound": "fie" },
            { "char": "ፍ", "sound": "f" },
            { "char": "ፎ", "sound": "fo" }
          ]
        }
      ],
      "column3": [
        {
          "family": "he",
          "familyName": "He Family",
          "baseName": "ህ",
          "baseChar": "ህ",
          "exampleWord": "ህቦይ (monkey)",
          "icon": "🐵",
          "color": "#26c6da",
          "characters": [
            { "char": "ሀ", "sound": "he" },
            { "char": "ሁ", "sound": "hu" },
            { "char": "ሂ", "sound": "hi" },
            { "char": "ሃ", "sound": "ha" },
            { "char": "ሄ", "sound": "hie" },
            { "char": "ህ", "sound": "h" },
            { "char": "ሆ", "sound": "ho" }
          ]
        },
        {
          "family": "E",
          "familyName": "E Family",
          "baseName": "እ",
          "baseChar": "እ",
          "exampleWord": "ወረቀት (paper)",
          "icon": "📄",
          "color": "#5dade2",
          "characters": [
            { "char": "እ", "sound": "E" },
            { "char": "ኡ", "sound": "U" },
            { "char": "ኢ", "sound": "I" },
            { "char": "ኣ", "sound": "A" },
            { "char": "ኤ", "sound": "IE" },
            { "char": "እ", "sound": "I" },
            { "char": "ኦ", "sound": "O" }
          ]
        },
        {
          "family": "we",
          "familyName": "We Family",
          "baseName": "ወ",
          "baseChar": "ወ",
          "exampleWord": "ወርቂ (gold)",
          "icon": "💰",
          "color": "#ec407a",
          "characters": [
            { "char": "ወ", "sound": "we" },
            { "char": "ዉ", "sound": "wu" },
            { "char": "ዊ", "sound": "wi" },
            { "char": "ዋ", "sound": "wa" },
            { "char": "ዌ", "sound": "wie" },
            { "char": "ው", "sound": "w" },
            { "char": "ዎ", "sound": "wo" }
          ]
        },
        {
          "family": "me",
          "familyName": "Me Family",
          "baseName": "መ",
          "baseChar": "መ",
          "exampleWord": "መኪና (car)",
          "icon": "🚗",
          "color": "#66bb6a",
          "characters": [
            { "char": "መ", "sound": "me" },
            { "char": "ሙ", "sound": "mu" },
            { "char": "ሚ", "sound": "mi" },
            { "char": "ማ", "sound": "ma" },
            { "char": "ሜ", "sound": "mie" },
            { "char": "ም", "sound": "m" },
            { "char": "ሞ", "sound": "mo" }
          ]
        },
        {
          "family": "pe",
          "familyName": "Pe Family",
          "baseName": "ፐ",
          "baseChar": "ፐ",
          "exampleWord": "ፓፓዮ (papaya)",
          "icon": "🥭",
          "color": "#ff9800",
          "characters": [
            { "char": "ፐ", "sound": "pe" },
            { "char": "ፑ", "sound": "pu" },
            { "char": "ፒ", "sound": "pi" },
            { "char": "ፓ", "sound": "pa" },
            { "char": "ፔ", "sound": "pie" },
            { "char": "ፕ", "sound": "p" },
            { "char": "ፖ", "sound": "po" }
          ]
        },
        {
          "family": "che",
          "familyName": "Che Family",
          "baseName": "ጨ",
          "baseChar": "ጨ",
          "exampleWord": "ጫው (tea)",
          "icon": "☕",
          "color": "#ef5350",
          "characters": [
            { "char": "ጨ", "sound": "che" },
            { "char": "ጩ", "sound": "chu" },
            { "char": "ጪ", "sound": "chi" },
            { "char": "ጫ", "sound": "cha" },
            { "char": "ጬ", "sound": "chie" },
            { "char": "ጭ", "sound": "ch" },
            { "char": "ጮ", "sound": "cho" }
          ]
        },
        {
          "family": "nye",
          "familyName": "Nye Family",
          "baseName": "ኘ",
          "baseChar": "ኘ",
          "exampleWord": "ኛው (leopard)",
          "icon": "🐆",
          "color": "#ffa726",
          "characters": [
            { "char": "ኘ", "sound": "nye" },
            { "char": "ኙ", "sound": "nyu" },
            { "char": "ኚ", "sound": "nyi" },
            { "char": "ኛ", "sound": "nya" },
            { "char": "ኜ", "sound": "nyie" },
            { "char": "ኝ", "sound": "ny" },
            { "char": "ኞ", "sound": "nyo" }
          ]
        },
        {
          "family": "Pe",
          "familyName": "Pe Family",
          "baseName": "ፐ",
          "baseChar": "ፐ",
          "exampleWord": "ፓስ (pass)",
          "icon": "🎫",
          "color": "#7e57c2",
          "characters": [
            { "char": "ፐ", "sound": "Pe" },
            { "char": "ፑ", "sound": "Pu" },
            { "char": "ፒ", "sound": "Pi" },
            { "char": "ፓ", "sound": "Pa" },
            { "char": "ፔ", "sound": "Pie" },
            { "char": "ፕ", "sound": "P" },
            { "char": "ፖ", "sound": "Po" }
          ]
        },
        {
          "family": "zhe",
          "familyName": "Zhe Family",
          "baseName": "ዠ",
          "baseChar": "ዠ",
          "exampleWord": "ቴሌቪዥን (television)",
          "icon": "📺",
          "color": "#42a5f5",
          "characters": [
            { "char": "ዠ", "sound": "zhe" },
            { "char": "ዡ", "sound": "zhu" },
            { "char": "ዢ", "sound": "zhi" },
            { "char": "ዣ", "sound": "zha" },
            { "char": "ዤ", "sound": "zhie" },
            { "char": "ዥ", "sound": "zh" },
            { "char": "ዦ", "sound": "zho" }
          ]
        }
      ]
    }
    return alphabet_data


def create_alphabet_grid_html(alphabet_structure):
    """Create complete alphabet grid with proper DOM manipulation"""
    import json

    # Convert data to JSON for JavaScript
    alphabet_data = json.dumps(alphabet_structure)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Noto Sans Ethiopic', Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }}

            .alphabet-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                max-width: 1800px;
                margin: 0 auto;
            }}

            .column {{
                display: flex;
                flex-direction: column;
                gap: 15px;
            }}

            .column-header {{
                text-align: center;
                font-size: 1.3em;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                border-bottom: 3px solid #3498db;
                margin-bottom: 15px;
            }}

            .family-box {{
                border-radius: 12px;
                padding: 15px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
                border: 3px solid;
            }}

            .family-box:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            }}

            .family-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                margin-bottom: 12px;
            }}

            .family-icon {{
                font-size: 1.6em;
            }}

            .family-name {{
                font-size: 1.1em;
                text-transform: capitalize;
            }}

            .family-content {{
                display: flex;
                align-items: center;
                gap: 15px;
            }}
            
            .base-char-display {{
                font-size: 4.5em;
                font-weight: bold;
                padding-right: 15px;
            }}

            .character-details {{
                flex: 1;
            }}

            .example-word {{
                text-align: center;
                margin-bottom: 10px;
                font-style: italic;
                color: #555;
                font-size: 1.1em;
            }}

            .characters-row {{
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 6px;
            }}

            .char-btn {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 8px 4px;
                border: 2px solid rgba(255,255,255,0.3);
                border-radius: 8px;
                background: rgba(255,255,255,0.1);
                cursor: pointer;
                transition: all 0.2s ease;
                min-width: 50px;
                color: white;
                font-weight: bold;
                flex: 1;
                aspect-ratio: 1;
            }}

            .char-btn:hover {{
                transform: scale(1.05);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                border-color: rgba(255,255,255,0.6);
            }}

            .char-btn:active {{
                transform: scale(0.95);
            }}

            .char-display {{
                font-size: 1.8em;
                font-weight: bold;
                font-family: 'Noto Sans Ethiopic', serif;
            }}

            .sound-label {{
                font-size: 0.8em;
                opacity: 0.9;
                text-align: center;
                margin-top: 2px;
            }}

            .selected-char {{
                background: rgba(255,255,255,0.4) !important;
                border-color: #fff !important;
                transform: scale(1.1);
            }}
        </style>
    </head>
    <body>
        <div class="alphabet-grid" id="alphabetGrid">
            <div class="column column-1">
                <div class="column-header"></div>
            </div>
            <div class="column column-2">
                <div class="column-header"></div>
            </div>
            <div class="column column-3">
                <div class="column-header"></div>
            </div>
        </div>

        <script>
            const alphabetData = {alphabet_data};
            let selectedCharacter = null;

            // Communication with parent window
            function selectCharacter(char) {{
                selectedCharacter = char;

                // Remove previous selection
                document.querySelectorAll('.char-btn').forEach(btn => {{
                    btn.classList.remove('selected-char');
                }});

                // Highlight selected character
                const targetBtn = Array.from(document.querySelectorAll('.char-btn')).find(btn => btn.querySelector('.char-display').textContent === char);
                if (targetBtn) {{
                    targetBtn.classList.add('selected-char');
                }}

                // Send to parent window (Streamlit)
                window.parent.postMessage({{
                    type: 'character_selected',
                    character: char
                }}, '*');
            }}

            function createFamilyBox(family, columnClass) {{
                const familyBox = document.createElement('div');
                familyBox.className = 'family-box';
                familyBox.style.borderColor = family.color;
                familyBox.style.background = `linear-gradient(135deg, ${{family.color}}1A, ${{family.color}}33)`;

                // Family header
                const header = document.createElement('div');
                header.className = 'family-header';
                header.style.background = family.color;

                const icon = document.createElement('span');
                icon.className = 'family-icon';
                icon.textContent = family.icon;

                const name = document.createElement('span');
                name.className = 'family-name';
                name.textContent = family.familyName;

                header.appendChild(icon);
                header.appendChild(name);
                
                // Content area
                const content = document.createElement('div');
                content.className = 'family-content';

                const baseCharDisplay = document.createElement('div');
                baseCharDisplay.className = 'base-char-display';
                baseCharDisplay.textContent = family.baseName;
                baseCharDisplay.style.color = family.color;

                const details = document.createElement('div');
                details.className = 'character-details';

                // Example word
                const example = document.createElement('div');
                example.className = 'example-word';
                example.textContent = family.exampleWord;

                // Characters row
                const charactersRow = document.createElement('div');
                charactersRow.className = 'characters-row';

                // Create character buttons
                family.characters.forEach((charObj) => {{
                    const button = document.createElement('button');
                    button.className = 'char-btn';
                    button.style.background = `linear-gradient(45deg, ${{family.color}}B3, ${{family.color}}E6)`;
                    button.onclick = () => selectCharacter(charObj.char);

                    const charDisplay = document.createElement('div');
                    charDisplay.className = 'char-display';
                    charDisplay.textContent = charObj.char;

                    const soundLabel = document.createElement('div');
                    soundLabel.className = 'sound-label';
                    soundLabel.textContent = charObj.sound;

                    button.appendChild(charDisplay);
                    button.appendChild(soundLabel);
                    charactersRow.appendChild(button);
                }});
                
                details.appendChild(example);
                details.appendChild(charactersRow);
                content.appendChild(baseCharDisplay);
                content.appendChild(details);
                familyBox.appendChild(header);
                familyBox.appendChild(content);

                return familyBox;
            }}

            function initializeGrid() {{
                const columns = {{
                    'column1': document.querySelector('.column-1'),
                    'column2': document.querySelector('.column-2'),
                    'column3': document.querySelector('.column-3')
                }};

                Object.keys(columns).forEach(columnKey => {{
                    const families = alphabetData[columnKey];
                    const column = columns[columnKey];
                    
                    families.forEach(family => {{
                        const familyBox = createFamilyBox(family);
                        column.appendChild(familyBox);
                    }});
                }});
            }}

            document.addEventListener('DOMContentLoaded', initializeGrid);
        </script>
    </body>
    </html>
    """


def create_auto_start_handwriting_html(
    text, pen_style="Realistic", writing_style="Natural", animation_speed=4.0
):
    """Create HTML5 Canvas-based handwriting animation that auto-starts"""

    import json

    safe_text = json.dumps(text)

    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tigrinya Handwriting Animation</title>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: 'Noto Sans Ethiopic', Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}

                .container {{
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.1);
                    padding: 30px;
                    max-width: 90%;
                    width: 100%;
                }}

                .title {{
                    text-align: center;
                    color: #2c3e50;
                    font-size: 2.5em;
                    margin-bottom: 20px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                }}

                .character-display {{
                    text-align: center;
                    font-size: 4em;
                    color: #e74c3c;
                    margin: 20px 0;
                    font-weight: bold;
                }}

                #canvas {{
                    border: 3px solid #3498db;
                    border-radius: 15px;
                    box-shadow: inset 0 4px 8px rgba(0,0,0,0.1);
                    background: #fafafa;
                    margin: 20px auto;
                    display: block;
                }}

                .controls {{
                    text-align: center;
                    margin: 20px 0;
                }}

                .btn {{
                    background: linear-gradient(45deg, #3498db, #2980b9);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 25px;
                    margin: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
                }}

                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
                }}

                .status {{
                    text-align: center;
                    margin: 15px 0;
                    font-size: 1.2em;
                    color: #34495e;
                }}

                .progress-bar {{
                    width: 100%;
                    height: 8px;
                    background: #ecf0f1;
                    border-radius: 4px;
                    overflow: hidden;
                    margin: 10px 0;
                }}

                .progress-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #3498db, #2ecc71);
                    border-radius: 4px;
                    transition: width 0.3s ease;
                    width: 0%;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="title">ትግርኛ ምስሊ (Tigrinya Writing)</div>
                <div class="character-display" id="currentChar">{text}</div>

                <canvas id="canvas" width="500" height="400"></canvas>

                <div class="progress-bar">
                    <div class="progress-fill" id="progressBar"></div>
                </div>

                <div class="status" id="status">Loading animation...</div>

                <div class="controls">
                    <button class="btn" onclick="startAnimation()">▶️ Start</button>
                    <button class="btn" onclick="clearCanvas()">🔄 Clear</button>
                    <button class="btn" onclick="pauseAnimation()">⏸️ Pause</button>
                </div>
            </div>

            <script>
                const canvas = document.getElementById('canvas');
                const ctx = canvas.getContext('2d');
                const text = {safe_text};
                let animationSpeed = {animation_speed};
                let isAnimating = false;
                let animationFrameId;
                let currentStep = 0;
                let totalSteps = 0;

                // Simple stroke patterns for basic characters
                const strokePatterns = {{
                    'አ': [
                        [[200, 100], [250, 150], [200, 200], [250, 250]],
                        [[300, 150], [250, 200], [300, 250]]
                    ],
                    'ኡ': [
                        [[200, 150], [250, 100], [300, 150]],
                        [[250, 150], [250, 300]]
                    ],
                    'ኢ': [
                        [[200, 100], [300, 100]],
                        [[250, 100], [250, 300]]
                    ],
                    'default': [
                        [[200, 150], [300, 150]],
                        [[250, 100], [250, 300]]
                    ]
                }};

                function getStrokePattern(char) {{
                    return strokePatterns[char] || strokePatterns['default'];
                }}

                function drawStroke(points, progress) {{
                    if (points.length < 2) return;

                    ctx.strokeStyle = '#2c3e50';
                    ctx.lineWidth = 4;
                    ctx.lineCap = 'round';
                    ctx.lineJoin = 'round';

                    ctx.beginPath();
                    ctx.moveTo(points[0][0], points[0][1]);

                    const totalPoints = points.length;
                    const currentPoint = Math.min(Math.floor(progress * totalPoints), totalPoints - 1);

                    for (let i = 1; i <= currentPoint; i++) {{
                        ctx.lineTo(points[i][0], points[i][1]);
                    }}

                    // Draw partial segment
                    if (currentPoint < totalPoints - 1) {{
                        const segmentProgress = (progress * totalPoints) - currentPoint;
                        const current = points[currentPoint];
                        const next = points[currentPoint + 1];
                        const x = current[0] + (next[0] - current[0]) * segmentProgress;
                        const y = current[1] + (next[1] - current[1]) * segmentProgress;
                        ctx.lineTo(x, y);
                    }}

                    ctx.stroke();
                }}

                function clearCanvas() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    currentStep = 0;
                    document.getElementById('progressBar').style.width = '0%';
                    document.getElementById('status').textContent = 'Canvas cleared';
                }}

                function pauseAnimation() {{
                    isAnimating = false;
                    if (animationFrameId) {{
                        cancelAnimationFrame(animationFrameId);
                    }}
                    document.getElementById('status').textContent = 'Animation paused';
                }}

                function startAnimation() {{
                    if (isAnimating) return;

                    clearCanvas();
                    isAnimating = true;
                    currentStep = 0;

                    const strokes = getStrokePattern(text);
                    totalSteps = strokes.length * 100;

                    document.getElementById('status').textContent = 'Animation starting...';
                    animate(strokes);
                }}

                function animate(strokes) {{
                    if (!isAnimating) return;

                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    const strokeIndex = Math.floor(currentStep / 100);
                    const strokeProgress = (currentStep % 100) / 100;

                    // Draw completed strokes
                    for (let i = 0; i < strokeIndex; i++) {{
                        drawStroke(strokes[i], 1.0);
                    }}

                    // Draw current stroke
                    if (strokeIndex < strokes.length) {{
                        drawStroke(strokes[strokeIndex], strokeProgress);
                    }}

                    // Update progress
                    const totalProgress = (currentStep / totalSteps) * 100;
                    document.getElementById('progressBar').style.width = totalProgress + '%';

                    currentStep++;

                    if (currentStep < totalSteps) {{
                        animationFrameId = requestAnimationFrame(() => animate(strokes));
                    }} else {{
                        document.getElementById('status').textContent = 'Animation complete!';
                        isAnimating = false;
                    }}
                }}

                // Auto-start animation after 1 second
                setTimeout(startAnimation, 1000);
            </script>
        </body>
        </html>
    """
    return html_content


def render():
    """Render the traditional three-column Tigrinya alphabet layout"""

    # Initialize session state
    if "selected_character" not in st.session_state:
        st.session_state.selected_character = " " 
    if "animation_character" not in st.session_state:
        st.session_state.animation_character = None

    # Page header
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='color: #2c3e50; font-size: 3em; margin-bottom: 10px;'>ፊደላት</h1>
            <h2 style='color: #34495e; font-size: 1.8em; margin-bottom: 20px;'>Traditional Tigrinya Alphabet</h2>
            <p style='color: #7f8c8d; font-size: 1.2em;'>Click any character to see handwriting animation</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Get alphabet structure
    alphabet_structure = create_traditional_alphabet_structure()

    # Create the interactive alphabet grid using HTML with proper DOM manipulation
    alphabet_grid_html = create_alphabet_grid_html(alphabet_structure)

    # Display the grid
    selected_char_result = components.html(alphabet_grid_html, height=3200)


    # Character animation section
    if st.session_state.selected_character and st.session_state.selected_character != " ":
        st.markdown("---")
        st.markdown("### Character Animation & Details")

        col_info, col_animation = st.columns([1, 2])

        with col_info:
            selected_char = st.session_state.selected_character
            st.markdown(
                f"""
                <div style='
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px;
                    border-radius: 15px;
                    color: white;
                    text-align: center;
                    margin: 20px 0;
                '>
                    <h1 style='font-size: 4em; margin: 0; font-family: "Noto Sans Ethiopic", serif;'>{selected_char}</h1>
                    <h3 style='margin: 10px 0;'>Selected Character</h3>
                </div>
            """,
                unsafe_allow_html=True,
            )

            # Find character family info
            for column_key in alphabet_structure:
                for family in alphabet_structure[column_key]:
                    for char_obj in family["characters"]:
                        if char_obj["char"] == selected_char:
                            st.info(f"**Family:** {family['familyName']}")
                            st.info(f"**Sound:** {char_obj['sound']}")
                            st.info(f"**Example:** {family['exampleWord']}")
                            st.info(f"**Icon:** {family['icon']}")
                            break

        with col_animation:
            st.markdown("#### Handwriting Animation")
            character_to_animate = st.session_state.animation_character or selected_char

            # Generate handwriting animation
            animation_html = create_auto_start_handwriting_html(
                text=character_to_animate,
                pen_style="Realistic",
                writing_style="Natural",
                animation_speed=3.0,
            )

            components.html(animation_html, height=600)

            st.markdown("#### Practice Writing")
            st.info("Watch the animation and practice writing this character!")

    else:
        st.info(
            "👆 Click any character above to see its handwriting animation and details!"
        )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #7f8c8d; margin-top: 40px;'>
            <p><strong>Traditional Tigrinya Alphabet Learning System</strong></p>
            <p>Learn the beautiful Tigrinya script with interactive animations</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    render()