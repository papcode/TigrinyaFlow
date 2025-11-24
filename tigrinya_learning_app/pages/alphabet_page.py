"""
Alphabet page module
Provides Geʽez/Tigrinya alphabet display with handwriting animations
"""

import streamlit as st
from utils.image_loader import ImageLoader

from clientTranslation import alef_row, feedel_rows


def create_handwriting_animation_html(character, char_name=""):
    """Create a simple handwriting animation for a character"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Ethiopic:wght@400;700&display=swap');
            body {{
                margin: 0;
                padding: 20px;
                font-family: 'Noto Sans Ethiopic', 'Ebrima', 'Nyala', sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 400px;
            }}

            .character-display {{
                font-size: 8em;
                text-align: center;
                color: #2c3e50;
                margin: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                animation: writeIn 2s ease-in-out;
            }}

            .character-info {{
                font-size: 1.5em;
                text-align: center;
                color: #666;
                margin: 10px;
                background: rgba(255,255,255,0.8);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}

            @keyframes writeIn {{
                0% {{
                    opacity: 0;
                    transform: scale(0.5) rotate(-5deg);
                }}
                50% {{
                    opacity: 0.7;
                    transform: scale(1.1) rotate(2deg);
                }}
                100% {{
                    opacity: 1;
                    transform: scale(1) rotate(0deg);
                }}
            }}

            .stroke-animation {{
                animation: strokeDraw 3s ease-in-out infinite;
            }}

            @keyframes strokeDraw {{
                0%, 100% {{
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                }}
                50% {{
                    text-shadow: 0 0 20px rgba(102,126,234,0.8), 2px 2px 4px rgba(0,0,0,0.2);
                }}
            }}
        </style>
    </head>
    <body>
        <div class="character-display stroke-animation">{character}</div>
        <div class="character-info">
            <strong>{char_name}</strong><br>
            Click to see handwriting animation
        </div>
        <script>
            document.querySelector('.character-display').addEventListener('click', function() {{
                this.style.animation = 'none';
                setTimeout(() => {{
                    this.style.animation = 'writeIn 2s ease-in-out, strokeDraw 3s ease-in-out infinite';
                }}, 100);
            }});
        </script>
    </body>
    </html>
    """
    return html_content


def create_character_grid(characters_dict, title="Characters", cols=7):
    """Create a grid of characters with click handlers"""
    st.markdown(f"### {title}")

    characters = (
        list(characters_dict.items())
        if isinstance(characters_dict, dict)
        else list(enumerate(characters_dict))
    )

    # Create rows
    for i in range(0, len(characters), cols):
        row_chars = characters[i : i + cols]
        columns = st.columns(cols)

        for j, (key, char) in enumerate(row_chars):
            with columns[j]:
                char_name = key if isinstance(key, str) else f"Form {key + 1}"

                # Create clickable character button
                if st.button(
                    char,
                    key=f"char_{title}_{i}_{j}",
                    help=f"Click to see {char} handwriting animation",
                ):
                    st.session_state[f"selected_char"] = char
                    st.session_state[f"selected_char_name"] = char_name


def render():
    """Main render function for alphabet page"""
    st.subheader("✍️ ፊደላት (Alphabets) - Geʽez Script")

    # Introduction
    st.markdown("""
    The Geʽez script (ፊደል) is used to write Tigrinya, Amharic, and other Ethiopian languages.
    Each character represents a consonant-vowel combination. Click on any character to see its handwriting animation!
    """)

    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🔤 Full Alphabet", "🎯 Character Finder", "✍️ Practice", "📚 Learning Guide"]
    )

    with tab1:
        # Alef row (vowel-only characters)
        st.markdown("#### Vowel Characters (አ-series)")
        vowel_names = ["a", "u", "i", "ā", "ē", "ə", "o"]
        alef_dict = {name: char for name, char in zip(vowel_names, alef_row)}
        create_character_grid(alef_dict, "Alef_Row", cols=7)

        st.markdown("---")

        # Main feedel rows
        st.markdown("#### Consonant-Vowel Characters")

        # Group characters by common consonants for better display
        common_consonants = ["h", "l", "m", "r", "s", "t", "b", "n"]
        special_consonants = [
            "ḥ",
            "x",
            "ḫ",
            "ʿ",
            "š",
            "q",
            "ṭ",
            "č",
            "č̣",
            "p",
            "p̣",
            "g",
            "d",
            "f",
            "z",
            "ž",
            "y",
            "w",
            "j",
            "ñ",
            "ṣ",
        ]

        # Display common consonants first
        st.markdown("##### Common Consonants")
        for consonant in common_consonants:
            if consonant in feedel_rows:
                st.markdown(f"**{consonant.upper()} ({consonant})**")
                vowel_forms = {
                    f"{consonant}{vowel}": char
                    for vowel, char in zip(
                        ["e", "u", "i", "a", "ē", "ə", "o"], feedel_rows[consonant]
                    )
                }
                create_character_grid(vowel_forms, f"feedel_{consonant}", cols=7)

        # Display special characters
        with st.expander("🔍 Special Characters & Rare Consonants", expanded=False):
            for consonant in special_consonants:
                if consonant in feedel_rows:
                    st.markdown(f"**{consonant.upper()} ({consonant})**")
                    vowel_forms = {
                        f"{consonant}{vowel}": char
                        for vowel, char in zip(
                            ["e", "u", "i", "a", "ē", "ə", "o"], feedel_rows[consonant]
                        )
                    }
                    create_character_grid(vowel_forms, f"special_{consonant}", cols=7)

    with tab2:
        st.markdown("### 🎯 Find and Practice Characters")

        col1, col2 = st.columns([1, 2])

        with col1:
            # Character search
            search_method = st.radio(
                "Search by:", ["Latin letter", "Geʽez character", "Browse all"]
            )

            if search_method == "Latin letter":
                latin_input = st.text_input(
                    "Enter Latin character(s):", placeholder="h, ha, hab..."
                )

                if latin_input:
                    # Find matching characters
                    matches = []
                    for cons, row in feedel_rows.items():
                        if latin_input.lower() in cons.lower():
                            for i, char in enumerate(row):
                                vowel = ["e", "u", "i", "a", "ē", "ə", "o"][i]
                                matches.append((f"{cons}{vowel}", char))

                    if matches:
                        st.success(f"Found {len(matches)} matches")
                        for latin, geez in matches[:10]:  # Show first 10
                            if st.button(f"{latin} → {geez}", key=f"match_{latin}"):
                                st.session_state["selected_char"] = geez
                                st.session_state["selected_char_name"] = latin
                    else:
                        st.warning("No matches found")

            elif search_method == "Geʽez character":
                geez_input = st.text_input(
                    "Enter Geʽez character:", placeholder="ሀ, ለ, መ..."
                )

                if geez_input and len(geez_input) == 1:
                    # Find character info
                    char_found = False
                    for cons, row in feedel_rows.items():
                        if geez_input in row:
                            vowel_index = row.index(geez_input)
                            vowel = ["e", "u", "i", "a", "ē", "ə", "o"][vowel_index]
                            st.success(f"Character: {geez_input}")
                            st.info(f"Consonant: {cons}")
                            st.info(f"Vowel: {vowel}")
                            st.info(f"Romanization: {cons}{vowel}")

                            if st.button("Practice this character"):
                                st.session_state["selected_char"] = geez_input
                                st.session_state["selected_char_name"] = (
                                    f"{cons}{vowel}"
                                )
                            char_found = True
                            break

                    if not char_found and geez_input in alef_row:
                        vowel_index = alef_row.index(geez_input)
                        vowel = ["a", "u", "i", "ā", "ē", "ə", "o"][vowel_index]
                        st.success(f"Vowel character: {geez_input}")
                        st.info(f"Romanization: {vowel}")
                        char_found = True

                    if not char_found:
                        st.warning("Character not found in the alphabet")

            else:  # Browse all
                st.markdown("**Quick Character Access:**")
                quick_chars = ["ሀ", "ለ", "መ", "ረ", "ሰ", "ተ", "በ", "ነ"]
                for char in quick_chars:
                    if st.button(char, key=f"quick_{char}"):
                        st.session_state["selected_char"] = char
                        st.session_state["selected_char_name"] = char

        with col2:
            # Display selected character animation
            if "selected_char" in st.session_state:
                char = st.session_state["selected_char"]
                char_name = st.session_state.get("selected_char_name", char)

                st.markdown(f"### Selected Character: {char}")

                # Create handwriting animation
                animation_html = create_handwriting_animation_html(char, char_name)
                st.components.v1.html(animation_html, height=500)

                # Character information
                st.markdown("#### Character Information")
                st.markdown(f"**Character:** {char}")
                st.markdown(f"**Name:** {char_name}")

                # Find character in alphabet
                for cons, row in feedel_rows.items():
                    if char in row:
                        vowel_index = row.index(char)
                        vowel = ["e", "u", "i", "a", "ē", "ə", "o"][vowel_index]
                        st.markdown(f"**Consonant:** {cons}")
                        st.markdown(f"**Vowel:** {vowel}")
                        st.markdown(f"**Full form:** {cons}{vowel}")
                        break

                # Show related characters (same consonant)
                if char not in alef_row:
                    for cons, row in feedel_rows.items():
                        if char in row:
                            st.markdown("#### Related Characters (same consonant)")
                            related_dict = {
                                f"{cons}{vowel}": c
                                for vowel, c in zip(
                                    ["e", "u", "i", "a", "ē", "ə", "o"], row
                                )
                            }
                            create_character_grid(
                                related_dict, f"related_{cons}", cols=7
                            )
                            break
            else:
                st.info(
                    "Select a character from the left panel to see its handwriting animation"
                )

    with tab3:
        st.markdown("### ✍️ Handwriting Practice")

        # Practice modes
        practice_mode = st.selectbox(
            "Choose practice mode:",
            ["Character Recognition", "Vowel Forms", "Common Words", "Random Practice"],
        )

        if practice_mode == "Character Recognition":
            st.markdown("#### Identify the Character")

            if st.button("Show Random Character", type="primary"):
                # Select random character
                import random

                all_chars = []
                for row in feedel_rows.values():
                    all_chars.extend(row)
                all_chars.extend(alef_row)

                random_char = random.choice(all_chars)
                st.session_state["practice_char"] = random_char

            if "practice_char" in st.session_state:
                char = st.session_state["practice_char"]

                # Display character large
                st.markdown(
                    f"""
                <div style='
                    font-size: 8em;
                    text-align: center;
                    padding: 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 15px;
                    margin: 20px 0;
                '>
                    {char}
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Answer input
                user_answer = st.text_input(
                    "What is this character in Latin script?", key="recognition_answer"
                )

                if st.button("Check Answer"):
                    # Find correct answer
                    correct_answer = None
                    for cons, row in feedel_rows.items():
                        if char in row:
                            vowel_index = row.index(char)
                            vowel = ["e", "u", "i", "a", "ē", "ə", "o"][vowel_index]
                            correct_answer = f"{cons}{vowel}"
                            break

                    if char in alef_row:
                        vowel_index = alef_row.index(char)
                        correct_answer = ["a", "u", "i", "ā", "ē", "ə", "o"][
                            vowel_index
                        ]

                    if user_answer.lower() == correct_answer.lower():
                        st.success(f"Correct! {char} = {correct_answer}")
                    else:
                        st.error(f"Not quite. {char} = {correct_answer}")

        elif practice_mode == "Vowel Forms":
            st.markdown("#### Practice Vowel Forms")

            consonant_choice = st.selectbox(
                "Choose consonant:", list(feedel_rows.keys())
            )

            if consonant_choice:
                st.markdown(
                    f"**Practice {consonant_choice.upper()} with different vowels:**"
                )

                vowel_forms = feedel_rows[consonant_choice]
                vowel_names = ["e", "u", "i", "a", "ē", "ə", "o"]

                practice_dict = {
                    f"{consonant_choice}{vowel}": char
                    for vowel, char in zip(vowel_names, vowel_forms)
                }
                create_character_grid(
                    practice_dict, f"practice_{consonant_choice}", cols=7
                )

        elif practice_mode == "Common Words":
            st.markdown("#### Practice with Common Words")

            # Common Tigrinya words broken down by characters
            common_words = {
                "ሰላም": ["ሰ", "ላ", "ም"],  # salam - peace/hello
                "ማይ": ["ማ", "ይ"],  # may - water
                "ኣቦ": ["ኣ", "ቦ"],  # abo - father
                "እንዳ": ["እ", "ን", "ዳ"],  # ǝnda - mother
            }

            selected_word = st.selectbox(
                "Choose a word to practice:", list(common_words.keys())
            )

            if selected_word:
                characters = common_words[selected_word]

                st.markdown(f"**Word: {selected_word}**")
                st.markdown("**Characters in this word:**")

                cols = st.columns(len(characters))
                for i, char in enumerate(characters):
                    with cols[i]:
                        st.markdown(
                            f"""
                        <div style='
                            font-size: 4em;
                            text-align: center;
                            padding: 20px;
                            background: #f8f9fa;
                            border-radius: 10px;
                            margin: 10px 0;
                            border: 2px solid #dee2e6;
                        '>
                            {char}
                        </div>
                        """,
                            unsafe_allow_html=True,
                        )

        else:  # Random Practice
            st.markdown("#### Random Character Practice")

            difficulty = st.select_slider("Difficulty:", ["Easy", "Medium", "Hard"])

            if st.button("Generate Random Practice Set", type="primary"):
                import random

                if difficulty == "Easy":
                    # Common consonants only
                    practice_consonants = ["h", "l", "m", "r", "s", "t", "b", "n"]
                elif difficulty == "Medium":
                    practice_consonants = list(feedel_rows.keys())[:15]
                else:
                    practice_consonants = list(feedel_rows.keys())

                # Generate 6 random characters
                random_chars = []
                for _ in range(6):
                    cons = random.choice(practice_consonants)
                    char_index = random.randint(0, 6)
                    char = feedel_rows[cons][char_index]
                    vowel = ["e", "u", "i", "a", "ē", "ə", "o"][char_index]
                    random_chars.append((char, f"{cons}{vowel}"))

                st.session_state["random_practice"] = random_chars

            if "random_practice" in st.session_state:
                st.markdown("**Practice these characters:**")

                chars_dict = {
                    name: char for char, name in st.session_state["random_practice"]
                }
                create_character_grid(chars_dict, "random_practice", cols=3)

    with tab4:
        st.markdown("### 📚 Learning Guide")

        # Learning tips and information
        st.markdown("""
        #### 🎯 How to Learn the Geʽez Alphabet

        **1. Start with the Vowel Sounds**
        - Learn the 7 vowel sounds: e, u, i, a, ē, ə, o
        - The አ series shows these vowels without consonants

        **2. Master Common Consonants First**
        - Begin with: h, l, m, r, s, t, b, n
        - Each consonant has 7 forms (one for each vowel)

        **3. Practice Pattern Recognition**
        - Notice how vowel markers change the base character
        - The 6th form (ə) is the base consonant without vowel marking

        **4. Use Memory Techniques**
        - Associate characters with familiar shapes
        - Practice writing characters by hand
        - Use spaced repetition for memorization
        """)

        # Character learning order
        st.markdown("#### 📖 Recommended Learning Order")

        learning_stages = {
            "Stage 1 - Vowels": list(alef_row),
            "Stage 2 - Basic Consonants": [
                feedel_rows["h"][0],
                feedel_rows["l"][0],
                feedel_rows["m"][0],
                feedel_rows["r"][0],
            ],
            "Stage 3 - Common Letters": [
                feedel_rows["s"][0],
                feedel_rows["t"][0],
                feedel_rows["b"][0],
                feedel_rows["n"][0],
            ],
        }

        for stage, characters in learning_stages.items():
            with st.expander(stage, expanded=False):
                chars_dict = {f"char_{i}": char for i, char in enumerate(characters)}
                create_character_grid(chars_dict, stage, cols=4)

        # Learning resources
        st.markdown("---")
        st.markdown("#### 📱 Practice Tips")

        tips = [
            "🖊️ **Write by hand** - Physical writing helps memorization",
            "🔄 **Use spaced repetition** - Review characters at increasing intervals",
            "📝 **Practice daily** - Even 10 minutes daily is better than long sessions",
            "🎯 **Focus on patterns** - Learn vowel modifications systematically",
            "📚 **Read simple words** - Apply character knowledge in context",
            "🎵 **Use mnemonics** - Create memory aids for difficult characters",
        ]

        for tip in tips:
            st.markdown(tip)

    # Footer with statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    total_characters = sum(len(row) for row in feedel_rows.values()) + len(alef_row)

    with col1:
        st.metric("Total Characters", total_characters)
    with col2:
        st.metric("Consonant Rows", len(feedel_rows))
    with col3:
        st.metric("Vowel Forms", 7)
    with col4:
        practice_count = len(st.session_state.get("random_practice", []))
        st.metric("Practice Set", practice_count)


if __name__ == "__main__":
    render()
