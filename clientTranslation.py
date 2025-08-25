# ============================================================
# Full Geʽez Transliterator: Latin ↔ Geʽez
# Vowel system: e=0, E=4
# Consonant keys: H, K, A, C
# ============================================================


import re
import gradio as gr
from typing import Dict, Tuple

# ============================
# Full Feedel Rows (updated keys)
# ============================
feedel_rows = {
    'h':  ("ሀ","ሁ","ሂ","ሃ","ሄ","ህ","ሆ"),   # h
    'H':  ("ሐ","ሑ","ሒ","ሓ","ሔ","ሕ","ሖ"),   # H (was ḥ)
    'x':  ("ኀ","ኁ","ኂ","ኃ","ኄ","ኅ","ኆ"),   # x
    'K':  ("ኸ","ኹ","ኺ","ኻ","ኼ","ኽ","ኾ"),   # K (was ḫ)
    'k':  ("ከ","ኩ","ኪ","ካ","ኬ","ክ","ኮ"),   # k
    'A':  ("ዐ","ዑ","ዒ","ዓ","ዔ","ዕ","ዖ"),   # A (was ʿ)
    'l':  ("ለ","ሉ","ሊ","ላ","ሌ","ል","ሎ"),
    'm':  ("መ","ሙ","ሚ","ማ","ሜ","ም","ሞ"),
    'r':  ("ረ","ሩ","ሪ","ራ","ሬ","ር","ሮ"),
    's':  ("ሰ","ሱ","ሲ","ሳ","ሴ","ስ","ሶ"),
    'š':  ("ሸ","ሹ","ሺ","ሻ","ሼ","ሽ","ሾ"),   # sh
    'q':  ("ቀ","ቁ","ቂ","ቃ","ቄ","ቅ","ቆ"),
    'b':  ("በ","ቡ","ቢ","ባ","ቤ","ብ","ቦ"),
    't':  ("ተ","ቱ","ቲ","ታ","ቴ","ት","ቶ"),
    'ṭ':  ("ጠ","ጡ","ጢ","ጣ","ጤ","ጥ","ጦ"), # emphatic t
    'C':  ("ቸ","ቹ","ቺ","ቻ","ቼ","ች","ቾ"), # C (was č)
    'č̣': ("ጨ","ጩ","ጪ","ጫ","ጬ","ጭ","ጮ"), # emphatic ch
    'p':  ("ፐ","ፑ","ፒ","ፓ","ፔ","ፕ","ፖ"),
    'p̣': ("ጰ","ጱ","ጲ","ጳ","ጴ","ጵ","ጶ"), # emphatic p
    'g':  ("ገ","ጉ","ጊ","ጋ","ጌ","ግ","ጎ"),
    'd':  ("ደ","ዱ","ዲ","ዳ","ዴ","ድ","ዶ"),
    'f':  ("ፈ","ፉ","ፊ","ፋ","ፌ","ፍ","ፎ"),
    'z':  ("ዘ","ዙ","ዚ","ዛ","ዜ","ዝ","ዞ"),
    'ž':  ("ዠ","ዡ","ዢ","ዣ","ዤ","ዥ","ዦ"), # zh
    'y':  ("የ","ዩ","ዪ","ያ","ዬ","ይ","ዮ"),
    'w':  ("ወ","ዉ","ዊ","ዋ","ዌ","ው","ዎ"),
    'n':  ("ነ","ኑ","ኒ","ና","ኔ","ን","ኖ"),
    'ñ':  ("ኘ","ኙ","ኚ","ኛ","ኜ","ኝ","ኞ"), # nya
    'ṣ':  ("ፀ","ፁ","ፂ","ፃ","ፄ","ፅ","ፆ"), # ṣ
    'j':  ("ጀ","ጁ","ጂ","ጃ","ጄ","ጅ","ጆ"),
}

alef_row = ("አ","ኡ","ኢ","ኣ","ኤ","እ","ኦ")

# ============================
# Updated Vowel Mapping
# ============================
# Now: 0=e, 4=E
vowel_to_index = {"e":0,"u":1,"i":2,"a":3,"E":4,"":5,"ə":5,"o":6}

# Reverse mapping for Geʽez → Latin
geez_char_to_cv: Dict[str, Tuple[str,str]] = {}
for cons, row in feedel_rows.items():
    geez_char_to_cv.update({row[i]:(cons,v) for i,v in enumerate(["e","u","i","a","E","","o"])})
geez_char_to_cv.update({
    alef_row[0]:("", "e"), alef_row[1]:("", "u"), alef_row[2]:("", "i"),
    alef_row[3]:("", "a"), alef_row[4]:("", "E"), alef_row[5]:("", ""),
    alef_row[6]:("", "o")
})

# Digraphs for phonetic typing
digraphs = ["sh","ch","ts","kha","ha","xa"]

# Phonetic mapping: plain Latin → consonant key
phonetic_map = {"kha":"K","ha":"H","xa":"x"}

# ============================
# Conversion Functions
# ============================

def latin_to_geez_syllable(text: str) -> str:
    """Convert Latin transliteration to Geʽez (syllable-based)"""
    text = text.strip()
    result = ""
    i = 0
    while i < len(text):
        match = None
        # Check for digraphs like "sh"
        for dg in sorted(digraphs, key=len, reverse=True):
            if text.startswith(dg, i):
                cons = phonetic_map.get(dg, dg[0])
                match = cons
                i += len(dg)
                break
        if not match:
            ch = text[i]
            match = ch
            i += 1
        # Vowel
        v = ""
        if i < len(text) and text[i] in ['e','u','i','a','E','o']:
            v = text[i]
            i += 1
        # Map to Geʽez
        if match in feedel_rows:
            idx = vowel_to_index.get(v,"")
            result += feedel_rows[match][idx]
        elif v:  # If vowel only
            if v == "e": result += alef_row[0]
            elif v == "u": result += alef_row[1]
            elif v == "i": result += alef_row[2]
            elif v == "a": result += alef_row[3]
            elif v == "E": result += alef_row[4]
            elif v == "o": result += alef_row[6]
        else:
            result += match
    return result

def geez_to_latin_syllable(text: str) -> str:
    """Convert Geʽez to Latin transliteration (syllable-based)"""
    result = ""
    for ch in text:
        if ch in geez_char_to_cv:
            cons,v = geez_char_to_cv[ch]
            result += cons+v
        else:
            result += ch
    return result

def latin_to_geez_letter(text: str) -> str:
    """Letter-by-letter mapping (basic Latin to Geʽez)"""
    mapping = {
        'h': 'ሀ','H': 'ሐ','k': 'ከ','K': 'ኸ','x': 'ኀ','A': 'ዐ','l': 'ለ','m': 'መ',
        'r': 'ረ','s': 'ሰ','S': 'ሠ','C': 'ቸ','t': 'ተ','T': 'ጠ','b': 'በ','B': 'ቨ',
        'g': 'ገ','d': 'ደ','f': 'ፈ','p': 'ፐ','n': 'ነ','z': 'ዘ','Z': 'ዠ','y': 'የ',
        'w': 'ወ','j': 'ጀ'
    }
    return ''.join(mapping.get(ch,ch) for ch in text)

def geez_to_latin_letter(text: str) -> str:
    """Letter-by-letter reverse mapping"""
    reverse_map = {v:k for k,v in {
        'h': 'ሀ','H': 'ሐ','k': 'ከ','K': 'ኸ','x': 'ኀ','A': 'ዐ','l': 'ለ','m': 'መ',
        'r': 'ረ','s': 'ሰ','S': 'ሠ','C': 'ቸ','t': 'ተ','T': 'ጠ','b': 'በ','B': 'ቨ',
        'g': 'ገ','d': 'ደ','f': 'ፈ','p': 'ፐ','n': 'ነ','z': 'ዘ','Z': 'ዠ','y': 'የ',
        'w': 'ወ','j': 'ጀ'
    }.items()}
    return ''.join(reverse_map.get(ch,ch) for ch in text)

# ============================
# Gradio UI
# ============================
def transliterate(text, mode, direction):
    if mode == "Syllable-based":
        return latin_to_geez_syllable(text) if direction=="Latin→Geʽez" else geez_to_latin_syllable(text)
    else:
        return latin_to_geez_letter(text) if direction=="Latin→Geʽez" else geez_to_latin_letter(text)

if __name__ == "__main__":
    with gr.Blocks() as demo:
        gr.Markdown("## Geʽez ↔ Latin Transliterator (Syllable or Letter Mode)")
        text = gr.Textbox(label="Input")
        mode = gr.Radio(["Syllable-based","Letter-based"], value="Syllable-based", label="Mode")
        direction = gr.Radio(["Latin→Geʽez","Geʽez→Latin"], value="Latin→Geʽez", label="Direction")
        out = gr.Textbox(label="Output")
        btn = gr.Button("Convert")
        btn.click(fn=transliterate, inputs=[text,mode,direction], outputs=out)

    demo.launch()