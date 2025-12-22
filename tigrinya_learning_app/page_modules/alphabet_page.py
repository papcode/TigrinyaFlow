"""
Tigrinya Alphabet Learning Page - Traditional Three-Column Layout
Complete implementation matching traditional Tigrinya alphabet educational materials
"""

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from utils.image_loader import ImageLoader
import urllib.parse

from clientTranslation import alef_row, feedel_rows, geez_to_latin_syllable


def create_traditional_alphabet_structure():
    """Create the traditional three-column alphabet structure with corrected data."""
    
    alphabet_data = {
    "column1": [{
            "family": "be",
            "familyName": "Be Family",
            "baseName": "በ",
            "baseChar": "በ",
            "exampleWord": "በጊዕ (sheep)",
            "icon": "🐑",
            "color": "#E63946",
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
            "color": "#06BCC1",
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
            "exampleWord": "ሸውዓተ (seven)",
            "icon": "7️⃣",
            "color": "#2A9D8F",
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
            "color": "#52B788",
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
            "color": "#F4A261",
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
            "exampleWord": "ለሚን (lemon)",
            "icon": "🍋",
            "color": "#F9C74F",
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
            "baseName": "አ",
            "baseChar": "አ",
            "exampleWord": "ኣንበሳ (lion)",
            "icon": "🦁",
            "color": "#E76F51",
            "characters": [
                { "char": "አ", "sound": "e" },
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
            "exampleWord": "ጸባ (milk)",
            "icon": "",
            "color": "#9D4EDD",
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
            "exampleWord": "ድሙ (cat)",
            "icon": "🐱",
            "color": "#FF6B9D",
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
            "color": "#4ECDC4",
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
            "color": "#FFB627",
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
    "column2": [{
            "family": "He",
            "familyName": "He Family",
            "baseName": "ሐ",
            "baseChar": "ሐ",
            "exampleWord": "ሓዊ (fire)",
            "icon": "🔥",
            "color": "#D62828",
            "characters": [
                { "char": "ሐ", "sound": "He" },
                { "char": "ሑ", "sound": "Hu" },
                { "char": "ሒ", "sound": "Hi" },
                { "char": "ሓ", "sound": "Ha" },
                { "char": "ሔ", "sound": "Hie" },
                { "char": "ሕ", "sound": "H" },
                { "char": "ሖ", "sound": "Ho" }
            ]
        },
        {
            "family": "te2",
            "familyName": "Te Family (variant)",
            "baseName": "ጠ",
            "baseChar": "ጠ",
            "exampleWord": "ጠረጴዛ (table)",
            "icon": " ",
            "color": "#8B5A3C",
            "characters": [
                { "char": "ጠ", "sound": "te" },
                { "char": "ጡ", "sound": "tu" },
                { "char": "ጢ", "sound": "ti" },
                { "char": "ጣ", "sound": "ta" },
                { "char": "ጤ", "sound": "tie" },
                { "char": "ጥ", "sound": "t" },
                { "char": "ጦ", "sound": "to" }
            ]
        },
        {
            "family": "che",
            "familyName": "Che Family",
            "baseName": "ጨ",
            "baseChar": "ጨ",
            "exampleWord": "ጨና (perfume)",
            "icon": "⚱💨",
            "color": "#C77DFF",
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
            "family": "te",
            "familyName": "Te Family",
            "baseName": "ተ",
            "baseChar": "ተ",
            "exampleWord": "ተመን (snake)",
            "icon": "🐍",
            "color": "#588157",
            "characters": [
                { "char": "ተ", "sound": "te" },
                { "char": "ቱ", "sound": "tu" },
                { "char": "ቲ", "sound": "ti" },
                { "char": "ታ", "sound": "ta" },
                { "char": "ቴ", "sound": "tie" },
                { "char": "ት", "sound": "t" },
                { "char": "ቶ", "sound": "to" }
            ]
        },
        {
            "family": "qe",
            "familyName": "Qe Family",
            "baseName": "ቀ",
            "baseChar": "ቀ",
            "exampleWord": "ቆቢዕ (hat)",
            "icon": "",
            "color": "#BC4749",
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
            "family": "qhe",
            "familyName": "Qhe Family",
            "baseName": "ቐ",
            "baseChar": "ቐ",
            "exampleWord": "መቐስ (scissors)",
            "icon": "✂️",
            "color": "#2D6A4F",
            "characters": [
                { "char": "ቐ", "sound": "qhe" },
                { "char": "ቑ", "sound": "qhu" },
                { "char": "ቒ", "sound": "qhi" },
                { "char": "ቓ", "sound": "qha" },
                { "char": "ቔ", "sound": "qhie" },
                { "char": "ቕ", "sound": "qh" },
                { "char": "ቖ", "sound": "qho" }
            ]
        },
        {
            "family": "ge",
            "familyName": "Ge Family",
            "baseName": "ገ",
            "baseChar": "ገ",
            "exampleWord": "ገዛ (house)",
            "icon": "🏠",
            "color": "#1B9AAA",
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
            "icon": "🐅",
            "color": "#F77F00",
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
            "exampleWord": "የማን (right-side)",
            "icon": "",
            "color": "#6C757D",
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
            "color": "#90BE6D",
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
            "family": "fe2",
            "familyName": "Fe Family (variant)",
            "baseName": "ፈ",
            "baseChar": "ፈ",
            "exampleWord": "ፈረስ (horse)",
            "icon": "🐴",
            "color": "#6F4E37",
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
    "column3": [{
            "family": "he",
            "familyName": "He Family",
            "baseName": "ሀ",
            "baseChar": "ሀ",
            "exampleWord": "ሆስፒታል (hospital)",
            "icon": "",
            "color": "#A0826D",
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
            "family": "e",
            "familyName": "'e Family",
            "baseName": "ዐ",
            "baseChar": "ዐ",
            "exampleWord": "ዓራት (bed)",
            "icon": "🛏️",
            "color": "#0077B6",
            "characters": [
                { "char": "ዐ", "sound": "e" },
                { "char": "ዑ", "sound": "u" },
                { "char": "ዒ", "sound": "i" },
                { "char": "ዓ", "sound": "a" },
                { "char": "ዔ", "sound": "ie" },
                { "char": "ዕ", "sound": "i" },
                { "char": "ዖ", "sound": "o" }
            ]
        },
        {
            "family": "we",
            "familyName": "We Family",
            "baseName": "ወ",
            "baseChar": "ወ",
            "exampleWord": "ወረቐት (paper)",
            "icon": "📄",
            "color": "#495057",
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
            "color": "#EF233C",
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
            "color": "#FF8C42",
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
            "baseName": "ቸ",
            "baseChar": "ቸ",
            "exampleWord": "ቻው (bye)",
            "icon": "👥",
            "color": "#7209B7",
            "characters": [
                { "char": "ቸ", "sound": "che" },
                { "char": "ቹ", "sound": "chu" },
                { "char": "ቺ", "sound": "chi" },
                { "char": "ቻ", "sound": "cha" },
                { "char": "ቼ", "sound": "chie" },
                { "char": "ች", "sound": "ch" },
                { "char": "ቾ", "sound": "cho" }
            ]
        },
        {
            "family": "nye",
            "familyName": "Nye Family",
            "baseName": "ኘ",
            "baseChar": "ኘ",
            "exampleWord": "ኛው (maeW)",
            "icon": "🐱",
            "color": "#9C6644",
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
            "family": "ve",
            "familyName": "Ve Family",
            "baseName": "ቨ",
            "baseChar": "ቨ",
            "exampleWord": "ቪድዮ ካሜራ (video camera)",
            "icon": "📹",
            "color": "#2B2D42",
            "characters": [
                { "char": "ቨ", "sound": "ve" },
                { "char": "ቩ", "sound": "vu" },
                { "char": "ቪ", "sound": "vi" },
                { "char": "ቫ", "sound": "va" },
                { "char": "ቬ", "sound": "vie" },
                { "char": "ቭ", "sound": "v" },
                { "char": "ቮ", "sound": "vo" }
            ]
        },
        {
            "family": "pe2",
            "familyName": "Pe Family (variant)",
            "baseName": "ጰ",
            "baseChar": "ጰ",
            "exampleWord": "ጳጳስ (pope)",
            "icon": "👴🏼",
            "color": "#4895EF",
            "characters": [
                { "char": "ጰ", "sound": "pe" },
                { "char": "ጱ", "sound": "pu" },
                { "char": "ጲ", "sound": "pi" },
                { "char": "ጳ", "sound": "pa" },
                { "char": "ጴ", "sound": "pie" },
                { "char": "ጵ", "sound": "p" },
                { "char": "ጶ", "sound": "po" }
            ]
        },
        {
            "family": "zhe",
            "familyName": "Zhe Family",
            "baseName": "ዠ",
            "baseChar": "ዠ",
            "exampleWord": "ተሌቪዥን (television)",
            "icon": "📺",
            "color": "#1A1A1A",
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


def create_alphabet_grid_html(alphabet_structure, selected_char=None):
    """Create complete alphabet grid with integrated modal animation - Clean solution"""
    import json

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
            
            /* Modal Overlay Styles */
            .modal-overlay {{
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                backdrop-filter: blur(8px);
                z-index: 10000;
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.3s ease;
            }}
            
            .modal-overlay.active {{
                display: flex;
            }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            
            @keyframes slideUp {{
                from {{
                    opacity: 0;
                    transform: translateY(30px) scale(0.95);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }}
            }}
            
            .modal-content {{
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.98) 100%);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 40px;
                max-width: 900px;
                width: 90%;
                max-height: 90vh;
                overflow-y: auto;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.3);
                animation: slideUp 0.3s ease;
                position: relative;
            }}
            
            .modal-header {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 20px;
                border-bottom: 2px solid rgba(102, 126, 234, 0.2);
                position: relative;
                text-align: center;
            }}

            .modal-char-display {{
                font-size: 6em;
                font-weight: bold;
                font-family: 'Noto Sans Ethiopic', serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                line-height: 1;
            }}

            .modal-family-info {{
                font-size: 1.5em;
                font-weight: 500;
                color: #764ba2;
                margin-top: 10px;
            }}
            
            .modal-close-btn {{
                position: absolute;
                top: -10px;
                right: -10px;
                background: rgba(255, 255, 255, 0.8);
                border: 2px solid rgba(102, 126, 234, 0.3);
                border-radius: 50%;
                width: 40px;
                height: 40px;
                font-size: 24px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s ease;
                color: #667eea;
                font-weight: bold;
            }}
            
            .modal-close-btn:hover {{
                background: rgba(102, 126, 234, 0.1);
                transform: rotate(90deg);
                border-color: #667eea;
            }}
            
            .modal-animation-container {{
                background: white;
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
                min-height: 350px;
                display: flex;
                align-items: center;
                justify-content: center;
            }}
            
            .modal-canvas-container {{
                width: 100%;
                max-width: 800px;
                max-height: 400px;
                overflow: auto;
                border-radius: 10px;
                border: 1px solid #e1e8ed;
                background: white;
            }}
            
            #modalAnimationCanvas {{
                display: block;
                background: white;
            }}
            
            .modal-progress-container {{
                margin: 20px 0;
            }}
            
            .modal-progress-bar {{
                width: 100%;
                height: 8px;
                background: #ecf0f1;
                border-radius: 4px;
                overflow: hidden;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .modal-progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 4px;
                width: 0%;
                transition: width 0.3s ease;
                box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
            }}
            
            .modal-status {{
                text-align: center;
                margin: 15px 0;
                font-weight: 600;
                font-size: 1.1em;
                color: #2c3e50;
            }}
            
            .modal-controls {{
                display: flex;
                gap: 10px;
                justify-content: center;
                margin-top: 20px;
            }}
            
            .modal-btn {{
                padding: 12px 24px;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }}
            
            .modal-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }}
            
            .modal-btn:active {{
                transform: translateY(0);
            }}
            
            .modal-btn.secondary {{
                background: linear-gradient(135deg, #95a5a6 0%, #7f8c8d 100%);
                box-shadow: 0 4px 15px rgba(149, 165, 166, 0.3);
            }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/opentype.js/1.3.4/opentype.min.js"></script>
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
        
        <!-- Modal Overlay -->
        <div class="modal-overlay" id="charModal">
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <div>
                        <h1 class="modal-char-display" id="modalCharDisplay"></h1>
                        <div class="modal-family-info" id="modalFamilyInfo"></div>
                    </div>
                    <button class="modal-close-btn" onclick="closeModal()" title="Close (ESC)">×</button>
                </div>
                
                <div class="modal-animation-container">
                    <div class="modal-canvas-container" id="modalCanvasContainer">
                        <canvas id="modalAnimationCanvas"></canvas>
                    </div>
                </div>
                
                <div class="modal-progress-container">
                    <div class="modal-progress-bar">
                        <div class="modal-progress-fill" id="modalProgressFill"></div>
                    </div>
                    <div class="modal-status" id="modalStatus">Loading font and preparing animation...</div>
                </div>
                
                <div class="modal-controls">
                    <button class="modal-btn" id="modalStartBtn" onclick="startModalAnimation()">▶ Start</button>
                    <button class="modal-btn secondary" id="modalResetBtn" onclick="resetModalAnimation()">↻ Reset</button>
                </div>
            </div>
        </div>

        <script>
            const alphabetData = {alphabet_data};
            let currentAnimation = null;
            let modalAnimationConfig = null;
            
            // Open modal with character - Clean solution, no cross-frame communication needed
            function selectCharacter(char) {{
                // Visual feedback
                const buttons = document.querySelectorAll('.char-btn');
                buttons.forEach(btn => {{
                    const charDisplay = btn.querySelector('.char-display');
                    if (charDisplay && charDisplay.textContent === char) {{
                        btn.style.transform = 'scale(1.15)';
                        btn.style.boxShadow = '0 6px 16px rgba(0,0,0,0.3)';
                        btn.style.backgroundColor = 'rgba(255, 255, 255, 0.5)';
                        setTimeout(() => {{
                            btn.style.transform = '';
                            btn.style.boxShadow = '';
                            btn.style.backgroundColor = '';
                        }}, 300);
                    }}
                }});

                // Find family info
                let familyName = '';
                let baseName = '';
                for (const columnKey in alphabetData) {{
                    for (const family of alphabetData[columnKey]) {{
                        if (family.characters.find(c => c.char === char)) {{
                            familyName = family.familyName;
                            baseName = family.baseName;
                            break;
                        }}
                    }}
                    if (familyName) break;
                }}
                
                // Open modal
                openModal(char, baseName, familyName);
            }}
            
            // Modal functions
            function openModal(char, baseName, familyName) {{
                const modal = document.getElementById('charModal');
                const charDisplay = document.getElementById('modalCharDisplay');
                const familyInfoDisplay = document.getElementById('modalFamilyInfo');

                charDisplay.textContent = char;
                if (familyName) {{
                    familyInfoDisplay.textContent = `${{baseName}} - ${{familyName}}`;
                }} else {{
                    familyInfoDisplay.textContent = '';
                }}

                modal.classList.add('active');
                
                // Initialize animation
                initializeModalAnimation(char);
                
                // Auto-start animation after 300ms
                setTimeout(() => {{
                    startModalAnimation();
                }}, 300);
            }}
            
            function closeModal() {{
                const modal = document.getElementById('charModal');
                modal.classList.remove('active');
                if (currentAnimation && currentAnimation.stop) {{
                    currentAnimation.stop();
                }}
            }}
            
            // Close modal on background click
            document.getElementById('charModal').addEventListener('click', function(e) {{
                if (e.target === this) {{
                    closeModal();
                }}
            }});
            
            // Close modal on ESC key
            document.addEventListener('keydown', function(e) {{
                if (e.key === 'Escape') {{
                    closeModal();
                }}
            }});
            
            // Initialize handwriting animation in modal
            function initializeModalAnimation(char) {{
                const canvas = document.getElementById('modalAnimationCanvas');
                const container = document.getElementById('modalCanvasContainer');
                
                // Reset progress
                document.getElementById('modalProgressFill').style.width = '0%';
                document.getElementById('modalStatus').textContent = 'Loading font and preparing animation...';
                
                // Set canvas size
                const canvasWidth = 800;
                const canvasHeight = 300;
                canvas.width = canvasWidth;
                canvas.height = canvasHeight;
                
                const ctx = canvas.getContext('2d');
                
                // Create animation config
                modalAnimationConfig = {{
                    text: char,
                    fontSize: 180,
                    font: null,
                    canvas: canvas,
                    ctx: ctx,
                    glyphCanvas: null,
                    glyphCtx: null,
                    maskCanvas: null,
                    maskCtx: null,
                    isAnimating: false,
                    currentCharIndex: 0,
                    currentPointIndex: 0,
                    characters: [],
                    nibRadius: 7,
                    inkColor: '#2c3e50',
                    penX: 0,
                    penY: 0,
                    penPressure: 1.0,
                    penSpeed: 0,
                    animationFrame: null,
                    lastFrameTime: 0,
                    frameCount: 0,
                    animationSpeed: 3.0,
                    stepSize: 2,
                    canvasWidth: canvasWidth,
                    canvasHeight: canvasHeight
                }};
                
                // Create offscreen canvases
                modalAnimationConfig.glyphCanvas = document.createElement('canvas');
                modalAnimationConfig.glyphCanvas.width = canvasWidth;
                modalAnimationConfig.glyphCanvas.height = canvasHeight;
                modalAnimationConfig.glyphCtx = modalAnimationConfig.glyphCanvas.getContext('2d');
                
                modalAnimationConfig.maskCanvas = document.createElement('canvas');
                modalAnimationConfig.maskCanvas.width = canvasWidth;
                modalAnimationConfig.maskCanvas.height = canvasHeight;
                modalAnimationConfig.maskCtx = modalAnimationConfig.maskCanvas.getContext('2d');
                
                // Configure rendering
                [ctx, modalAnimationConfig.glyphCtx, modalAnimationConfig.maskCtx].forEach(c => {{
                    c.imageSmoothingEnabled = true;
                    c.imageSmoothingQuality = 'high';
                    c.lineCap = 'round';
                    c.lineJoin = 'round';
                }});
                
                // Load font
                if (typeof opentype !== 'undefined') {{
                    opentype.load('https://fonts.gstatic.com/s/notosansethiopic/v49/7cHPv50vjIepfJVOZZgcpQ5B9FBTH9KGNfhSTgtoow1KVnIvyBoMSzUMacb-T35OK6Dj.ttf', 
                        function(err, font) {{
                            if (err) {{
                                console.error('Font loading error:', err);
                                document.getElementById('modalStatus').textContent = 'Error loading font. Using fallback...';
                                prepareCharacterPathsFallback();
                            }} else {{
                                modalAnimationConfig.font = font;
                                document.getElementById('modalStatus').textContent = 'Font loaded - Ready to animate';
                                prepareCharacterPaths();
                            }}
                        }});
                }} else {{
                    // Load opentype.js if not available
                    const script = document.createElement('script');
                    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/opentype.js/1.3.4/opentype.min.js';
                    script.onload = function() {{
                        opentype.load('https://fonts.gstatic.com/s/notosansethiopic/v49/7cHPv50vjIepfJVOZZgcpQ5B9FBTH9KGNfhSTgtoow1KVnIvyBoMSzUMacb-T35OK6Dj.ttf', 
                            function(err, font) {{
                                if (err) {{
                                    prepareCharacterPathsFallback();
                                }} else {{
                                    modalAnimationConfig.font = font;
                                    prepareCharacterPaths();
                                }}
                            }});
                    }};
                    document.head.appendChild(script);
                }}
            }}
            
            function prepareCharacterPaths() {{
                const baseY = modalAnimationConfig.canvasHeight / 2 + modalAnimationConfig.fontSize / 4;
                let currentX = (modalAnimationConfig.canvasWidth - modalAnimationConfig.fontSize * 0.7) / 2;
                
                modalAnimationConfig.glyphCtx.fillStyle = 'white';
                modalAnimationConfig.glyphCtx.fillRect(0, 0, modalAnimationConfig.canvasWidth, modalAnimationConfig.canvasHeight);
                
                if (modalAnimationConfig.font) {{
                    modalAnimationConfig.glyphCtx.font = `${{modalAnimationConfig.fontSize}}px 'Noto Sans Ethiopic'`;
                    modalAnimationConfig.glyphCtx.fillStyle = modalAnimationConfig.inkColor;
                    modalAnimationConfig.glyphCtx.fillText(modalAnimationConfig.text, currentX, baseY);
                    
                    try {{
                        const fontPath = modalAnimationConfig.font.getPath(modalAnimationConfig.text, currentX, baseY, modalAnimationConfig.fontSize);
                        const points = extractPathPoints(fontPath);
                        modalAnimationConfig.characters = [{{
                            char: modalAnimationConfig.text,
                            type: 'character',
                            x: currentX,
                            y: baseY,
                            points: resamplePath(points, modalAnimationConfig.stepSize)
                        }}];
                    }} catch (e) {{
                        console.warn('Error generating path:', e);
                        prepareCharacterPathsFallback();
                    }}
                }} else {{
                    prepareCharacterPathsFallback();
                }}
            }}
            
            function prepareCharacterPathsFallback() {{
                const baseY = modalAnimationConfig.canvasHeight / 2;
                const currentX = modalAnimationConfig.canvasWidth / 2;
                modalAnimationConfig.glyphCtx.font = `${{modalAnimationConfig.fontSize}}px 'Noto Sans Ethiopic'`;
                modalAnimationConfig.glyphCtx.fillStyle = modalAnimationConfig.inkColor;
                modalAnimationConfig.glyphCtx.textAlign = 'center';
                modalAnimationConfig.glyphCtx.textBaseline = 'middle';
                modalAnimationConfig.glyphCtx.fillText(modalAnimationConfig.text, currentX, baseY);
                // Simple fallback path
                const charWidth = modalAnimationConfig.fontSize * 0.6;
                const charHeight = modalAnimationConfig.fontSize * 0.8;
                modalAnimationConfig.characters = [{{
                    char: modalAnimationConfig.text,
                    type: 'character',
                    x: currentX - charWidth/2,
                    y: baseY,
                    points: [
                        {{x: currentX - charWidth/2, y: baseY - charHeight * 0.7}},
                        {{x: currentX + charWidth/2, y: baseY - charHeight * 0.7}},
                        {{x: currentX + charWidth/2, y: baseY}},
                        {{x: currentX - charWidth/2, y: baseY}},
                        {{x: currentX - charWidth/2, y: baseY - charHeight * 0.7}}
                    ]
                }}];
            }}
            
            function extractPathPoints(path) {{
                const points = [];
                let currentContour = [];
                
                for (const cmd of path.commands) {{
                    switch (cmd.type) {{
                        case 'M':
                            if (currentContour.length > 0) points.push(...currentContour);
                            currentContour = [{{x: cmd.x, y: cmd.y}}];
                            break;
                        case 'L':
                            currentContour.push({{x: cmd.x, y: cmd.y}});
                            break;
                        case 'Q':
                            const qStart = currentContour[currentContour.length - 1] || {{x: 0, y: 0}};
                            const qCurve = sampleQuadraticBezier(qStart, {{x: cmd.x1, y: cmd.y1}}, {{x: cmd.x, y: cmd.y}}, 0.1);
                            currentContour.push(...qCurve.slice(1));
                            break;
                        case 'C':
                            const cStart = currentContour[currentContour.length - 1] || {{x: 0, y: 0}};
                            const cCurve = sampleCubicBezier(cStart, {{x: cmd.x1, y: cmd.y1}}, {{x: cmd.x2, y: cmd.y2}}, {{x: cmd.x, y: cmd.y}}, 0.1);
                            currentContour.push(...cCurve.slice(1));
                            break;
                        case 'Z':
                            if (currentContour.length > 0) {{
                                points.push(...currentContour);
                                currentContour = [];
                            }}
                            break;
                    }}
                }}
                if (currentContour.length > 0) points.push(...currentContour);
                return points;
            }}
            
            function sampleQuadraticBezier(p0, p1, p2, step) {{
                const points = [];
                for (let t = 0; t <= 1; t += step) {{
                    const x = Math.pow(1-t, 2) * p0.x + 2*(1-t)*t * p1.x + Math.pow(t, 2) * p2.x;
                    const y = Math.pow(1-t, 2) * p0.y + 2*(1-t)*t * p1.y + Math.pow(t, 2) * p2.y;
                    points.push({{x, y}});
                }}
                return points;
            }}
            
            function sampleCubicBezier(p0, p1, p2, p3, step) {{
                const points = [];
                for (let t = 0; t <= 1; t += step) {{
                    const x = Math.pow(1-t, 3) * p0.x + 3 * Math.pow(1-t, 2) * t * p1.x + 
                             3 * (1-t) * Math.pow(t, 2) * p2.x + Math.pow(t, 3) * p3.x;
                    const y = Math.pow(1-t, 3) * p0.y + 3 * Math.pow(1-t, 2) * t * p1.y + 
                             3 * (1-t) * Math.pow(t, 2) * p2.y + Math.pow(t, 3) * p3.y;
                    points.push({{x, y}});
                }}
                return points;
            }}
            
            function resamplePath(path, stepSize) {{
                if (path.length < 2) return path;
                const resampled = [path[0]];
                let currentDistance = 0;
                
                for (let i = 1; i < path.length; i++) {{
                    const prev = path[i - 1];
                    const curr = path[i];
                    const segmentLength = Math.sqrt(Math.pow(curr.x - prev.x, 2) + Math.pow(curr.y - prev.y, 2));
                    currentDistance += segmentLength;
                    
                    while (currentDistance >= stepSize) {{
                        const t = (stepSize - (currentDistance - segmentLength)) / segmentLength;
                        resampled.push({{
                            x: prev.x + (curr.x - prev.x) * t,
                            y: prev.y + (curr.y - prev.y) * t
                        }});
                        currentDistance -= stepSize;
                    }}
                }}
                if (path.length > 0) resampled.push(path[path.length - 1]);
                return resampled;
            }}
            
            function paintNib(x, y, pressure = 1.0) {{
                modalAnimationConfig.maskCtx.save();
                modalAnimationConfig.maskCtx.translate(x, y);
                const radius = modalAnimationConfig.nibRadius * pressure;
                const gradient = modalAnimationConfig.maskCtx.createRadialGradient(0, 0, 0, 0, 0, radius);
                gradient.addColorStop(0, 'black');
                gradient.addColorStop(0.7, 'rgba(0,0,0,0.8)');
                gradient.addColorStop(1, 'rgba(0,0,0,0.3)');
                modalAnimationConfig.maskCtx.fillStyle = gradient;
                modalAnimationConfig.maskCtx.beginPath();
                modalAnimationConfig.maskCtx.arc(0, 0, radius, 0, Math.PI * 2);
                modalAnimationConfig.maskCtx.fill();
                modalAnimationConfig.maskCtx.restore();
            }}
            
            function drawPen(x, y, angle = 0, pressure = 1.0) {{
                const ctx = modalAnimationConfig.ctx;
                ctx.save();
                ctx.translate(x, y);
                ctx.rotate(angle);
                const scale = 0.8 + pressure * 0.4;
                ctx.scale(scale, scale);
                ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
                ctx.fillRect(-4, 4, 8, 35);
                const gradient = ctx.createLinearGradient(0, 0, 0, 30);
                gradient.addColorStop(0, '#4169E1');
                gradient.addColorStop(0.5, '#6495ED');
                gradient.addColorStop(1, '#1E3A8A');
                ctx.fillStyle = gradient;
                ctx.fillRect(-3.5, 0, 7, 30);
                ctx.fillStyle = '#696969';
                ctx.fillRect(-4, 10, 8, 10);
                ctx.fillStyle = '#000080';
                ctx.beginPath();
                ctx.arc(0, -2, 2.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
                ctx.fillRect(-1, 2, 2, 15);
                ctx.restore();
            }}
            
            function compositeFrame() {{
                modalAnimationConfig.ctx.clearRect(0, 0, modalAnimationConfig.canvas.width, modalAnimationConfig.canvas.height);
                modalAnimationConfig.ctx.fillStyle = 'white';
                modalAnimationConfig.ctx.fillRect(0, 0, modalAnimationConfig.canvas.width, modalAnimationConfig.canvas.height);
                modalAnimationConfig.ctx.drawImage(modalAnimationConfig.glyphCanvas, 0, 0);
                modalAnimationConfig.ctx.globalCompositeOperation = 'destination-in';
                modalAnimationConfig.ctx.drawImage(modalAnimationConfig.maskCanvas, 0, 0);
                modalAnimationConfig.ctx.globalCompositeOperation = 'source-over';
                if (modalAnimationConfig.isAnimating) {{
                    drawPen(modalAnimationConfig.penX, modalAnimationConfig.penY - 40, 0, modalAnimationConfig.penPressure);
                }}
            }}
            
            function calculatePenPressure(speed, pointIndex, totalPoints) {{
                let pressure = 1.0;
                if (speed > 0) pressure *= Math.max(0.5, 2.0 - speed / 10);
                const progress = pointIndex / totalPoints;
                if (progress < 0.1) pressure *= 0.7 + progress * 3;
                else if (progress > 0.9) pressure *= 0.7 + (1 - progress) * 3;
                pressure *= 0.9 + Math.random() * 0.2;
                return Math.max(0.3, Math.min(1.5, pressure));
            }}
            
            function startModalAnimation() {{
                if (!modalAnimationConfig || modalAnimationConfig.isAnimating) return;
                resetModalAnimationState();
                modalAnimationConfig.isAnimating = true;
                modalAnimationConfig.maskCtx.clearRect(0, 0, modalAnimationConfig.canvasWidth, modalAnimationConfig.canvasHeight);
                updateModalProgress(0);
                document.getElementById('modalStatus').textContent = 'Animation starting...';
                modalAnimationConfig.lastFrameTime = performance.now();
                animateNextFrame();
            }}
            
            function resetModalAnimation() {{
                if (!modalAnimationConfig) return;
                if (modalAnimationConfig.isAnimating) {{
                    modalAnimationConfig.isAnimating = false;
                    if (modalAnimationConfig.animationFrame) {{
                        cancelAnimationFrame(modalAnimationConfig.animationFrame);
                    }}
                }}
                resetModalAnimationState();
                modalAnimationConfig.maskCtx.clearRect(0, 0, modalAnimationConfig.canvasWidth, modalAnimationConfig.canvasHeight);
                updateModalProgress(0);
                document.getElementById('modalStatus').textContent = 'Ready to animate';
                compositeFrame();
            }}
            
            function resetModalAnimationState() {{
                if (!modalAnimationConfig) return;
                modalAnimationConfig.currentCharIndex = 0;
                modalAnimationConfig.currentPointIndex = 0;
                modalAnimationConfig.penX = 0;
                modalAnimationConfig.penY = 0;
                modalAnimationConfig.penPressure = 1.0;
                modalAnimationConfig.penSpeed = 0;
                modalAnimationConfig.frameCount = 0;
            }}
            
            function animateNextFrame() {{
                if (!modalAnimationConfig || !modalAnimationConfig.isAnimating) return;
                
                const currentTime = performance.now();
                modalAnimationConfig.lastFrameTime = currentTime;
                modalAnimationConfig.frameCount++;
                
                if (modalAnimationConfig.currentCharIndex >= modalAnimationConfig.characters.length) {{
                    completeModalAnimation();
                    return;
                }}
                
                const character = modalAnimationConfig.characters[modalAnimationConfig.currentCharIndex];
                
                const totalPoints = modalAnimationConfig.characters.reduce((sum, char) => sum + char.points.length, 0);
                const currentPoints = modalAnimationConfig.characters.slice(0, modalAnimationConfig.currentCharIndex).reduce((sum, char) => sum + char.points.length, 0) + modalAnimationConfig.currentPointIndex;
                const progress = totalPoints > 0 ? (currentPoints / totalPoints) * 100 : 0;
                updateModalProgress(progress);
                
                if (modalAnimationConfig.currentPointIndex >= character.points.length) {{
                    modalAnimationConfig.currentCharIndex++;
                    modalAnimationConfig.currentPointIndex = 0;
                    setTimeout(() => {{
                        modalAnimationConfig.animationFrame = requestAnimationFrame(animateNextFrame);
                    }}, 100 / modalAnimationConfig.animationSpeed);
                    return;
                }}
                
                const point = character.points[modalAnimationConfig.currentPointIndex];
                if (!point) {{
                    modalAnimationConfig.currentPointIndex++;
                    modalAnimationConfig.animationFrame = requestAnimationFrame(animateNextFrame);
                    return;
                }}
                
                if (modalAnimationConfig.currentPointIndex > 0) {{
                    const prevPoint = character.points[modalAnimationConfig.currentPointIndex - 1];
                    modalAnimationConfig.penSpeed = Math.sqrt(Math.pow(point.x - prevPoint.x, 2) + Math.pow(point.y - prevPoint.y, 2));
                }}
                
                modalAnimationConfig.penX = point.x;
                modalAnimationConfig.penY = point.y;
                modalAnimationConfig.penPressure = calculatePenPressure(modalAnimationConfig.penSpeed, modalAnimationConfig.currentPointIndex, character.points.length);
                
                paintNib(modalAnimationConfig.penX, modalAnimationConfig.penY, modalAnimationConfig.penPressure);
                compositeFrame();
                
                modalAnimationConfig.currentPointIndex++;
                
                const baseDelay = 20;
                const speedAdjustedDelay = Math.max(5, baseDelay / modalAnimationConfig.animationSpeed);
                
                setTimeout(() => {{
                    modalAnimationConfig.animationFrame = requestAnimationFrame(animateNextFrame);
                }}, speedAdjustedDelay);
            }}
            
            function completeModalAnimation() {{
                if (!modalAnimationConfig) return;
                modalAnimationConfig.isAnimating = false;
                updateModalProgress(100);
                document.getElementById('modalStatus').textContent = `Animation complete! (${{modalAnimationConfig.frameCount}} frames)`;
                modalAnimationConfig.ctx.clearRect(0, 0, modalAnimationConfig.canvas.width, modalAnimationConfig.canvas.height);
                modalAnimationConfig.ctx.fillStyle = 'white';
                modalAnimationConfig.ctx.fillRect(0, 0, modalAnimationConfig.canvas.width, modalAnimationConfig.canvas.height);
                modalAnimationConfig.ctx.drawImage(modalAnimationConfig.glyphCanvas, 0, 0);
                modalAnimationConfig.ctx.globalCompositeOperation = 'destination-in';
                modalAnimationConfig.ctx.drawImage(modalAnimationConfig.maskCanvas, 0, 0);
                modalAnimationConfig.ctx.globalCompositeOperation = 'source-over';
            }}
            
            function updateModalProgress(percent) {{
                document.getElementById('modalProgressFill').style.width = percent + '%';
            }}
            
            // Store animation reference
            currentAnimation = {{
                start: startModalAnimation,
                reset: resetModalAnimation,
                stop: function() {{
                    if (modalAnimationConfig) {{
                        modalAnimationConfig.isAnimating = false;
                        if (modalAnimationConfig.animationFrame) {{
                            cancelAnimationFrame(modalAnimationConfig.animationFrame);
                        }}
                    }}
                }}
            }};

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
                    const button = document.createElement('div');
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

def create_auto_start_handwriting_html(text, pen_style="Realistic", writing_style="Natural", animation_speed=4.0, step_size=2):
    """
    Create HTML5 Canvas-based fluid handwriting animation with continuous path system
    
    Args:
        text (str): Text to animate
        pen_style (str): Style of pen rendering ("Realistic", "Simple", "Brush")
        writing_style (str): Writing characteristics ("Natural", "Formal", "Cursive")
        animation_speed (float): Animation speed multiplier
        step_size (int): Point sampling density in pixels (1-3 for smooth animation)
    
    Returns:
        str: Complete HTML content with fluid handwriting animation
    """
    
    import json
    
    # Escape text for JavaScript
    safe_text = json.dumps(text)
    
    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Fluid Handwriting Animation - Enhanced</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/opentype.js/1.3.4/opentype.min.js"></script>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;700&display=swap');
                
                body {{
                    margin: 0;
                    padding: 20px;
                    font-family: 'Noto Sans Ethiopic', 'Ebrima', 'Nyala', sans-serif;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 100vh;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                
                .container {{
                    max-width: 1200px;
                    width: 100%;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 15px 40px rgba(0,0,0,0.12);
                    padding: 40px;
                    margin: 20px;
                }}
                

                
                .text-display {{
                    font-size: 1.6em;
                    text-align: center;
                    margin: 20px 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #e8f4fd 0%, #f0f8ff 100%);
                    border-radius: 12px;
                    border: 2px solid rgba(102, 126, 234, 0.2);
                    color: #2c3e50;
                    font-weight: 500;
                }}
                
                .animation-area {{
                    position: relative;
                    background: #fefefe;
                    border: 2px solid #e1e8ed;
                    border-radius: 15px;
                    margin: 25px 0;
                    min-height: 350px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 15px;
                    box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
                }}
                
                .scroll-container {{
                    width: 100%;
                    max-width: 1000px;
                    max-height: 450px;
                    overflow: auto;
                    border-radius: 10px;
                    border: 1px solid #ddd;
                    background: white;
                    position: relative;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                
                #animationCanvas {{
                    display: block;
                    background: white;
                    border-radius: 8px;
                }}
                
                .progress-container {{
                    margin: 20px 0;
                }}
                
                .progress-bar {{
                    width: 100%;
                    height: 8px;
                    background: #ecf0f1;
                    border-radius: 4px;
                    overflow: hidden;
                    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
                }}
                
                .progress-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #667eea, #764ba2);
                    border-radius: 4px;
                    width: 0%;
                    transition: width 0.3s ease;
                    box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
                }}
                
                .status {{
                    text-align: center;
                    margin: 15px 0;
                    font-weight: 600;
                    font-size: 1.1em;
                    color: #2c3e50;
                }}

                .scroll-container::-webkit-scrollbar {{
                    width: 10px;
                    height: 10px;
                }}

                .scroll-container::-webkit-scrollbar-track {{
                    background: #f1f1f1;
                    border-radius: 5px;
                }}

                .scroll-container::-webkit-scrollbar-thumb {{
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    border-radius: 5px;
                }}

                .scroll-container::-webkit-scrollbar-thumb:hover {{
                    background: linear-gradient(135deg, #5a67d8, #6b46c1);
                }}
            </style>
        </head>
        <body>
            <div class="container">                
                <div class="text-display">
                    <strong>Animating:</strong> {text}
                </div>
                
                <div class="animation-area">
                    <div class="scroll-container" id="scrollContainer">
                        <canvas id="animationCanvas"></canvas>
                    </div>
                </div>
                
                <div class="progress-container">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <div class="status" id="status">Loading font and preparing animation...</div>
                </div>
            </div>

            <script>
                // Enhanced animation configuration with fluid path system
                const config = {{
                    text: {safe_text},
                    penStyle: "{pen_style}",
                    writingStyle: "{writing_style}",
                    animationSpeed: {animation_speed},
                    stepSize: {step_size},
                    
                    // Canvas elements
                    canvas: null,
                    ctx: null,
                    glyphCanvas: null,
                    glyphCtx: null,
                    maskCanvas: null,
                    maskCtx: null,
                    
                    // Animation state
                    isAnimating: false,
                    currentCharIndex: 0,
                    currentPointIndex: 0,
                    
                    // Font and layout
                    font: null,
                    fontSize: 120,
                    characters: [],
                    scrollContainer: null,
                    canvasWidth: 2400,
                    canvasHeight: 400,
                    
                    // Fluid path settings
                    revealMode: 'ink-mask',
                    nibRadius: 0,
                    inkColor: '#2c3e50',
                    
                    // Animation state
                    penX: 0,
                    penY: 0,
                    penPressure: 1.0,
                    penSpeed: 0,
                    animationFrame: null,
                    
                    // Performance tracking
                    lastFrameTime: 0,
                    frameCount: 0
                }};

                // Load font and initialize with auto-start
                opentype.load('https://fonts.gstatic.com/s/notosansethiopic/v49/7cHPv50vjIepfJVOZZgcpQ5B9FBTH9KGNfhSTgtoow1KVnIvyBoMSzUMacb-T35OK6Dj.ttf', function (err, font) {{
                    if (err) {{
                        console.error('Font loading error:', err);
                        document.getElementById('status').textContent = 'Error loading font. Using fallback - Starting animation...';
                        initWithoutFont();
                        // Auto-start even with fallback font after a short delay
                        setTimeout(startAnimation, 800);
                    }} else {{
                        config.font = font;
                        document.getElementById('status').textContent = 'Font loaded successfully - Starting animation...';
                        initCanvas();
                        prepareCharacterPaths();
                        // Auto-start animation after font loads and paths are prepared
                        setTimeout(startAnimation, 500);
                    }}
                }});
                
                // Initialize without font (fallback)
                function initWithoutFont() {{
                    config.font = null;
                    initCanvas();
                    prepareCharacterPaths();
                }}
                
                // Initialize canvas system
                function initCanvas() {{
                    config.canvas = document.getElementById('animationCanvas');
                    config.scrollContainer = document.getElementById('scrollContainer');
                    
                    // Calculate optimal canvas dimensions
                    const textLength = config.text.length;
                    const estimatedWidth = Math.max(900, textLength * 130);
                    config.canvasWidth = estimatedWidth;
                    config.canvas.width = config.canvasWidth;
                    config.canvas.height = config.canvasHeight;
                    config.ctx = config.canvas.getContext('2d');
                    
                    // Create offscreen canvases for compositing
                    config.glyphCanvas = document.createElement('canvas');
                    config.glyphCanvas.width = config.canvasWidth;
                    config.glyphCanvas.height = config.canvasHeight;
                    config.glyphCtx = config.glyphCanvas.getContext('2d');
                    
                    config.maskCanvas = document.createElement('canvas');
                    config.maskCanvas.width = config.canvasWidth;
                    config.maskCanvas.height = config.canvasHeight;
                    config.maskCtx = config.maskCanvas.getContext('2d');
                    
                    // Configure rendering contexts for quality
                    [config.ctx, config.glyphCtx, config.maskCtx].forEach(ctx => {{
                        ctx.imageSmoothingEnabled = true;
                        ctx.imageSmoothingQuality = 'high';
                        ctx.lineCap = 'round';
                        ctx.lineJoin = 'round';
                    }});
                    
                    // Calculate nib size based on font size
                    config.nibRadius = config.fontSize * 0.04;
                    
                    config.scrollContainer.scrollLeft = 0;
                }}

                // Prepare character paths using fluid continuous path system
 function prepareCharacterPaths() {{
                    const baseY = config.canvasHeight / 2 + config.fontSize / 4;
                    
                    // Calculate total text width to center it
                    let totalTextWidth = 0;
                    for (let i = 0; i < config.text.length; i++) {{
                        const char = config.text[i];
                        if (char === ' ') {{
                            const spaceWidth = config.font ? 
                                config.font.getAdvanceWidth(' ', config.fontSize) : 
                                config.fontSize * 0.3;
                            totalTextWidth += spaceWidth;
                        }} else {{
                            const charWidth = config.font ? 
                                config.font.getAdvanceWidth(char, config.fontSize) : 
                                config.fontSize * 0.6; // Reduced from 0.7 for better centering
                            totalTextWidth += charWidth;
                        }}
                    }}
                    
                    // Calculate centered starting X position with some padding
                    const padding = 50;
                    const availableWidth = config.canvasWidth - (2 * padding);
                    const startX = padding + (availableWidth - totalTextWidth) / 2;
                    let currentX = Math.max(padding, startX); // Ensure minimum padding
                    
                    config.characters = [];
                    
                    // Clear and prepare glyph canvas
                    config.glyphCtx.fillStyle = 'white';
                    config.glyphCtx.fillRect(0, 0, config.canvasWidth, config.canvasHeight);
                    
                    for (let i = 0; i < config.text.length; i++) {{
                        const char = config.text[i];
                        
                        if (char === ' ') {{
                            const spaceWidth = config.font ? 
                                config.font.getAdvanceWidth(' ', config.fontSize) : 
                                config.fontSize * 0.3;
                            currentX += spaceWidth;
                            config.characters.push({{
                                char: ' ',
                                type: 'space',
                                x: currentX,
                                y: baseY,
                                width: spaceWidth,
                                points: [] // No drawing points for spaces
                            }});
                            continue;
                        }}
                        
                        // Render glyph to offscreen canvas
                        if (config.font) {{
                            config.glyphCtx.font = `${{config.fontSize}}px 'Noto Sans Ethiopic'`;
                        }} else {{
                            config.glyphCtx.font = `${{config.fontSize}}px 'Noto Sans Ethiopic', serif`;
                        }}
                        config.glyphCtx.fillStyle = config.inkColor;
                        config.glyphCtx.fillText(char, currentX, baseY);
                        
                        // Generate continuous path for character
                        const continuousPath = generateContinuousPath(char, currentX, baseY);
                        
                        config.characters.push({{
                            char: char,
                            type: 'character',
                            x: currentX,
                            y: baseY,
                            points: continuousPath
                        }});
                        
                        // Advance to next character position
                        const charWidth = config.font ? 
                            config.font.getAdvanceWidth(char, config.fontSize) : 
                            config.fontSize * 0.7;
                        currentX += charWidth;
                    }}
                    
                    updateStatus(`Prepared ${{config.characters.length}} characters - Animation will start soon...`);
                }}

                // Generate continuous path for a character (CORE FLUID ALGORITHM)
                function generateContinuousPath(char, offsetX, offsetY) {{
                    if (!config.font) {{
                        // Fallback: simple path for when font is not available
                        return generateFallbackPath(char, offsetX, offsetY);
                    }}
                    
                    try {{
                        const fontPath = config.font.getPath(char, offsetX, offsetY, config.fontSize);
                        return convertToFluidPath(fontPath, offsetX, offsetY);
                    }} catch (error) {{
                        console.warn(`Error generating path for '${{char}}':`, error);
                        return generateFallbackPath(char, offsetX, offsetY);
                    }}
                }}

                // Convert OpenType path to fluid continuous path
                function convertToFluidPath(path, offsetX, offsetY) {{
                    const contours = extractPathContours(path);
                    if (contours.length === 0) return [];
                    
                    // Find optimal entry point (usually leftmost)
                    const entryPoint = findOptimalEntryPoint(contours);
                    
                    // Create continuous path by connecting contours intelligently
                    const fluidPath = createFluidContourPath(contours, entryPoint);
                    
                    // Resample path at fixed step size for smooth animation
                    return resamplePath(fluidPath, config.stepSize);
                }}

                // Extract contours from OpenType path commands
                function extractPathContours(path) {{
                    const contours = [];
                    let currentContour = [];
                    
                    for (const cmd of path.commands) {{
                        switch (cmd.type) {{
                            case 'M': // MoveTo
                                if (currentContour.length > 0) {{
                                    contours.push([...currentContour]);
                                }}
                                currentContour = [{{x: cmd.x, y: cmd.y}}];
                                break;
                                
                            case 'L': // LineTo
                                currentContour.push({{x: cmd.x, y: cmd.y}});
                                break;
                                
                            case 'Q': // Quadratic Bezier
                                const qStart = currentContour[currentContour.length - 1];
                                const qCurve = sampleQuadraticBezier(qStart, {{x: cmd.x1, y: cmd.y1}}, {{x: cmd.x, y: cmd.y}}, 0.1);
                                currentContour.push(...qCurve.slice(1)); // Skip first point (duplicate)
                                break;
                                
                            case 'C': // Cubic Bezier
                                const cStart = currentContour[currentContour.length - 1];
                                const cCurve = sampleCubicBezier(cStart, {{x: cmd.x1, y: cmd.y1}}, {{x: cmd.x2, y: cmd.y2}}, {{x: cmd.x, y: cmd.y}}, 0.1);
                                currentContour.push(...cCurve.slice(1)); // Skip first point (duplicate)
                                break;
                                
                            case 'Z': // ClosePath
                                if (currentContour.length > 0) {{
                                    contours.push([...currentContour]);
                                    currentContour = [];
                                }}
                                break;
                        }}
                    }}
                    
                    if (currentContour.length > 0) {{
                        contours.push(currentContour);
                    }}
                    
                    return contours;
                }}

                // Sample quadratic Bezier curve
                function sampleQuadraticBezier(p0, p1, p2, step) {{
                    const points = [];
                    for (let t = 0; t <= 1; t += step) {{
                        const x = Math.pow(1-t, 2) * p0.x + 2*(1-t)*t * p1.x + Math.pow(t, 2) * p2.x;
                        const y = Math.pow(1-t, 2) * p0.y + 2*(1-t)*t * p1.y + Math.pow(t, 2) * p2.y;
                        points.push({{x, y}});
                    }}
                    return points;
                }}

                // Sample cubic Bezier curve
                function sampleCubicBezier(p0, p1, p2, p3, step) {{
                    const points = [];
                    for (let t = 0; t <= 1; t += step) {{
                        const x = Math.pow(1-t, 3) * p0.x + 3 * Math.pow(1-t, 2) * t * p1.x + 
                                3 * (1-t) * Math.pow(t, 2) * p2.x + Math.pow(t, 3) * p3.x;
                        const y = Math.pow(1-t, 3) * p0.y + 3 * Math.pow(1-t, 2) * t * p1.y + 
                                3 * (1-t) * Math.pow(t, 2) * p2.y + Math.pow(t, 3) * p3.y;
                        points.push({{x, y}});
                    }}
                    return points;
                }}

                // Find optimal entry point for writing
                function findOptimalEntryPoint(contours) {{
                    if (contours.length === 0) return null;
                    
                    let leftmostPoint = null;
                    let minX = Infinity;
                    
                    contours.forEach((contour, contourIndex) => {{
                        contour.forEach((point, pointIndex) => {{
                            if (point.x < minX) {{
                                minX = point.x;
                                leftmostPoint = {{contourIndex, pointIndex, point}};
                            }}
                        }});
                    }});
                    
                    return leftmostPoint;
                }}

                // Create fluid path by intelligently connecting contours
                function createFluidContourPath(contours, entryPoint) {{
                    if (!entryPoint || contours.length === 0) return [];
                    
                    const fluidPath = [];
                    const processedContours = new Set();
                    
                    // Start with entry contour
                    const startContour = contours[entryPoint.contourIndex];
                    const reorderedStartContour = reorderContourFromPoint(startContour, entryPoint.pointIndex);
                    fluidPath.push(...reorderedStartContour);
                    processedContours.add(entryPoint.contourIndex);
                    
                    // Connect remaining contours using shortest path
                    while (processedContours.size < contours.length) {{
                        const lastPoint = fluidPath[fluidPath.length - 1];
                        let nearestContour = null;
                        let nearestDistance = Infinity;
                        let nearestStartIndex = 0;
                        
                        contours.forEach((contour, index) => {{
                            if (processedContours.has(index)) return;
                            
                            contour.forEach((point, pointIndex) => {{
                                const distance = Math.sqrt(
                                    Math.pow(point.x - lastPoint.x, 2) + 
                                    Math.pow(point.y - lastPoint.y, 2)
                                );
                                if (distance < nearestDistance) {{
                                    nearestDistance = distance;
                                    nearestContour = index;
                                    nearestStartIndex = pointIndex;
                                }}
                            }});
                        }});
                        
                        if (nearestContour !== null) {{
                            // Add connecting line if distance is significant
                            if (nearestDistance > config.stepSize * 2) {{
                                const connectPoint = contours[nearestContour][nearestStartIndex];
                                fluidPath.push(...interpolatePoints(lastPoint, connectPoint, config.stepSize));
                            }}
                            
                            // Add reordered contour
                            const nextContour = reorderContourFromPoint(contours[nearestContour], nearestStartIndex);
                            fluidPath.push(...nextContour);
                            processedContours.add(nearestContour);
                        }} else {{
                            break; // Safety break
                        }}
                    }}
                    
                    return fluidPath;
                }}

                // Reorder contour points starting from specific index
                function reorderContourFromPoint(contour, startIndex) {{
                    if (startIndex === 0) return [...contour];
                    return [...contour.slice(startIndex), ...contour.slice(0, startIndex)];
                }}

                // Interpolate points between two locations
                function interpolatePoints(start, end, stepSize) {{
                    const points = [];
                    const distance = Math.sqrt(Math.pow(end.x - start.x, 2) + Math.pow(end.y - start.y, 2));
                    const steps = Math.ceil(distance / stepSize);
                    
                    for (let i = 1; i <= steps; i++) {{
                        const t = i / steps;
                        points.push({{
                            x: start.x + (end.x - start.x) * t,
                            y: start.y + (end.y - start.y) * t
                        }});
                    }}
                    
                    return points;
                }}

                // Resample path at fixed step size
                function resamplePath(path, stepSize) {{
                    if (path.length < 2) return path;
                    
                    const resampled = [path[0]];
                    let currentDistance = 0;
                    
                    for (let i = 1; i < path.length; i++) {{
                        const prev = path[i - 1];
                        const curr = path[i];
                        const segmentLength = Math.sqrt(
                            Math.pow(curr.x - prev.x, 2) + Math.pow(curr.y - prev.y, 2)
                        );
                        
                        currentDistance += segmentLength;
                        
                        while (currentDistance >= stepSize) {{
                            const t = (stepSize - (currentDistance - segmentLength)) / segmentLength;
                            const interpolated = {{
                                x: prev.x + (curr.x - prev.x) * t,
                                y: prev.y + (curr.y - prev.y) * t
                            }};
                            resampled.push(interpolated);
                            currentDistance -= stepSize;
                        }}
                    }}
                    
                    // Always include the last point
                    if (path.length > 0) {{
                        resampled.push(path[path.length - 1]);
                    }}
                    
                    return resampled;
                }}

                // Generate fallback path when font is not available
                function generateFallbackPath(char, offsetX, offsetY) {{
                    const charWidth = config.fontSize * 0.6;
                    const charHeight = config.fontSize * 0.8;
                    
                    // Simple rectangular path as fallback
                    return [
                        {{x: offsetX, y: offsetY - charHeight * 0.7}},
                        {{x: offsetX + charWidth, y: offsetY - charHeight * 0.7}},
                        {{x: offsetX + charWidth, y: offsetY}},
                        {{x: offsetX, y: offsetY}},
                        {{x: offsetX, y: offsetY - charHeight * 0.7}}
                    ];
                }}

                // Enhanced nib painting with pressure variation
                function paintNib(x, y, pressure = 1.0) {{
                    config.maskCtx.save();
                    config.maskCtx.translate(x, y);
                    
                    const radius = config.nibRadius * pressure;
                    
                    if (config.penStyle === "Brush") {{
                        // Brush-like nib with texture
                        const gradient = config.maskCtx.createRadialGradient(0, 0, 0, 0, 0, radius);
                        gradient.addColorStop(0, 'black');
                        gradient.addColorStop(0.7, 'rgba(0,0,0,0.8)');
                        gradient.addColorStop(1, 'rgba(0,0,0,0.3)');
                        config.maskCtx.fillStyle = gradient;
                    }} else {{
                        config.maskCtx.fillStyle = 'black';
                    }}
                    
                    config.maskCtx.beginPath();
                    config.maskCtx.arc(0, 0, radius, 0, Math.PI * 2);
                    config.maskCtx.fill();
                    
                    config.maskCtx.restore();
                }}

                // Enhanced pen rendering
                function drawPen(x, y, angle = 0, pressure = 1.0) {{
                    const ctx = config.ctx;
                    ctx.save();
                    ctx.translate(x, y);
                    ctx.rotate(angle);
                    
                    const scale = 0.8 + pressure * 0.4; // Pen size varies with pressure
                    ctx.scale(scale, scale);
                    
                    // Pen shadow
                    ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
                    ctx.fillRect(-4, 4, 8, 35);
                    
                    // Pen body gradient
                    const gradient = ctx.createLinearGradient(0, 0, 0, 30);
                    gradient.addColorStop(0, '#4169E1');
                    gradient.addColorStop(0.5, '#6495ED');
                    gradient.addColorStop(1, '#1E3A8A');
                    ctx.fillStyle = gradient;
                    ctx.fillRect(-3.5, 0, 7, 30);
                    
                    // Pen grip
                    ctx.fillStyle = '#696969';
                    ctx.fillRect(-4, 10, 8, 10);
                    
                    // Pen tip
                    ctx.fillStyle = '#000080';
                    ctx.beginPath();
                    ctx.arc(0, -2, 2.5, 0, Math.PI * 2);
                    ctx.fill();
                    
                    // Highlight
                    ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
                    ctx.fillRect(-1, 2, 2, 15);
                    
                    ctx.restore();
                }}

                // Auto-scroll to follow pen movement
                function scrollToPosition(x) {{
                    if (!config.scrollContainer) return;
                    
                    const containerWidth = config.scrollContainer.clientWidth;
                    const scrollLeft = config.scrollContainer.scrollLeft;
                    const scrollRight = scrollLeft + containerWidth;
                    const padding = 120;
                    
                    if (x < scrollLeft + padding) {{
                        config.scrollContainer.scrollLeft = Math.max(0, x - padding);
                    }} else if (x > scrollRight - padding) {{
                        config.scrollContainer.scrollLeft = x - containerWidth + padding;
                    }}
                }}

                // Composite frame using mask system
                function compositeFrame() {{
                    const ctx = config.ctx;
                    
                    // Clear main canvas
                    ctx.clearRect(0, 0, config.canvas.width, config.canvas.height);
                    
                    // Draw paper background
                    ctx.fillStyle = 'white';
                    ctx.fillRect(0, 0, config.canvas.width, config.canvas.height);
                    
                    // Draw filled glyph layer
                    ctx.drawImage(config.glyphCanvas, 0, 0);
                    
                    // Apply ink mask (reveal only where ink has been painted)
                    ctx.globalCompositeOperation = 'destination-in';
                    ctx.drawImage(config.maskCanvas, 0, 0);
                    ctx.globalCompositeOperation = 'source-over';
                    
                    // Draw pen at current position
                    if (config.isAnimating) {{
                        drawPen(config.penX, config.penY - 40, 0, config.penPressure);
                    }}
                }}

                // Calculate pen pressure based on speed and position
                function calculatePenPressure(speed, pointIndex, totalPoints) {{
                    // Base pressure
                    let pressure = 1.0;
                    
                    // Vary pressure based on speed (slower = more pressure)
                    if (speed > 0) {{
                        pressure *= Math.max(0.5, 2.0 - speed / 10);
                    }}
                    
                    // Slight pressure variation at start and end of strokes
                    const progress = pointIndex / totalPoints;
                    if (progress < 0.1) {{
                        pressure *= 0.7 + progress * 3; // Fade in
                    }} else if (progress > 0.9) {{
                        pressure *= 0.7 + (1 - progress) * 3; // Fade out
                    }}
                    
                    // Add subtle random variation
                    pressure *= 0.9 + Math.random() * 0.2;
                    
                    return Math.max(0.3, Math.min(1.5, pressure));
                }}

                // Control function - simplified for auto-start
                function startAnimation() {{
                    if (config.isAnimating) return;
                    
                    resetAnimationState();
                    config.isAnimating = true;
                    
                    // Clear mask canvas
                    config.maskCtx.clearRect(0, 0, config.canvasWidth, config.canvasHeight);
                    
                    updateStatus('Animation starting...');
                    
                    // Start animation loop
                    config.lastFrameTime = performance.now();
                    animateNextFrame();
                }}

                function resetAnimationState() {{
                    config.currentCharIndex = 0;
                    config.currentPointIndex = 0;
                    config.penX = 0;
                    config.penY = 0;
                    config.penPressure = 1.0;
                    config.penSpeed = 0;
                    config.frameCount = 0;
                }}

                // Main animation loop with enhanced fluid movement
                function animateNextFrame() {{
                    if (!config.isAnimating) return;
                    
                    const currentTime = performance.now();
                    const deltaTime = currentTime - config.lastFrameTime;
                    config.lastFrameTime = currentTime;
                    config.frameCount++;
                    
                    // Check if animation is complete
                    if (config.currentCharIndex >= config.characters.length) {{
                        completeAnimation();
                        return;
                    }}
                    
                    const character = config.characters[config.currentCharIndex];
                    
                    // Update progress
                    const totalPoints = config.characters.reduce((sum, char) => sum + char.points.length, 0);
                    const currentPoints = config.characters.slice(0, config.currentCharIndex).reduce((sum, char) => sum + char.points.length, 0) + config.currentPointIndex;
                    const progress = totalPoints > 0 ? (currentPoints / totalPoints) * 100 : 0;
                    document.getElementById('progressFill').style.width = progress + '%';
                    
                    if (character.type === 'space') {{
                        // Handle space - quick movement without drawing
                        config.penX = character.x;
                        config.penY = character.y;
                        scrollToPosition(config.penX);
                        compositeFrame();
                        
                        setTimeout(() => {{
                            config.currentCharIndex++;
                            config.currentPointIndex = 0;
                            config.animationFrame = requestAnimationFrame(animateNextFrame);
                        }}, 200 / config.animationSpeed);
                        return;
                    }}
                    
                    // Handle character with continuous path
                    if (config.currentPointIndex >= character.points.length) {{
                        // Move to next character
                        config.currentCharIndex++;
                        config.currentPointIndex = 0;
                        setTimeout(() => {{
                            config.animationFrame = requestAnimationFrame(animateNextFrame);
                        }}, 100 / config.animationSpeed);
                        return;
                    }}
                    
                    // Get current point
                    const point = character.points[config.currentPointIndex];
                    if (!point) {{
                        config.currentPointIndex++;
                        config.animationFrame = requestAnimationFrame(animateNextFrame);
                        return;
                    }}
                    
                    // Calculate pen speed for pressure variation
                    if (config.currentPointIndex > 0) {{
                        const prevPoint = character.points[config.currentPointIndex - 1];
                        config.penSpeed = Math.sqrt(
                            Math.pow(point.x - prevPoint.x, 2) + 
                            Math.pow(point.y - prevPoint.y, 2)
                        );
                    }}
                    
                    // Update pen position and pressure
                    config.penX = point.x;
                    config.penY = point.y;
                    config.penPressure = calculatePenPressure(config.penSpeed, config.currentPointIndex, character.points.length);
                    
                    // Paint ink at current position
                    paintNib(config.penX, config.penY, config.penPressure);
                    
                    // Render frame
                    compositeFrame();
                    scrollToPosition(config.penX);
                    
                    config.currentPointIndex++;
                    
                    // Schedule next frame with dynamic timing
                    const baseDelay = 20; // Base delay in ms
                    const speedAdjustedDelay = Math.max(5, baseDelay / config.animationSpeed);
                    
                    setTimeout(() => {{
                        config.animationFrame = requestAnimationFrame(animateNextFrame);
                    }}, speedAdjustedDelay);
                }}

                function completeAnimation() {{
                    config.isAnimating = false;
                    
                    // Update UI
                    document.getElementById('progressFill').style.width = '100%';
                    
                    updateStatus(`Animation complete! (${{config.frameCount}} frames rendered)`);
                    
                    // Final render without pen
                    config.ctx.clearRect(0, 0, config.canvas.width, config.canvas.height);
                    config.ctx.fillStyle = 'white';
                    config.ctx.fillRect(0, 0, config.canvas.width, config.canvas.height);
                    config.ctx.drawImage(config.glyphCanvas, 0, 0);
                    config.ctx.globalCompositeOperation = 'destination-in';
                    ctx.drawImage(config.maskCanvas, 0, 0);
                    ctx.globalCompositeOperation = 'source-over';
                }}

                function updateStatus(message) {{
                    document.getElementById('status').textContent = message;
                }}
            </script>
        </body>
        </html>
    """
    return html_content


def get_all_characters(alphabet_structure):
    """Extract all characters from alphabet structure for selection"""
    all_chars = []
    for column_key in alphabet_structure:
        for family in alphabet_structure[column_key]:
            for char_obj in family["characters"]:
                char = char_obj["char"]
                sound = char_obj["sound"]
                family_name = family["familyName"]
                # Create display label
                label = f"{char} ({sound}) - {family_name}"
                all_chars.append((char, label))
    # Remove duplicates and sort
    unique_chars = {}
    for char, label in all_chars:
        if char not in unique_chars:
            unique_chars[char] = label
    return [(char, unique_chars[char]) for char in sorted(unique_chars.keys())]


def render():
    """Render the traditional three-column Tigrinya alphabet layout with integrated modal"""
    
    # Page header
    st.markdown(
        """
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='color: #2c3e50; font-size: 3em; margin-bottom: 10px;'>ፊደላት</h1>
            <h2 style='color: #34495e; font-size: 1.8em; margin-bottom: 20px;'>Traditional Tigrinya Alphabet</h2>
            <p style='color: #7f8c8d; font-size: 1.2em;'>✨ Click any character to see its handwriting animation in a beautiful modal ✨</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Get alphabet structure
    alphabet_structure = create_traditional_alphabet_structure()
    
    # Create the interactive alphabet grid with integrated modal
    alphabet_grid_html = create_alphabet_grid_html(alphabet_structure)
    
    # Display component - everything happens in the iframe now!
    components.html(
        alphabet_grid_html, 
        height=3200,
        scrolling=True
    )
    
    # Simple info section
    st.markdown("---")
    st.info("💡 **Tip:** Click any character in the grid above to see its handwriting animation. The animation appears in a modal overlay with smooth pen movement!")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Tigrinya Alphabet Learning")
    render()
    render()