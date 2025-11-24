# ============================================================
# Full Geʽez Transliterator: Latin ↔ Geʽez
# Vowel system: e=0, ə=5, E=4
# Fixed phonetic mapping for proper transliteration
# ============================================================
# CLIENT TRANSLATION V2


import re
from typing import Dict, Tuple

import gradio as gr

# ============================
# Full Feedel Rows (corrected)
# ============================
feedel_rows = {
    "h": ("ሀ", "ሁ", "ሂ", "ሃ", "ሄ", "ህ", "ሆ"),  # h
    "ḥ": ("ሐ", "ሑ", "ሒ", "ሓ", "ሔ", "ሕ", "ሖ"),  # ḥ (pharyngeal h)
    "x": ("ኀ", "ኁ", "ኂ", "ኃ", "ኄ", "ኅ", "ኆ"),  # x (kha)
    "ḫ": ("ኸ", "ኹ", "ኺ", "ኻ", "ኼ", "ኽ", "ኾ"),  # ḫ (velar fricative)
    "k": ("ከ", "ኩ", "ኪ", "ካ", "ኬ", "ክ", "ኮ"),  # k
    "ʿ": ("ዐ", "ዑ", "ዒ", "ዓ", "ዔ", "ዕ", "ዖ"),  # ʿ (ayn)
    "l": ("ለ", "ሉ", "ሊ", "ላ", "ሌ", "ል", "ሎ"),
    "m": ("መ", "ሙ", "ሚ", "ማ", "ሜ", "ም", "ሞ"),
    "r": ("ረ", "ሩ", "ሪ", "ራ", "ሬ", "ር", "ሮ"),
    "s": ("ሰ", "ሱ", "ሲ", "ሳ", "ሴ", "ስ", "ሶ"),
    "š": ("ሸ", "ሹ", "ሺ", "ሻ", "ሼ", "ሽ", "ሾ"),  # sh
    "q": ("ቀ", "ቁ", "ቂ", "ቃ", "ቄ", "ቅ", "ቆ"),
    "b": ("በ", "ቡ", "ቢ", "ባ", "ቤ", "ብ", "ቦ"),
    "t": ("ተ", "ቱ", "ቲ", "ታ", "ቴ", "ት", "ቶ"),
    "ṭ": ("ጠ", "ጡ", "ጢ", "ጣ", "ጤ", "ጥ", "ጦ"),  # emphatic t
    "č": ("ቸ", "ቹ", "ቺ", "ቻ", "ቼ", "ች", "ቾ"),  # ch
    "č̣": ("ጨ", "ጩ", "ጪ", "ጫ", "ጬ", "ጭ", "ጮ"),  # emphatic ch
    "p": ("ፐ", "ፑ", "ፒ", "ፓ", "ፔ", "ፕ", "ፖ"),
    "p̣": ("ጰ", "ጱ", "ጲ", "ጳ", "ጴ", "ጵ", "ጶ"),  # emphatic p
    "g": ("ገ", "ጉ", "ጊ", "ጋ", "ጌ", "ግ", "ጎ"),
    "d": ("ደ", "ዱ", "ዲ", "ዳ", "ዴ", "ድ", "ዶ"),
    "f": ("ፈ", "ፉ", "ፊ", "ፋ", "ፌ", "ፍ", "ፎ"),
    "z": ("ዘ", "ዙ", "ዚ", "ዛ", "ዜ", "ዝ", "ዞ"),
    "ž": ("ዠ", "ዡ", "ዢ", "ዣ", "ዤ", "ዥ", "ዦ"),  # zh
    "y": ("የ", "ዩ", "ዪ", "ያ", "ዬ", "ይ", "ዮ"),
    "w": ("ወ", "ዉ", "ዊ", "ዋ", "ዌ", "ው", "ዎ"),
    "n": ("ነ", "ኑ", "ኒ", "ና", "ኔ", "ን", "ኖ"),
    "ñ": ("ኘ", "ኙ", "ኚ", "ኛ", "ኜ", "ኝ", "ኞ"),  # nya
    "ṣ": ("ፀ", "ፁ", "ፂ", "ፃ", "ፄ", "ፅ", "ፆ"),  # ṣ (emphatic s)
    "j": ("ጀ", "ጁ", "ጂ", "ጃ", "ጄ", "ጅ", "ጆ"),
}

alef_row = ("አ", "ኡ", "ኢ", "ኣ", "ኤ", "እ", "ኦ")

# ============================
# Vowel Mapping (corrected)
# ============================
# Standard: e=0, u=1, i=2, a=3, ē=4, ə=5, o=6
vowel_to_index = {"e": 0, "u": 1, "i": 2, "a": 3, "ē": 4, "ə": 5, "": 5, "o": 6}

# Alternative input keys for convenience
alt_vowel_keys = {"E": "ē"}  # Allow E as input for ē

# Reverse mapping for Geʽez → Latin
geez_char_to_cv: Dict[str, Tuple[str, str]] = {}
for cons, row in feedel_rows.items():
    geez_char_to_cv.update(
        {row[i]: (cons, v) for i, v in enumerate(["e", "u", "i", "a", "ē", "ə", "o"])}
    )

# Add alef row mappings
geez_char_to_cv.update(
    {
        alef_row[0]: ("", "a"),  # አ = a (not e)
        alef_row[1]: ("", "u"),  # ኡ = u
        alef_row[2]: ("", "i"),  # ኢ = i
        alef_row[3]: ("", "ā"),  # ኣ = ā (long a)
        alef_row[4]: ("", "ē"),  # ኤ = ē (long e)
        alef_row[5]: ("", "ə"),  # እ = ə (schwa)
        alef_row[6]: ("", "o"),  # ኦ = o
    }
)

# Digraphs and phonetic mappings for easier input
phonetic_replacements = [
    ("ch", "č"),
    ("sh", "š"),
    ("kh", "x"),
    ("zh", "ž"),
    ("ny", "ñ"),
    ("ts", "ṣ"),
    ("ayn", "ʿ"),
    ("H", "ḥ"),  # Capital H for pharyngeal h
    ("K", "ḫ"),  # Capital K for velar fricative
    ("T", "ṭ"),  # Capital T for emphatic t
    ("S", "ṣ"),  # Capital S for emphatic s
    ("A", "ʿ"),  # Capital A for ayn (alternative)
]

# ============================
# Conversion Functions
# ============================


def preprocess_latin(text: str) -> str:
    """Apply phonetic replacements for easier input"""
    for old, new in phonetic_replacements:
        text = text.replace(old, new)

    # Handle alternative vowel keys
    for alt, std in alt_vowel_keys.items():
        text = text.replace(alt, std)

    return text


def latin_to_geez_syllable(text: str) -> str:
    """Convert Latin transliteration to Geʽez (syllable-based)"""
    text = preprocess_latin(text.strip())
    result = ""
    i = 0

    while i < len(text):
        # Find consonant
        cons = ""
        if i < len(text):
            ch = text[i]
            # Check for special characters first
            if ch in ["ḥ", "ḫ", "ʿ", "š", "ṭ", "č", "p̣", "č̣", "ž", "ñ", "ṣ"]:
                cons = ch
                i += 1
            elif ch in feedel_rows:
                cons = ch
                i += 1
            elif ch.isalpha():
                cons = ch
                i += 1
            else:
                result += ch
                i += 1
                continue

        # Find vowel
        vowel = "ə"  # default to schwa (6th form)
        if i < len(text) and text[i] in vowel_to_index:
            vowel = text[i]
            i += 1

        # Convert to Geʽez
        if cons in feedel_rows:
            idx = vowel_to_index.get(vowel, 5)
            result += feedel_rows[cons][idx]
        elif cons == "" and vowel in vowel_to_index:
            # Vowel-only syllable
            idx = vowel_to_index[vowel]
            result += alef_row[idx] if idx < len(alef_row) else vowel
        else:
            result += cons + vowel if vowel != "ə" else cons

    return result


def geez_to_latin_syllable(text: str) -> str:
    """Convert Geʽez to Latin transliteration (syllable-based)"""
    result = ""

    for ch in text:
        if ch in geez_char_to_cv:
            cons, vowel = geez_char_to_cv[ch]
            if vowel == "ə":  # Don't show schwa explicitly
                result += cons
            else:
                result += cons + vowel
        else:
            result += ch

    return result


def latin_to_geez_letter(text: str) -> str:
    """Letter-by-letter mapping (basic Latin to Geʽez)"""
    text = preprocess_latin(text)
    mapping = {
        "h": "ሀ",
        "ḥ": "ሐ",
        "k": "ከ",
        "ḫ": "ኸ",
        "x": "ኀ",
        "ʿ": "ዐ",
        "l": "ለ",
        "m": "መ",
        "r": "ረ",
        "s": "ሰ",
        "š": "ሸ",
        "č": "ቸ",
        "t": "ተ",
        "ṭ": "ጠ",
        "b": "በ",
        "g": "ገ",
        "d": "ደ",
        "f": "ፈ",
        "p": "ፐ",
        "n": "ነ",
        "z": "ዘ",
        "ž": "ዠ",
        "y": "የ",
        "w": "ወ",
        "j": "ጀ",
        "q": "ቀ",
        "ñ": "ኘ",
        "ṣ": "ፀ",
        "č̣": "ጨ",
        "p̣": "ጰ",
    }
    return "".join(mapping.get(ch, ch) for ch in text)


def geez_to_latin_letter(text: str) -> str:
    """Letter-by-letter reverse mapping"""
    reverse_map = {
        "ሀ": "h",
        "ሐ": "ḥ",
        "ከ": "k",
        "ኸ": "ḫ",
        "ኀ": "x",
        "ዐ": "ʿ",
        "ለ": "l",
        "መ": "m",
        "ረ": "r",
        "ሰ": "s",
        "ሸ": "š",
        "ቸ": "č",
        "ተ": "t",
        "ጠ": "ṭ",
        "በ": "b",
        "ገ": "g",
        "ደ": "d",
        "ፈ": "f",
        "ፐ": "p",
        "ነ": "n",
        "ዘ": "z",
        "ዠ": "ž",
        "የ": "y",
        "ወ": "w",
        "ጀ": "j",
        "ቀ": "q",
        "ኘ": "ñ",
        "ፀ": "ṣ",
        "ጨ": "č̣",
        "ጰ": "p̣",
    }
    return "".join(reverse_map.get(ch, ch) for ch in text)


# ============================
# Gradio UI
# ============================
def transliterate(text, mode, direction):
    if not text.strip():
        return ""

    try:
        if mode == "Syllable-based":
            if direction == "Latin→Geʽez":
                return latin_to_geez_syllable(text)
            else:
                return geez_to_latin_syllable(text)
        else:
            if direction == "Latin→Geʽez":
                return latin_to_geez_letter(text)
            else:
                return geez_to_latin_letter(text)
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    with gr.Blocks(title="Geʽez Transliterator") as demo:
        gr.Markdown("## Geʽez ↔ Latin Transliterator")
        gr.Markdown("""
        **Phonetic shortcuts:** ch→č, sh→š, kh→x, zh→ž, ny→ñ, ts/S→ṣ, H→ḥ, K→ḫ, T→ṭ, A→ʿ

        **Example:** "tsaAda" → "ጻዕዳ" (white)
        """)

        with gr.Row():
            with gr.Column():
                text = gr.Textbox(
                    label="Input Text",
                    placeholder="Enter text to transliterate...",
                    lines=3,
                )
                mode = gr.Radio(
                    ["Syllable-based", "Letter-based"],
                    value="Syllable-based",
                    label="Conversion Mode",
                )
                direction = gr.Radio(
                    ["Latin→Geʽez", "Geʽez→Latin"],
                    value="Latin→Geʽez",
                    label="Direction",
                )
                btn = gr.Button("Convert", variant="primary")

            with gr.Column():
                out = gr.Textbox(label="Output", lines=3, interactive=False)

        # Auto-convert on input change
        text.change(fn=transliterate, inputs=[text, mode, direction], outputs=out)
        mode.change(fn=transliterate, inputs=[text, mode, direction], outputs=out)
        direction.change(fn=transliterate, inputs=[text, mode, direction], outputs=out)
        btn.click(fn=transliterate, inputs=[text, mode, direction], outputs=out)

        # Examples
        gr.Examples(
            examples=[
                ["tsaAda", "Syllable-based", "Latin→Geʽez"],
                ["ጻዕዳ", "Syllable-based", "Geʽez→Latin"],
                ["salam", "Syllable-based", "Latin→Geʽez"],
                ["ሰላም", "Syllable-based", "Geʽez→Latin"],
            ],
            inputs=[text, mode, direction],
            outputs=out,
            fn=transliterate,
        )

    demo.launch()
