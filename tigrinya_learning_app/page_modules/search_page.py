"""
Search and translation page module
Provides word search, translation, and vocabulary display functionality
"""

import streamlit as st
from deep_translator import GoogleTranslator
from utils.image_loader import ImageLoader
from utils.vocab_data import COMMON_PHRASES, VOCAB_CATEGORIES, VOCAB_DICT

from clientTranslation import geez_to_latin_syllable, latin_to_geez_syllable


def create_word_card(
    word: str, translation: str, phonetic: str, show_image: bool = True
):
    """Create a styled word card with optional image"""
    col1, col2 = st.columns([2, 3] if show_image else [1, 1])

    with col1:
        st.markdown(
            f"""
        <div style='
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 15px;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            color: white;
            text-align: center;
        '>
            <h2 style='margin: 0; font-size: 1.5em;'>{word.title()}</h2>
            <h1 style='margin: 15px 0; font-size: 3.5em; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{translation}</h1>
            <h3 style='margin: 0; opacity: 0.9;'>({phonetic})</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )

    if show_image:
        with col2:
            image_loader = ImageLoader()
            image_loader.display_image_with_caption(word, translation, phonetic)


def search_vocabulary(query: str, search_type: str = "both"):
    """Search vocabulary with fuzzy matching"""
    query = query.lower().strip()
    results = []

    if not query:
        return results

    # Search in main vocabulary
    for eng_word, tigrinya_word in VOCAB_DICT.items():
        match_found = False

        if search_type in ["english", "both"]:
            if query in eng_word.lower():
                match_found = True

        if search_type in ["tigrinya", "both"]:
            if (
                query in tigrinya_word
                or query in geez_to_latin_syllable(tigrinya_word).lower()
            ):
                match_found = True

        if match_found:
            phonetic = geez_to_latin_syllable(tigrinya_word)
            results.append(
                {
                    "english": eng_word,
                    "tigrinya": tigrinya_word,
                    "phonetic": phonetic,
                    "category": get_word_category(eng_word),
                }
            )

    # Search in common phrases
    for eng_phrase, tigrinya_phrase in COMMON_PHRASES.items():
        match_found = False

        if search_type in ["english", "both"]:
            if query in eng_phrase.lower():
                match_found = True

        if search_type in ["tigrinya", "both"]:
            if query in tigrinya_phrase:
                match_found = True

        if match_found:
            phonetic = geez_to_latin_syllable(tigrinya_phrase)
            results.append(
                {
                    "english": eng_phrase,
                    "tigrinya": tigrinya_phrase,
                    "phonetic": phonetic,
                    "category": "phrases",
                }
            )

    return sorted(results, key=lambda x: x["english"])


def get_word_category(word: str):
    """Find which category a word belongs to"""
    for category, words in VOCAB_CATEGORIES.items():
        if word in words:
            return category
    return "other"


def translate_with_google(text: str, source: str = "auto", target: str = "ti"):
    """Translate text using Google Translator"""
    try:
        translator = GoogleTranslator(source=source, target=target)
        translation = translator.translate(text)
        return translation
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None


def render():
    """Main render function for search page"""
    st.subheader("🔍 Search for a word")

    # Create tabs for different search modes
    tab1, tab2, tab3 = st.tabs(
        ["🔍 Word Search", "🌐 Live Translation", "📝 Transliteration"]
    )

    with tab1:
        col1, col2 = st.columns([1, 1])

        with col1:
            # Input methods
            input_method = st.radio(
                "Input method:",
                ["Type word", "Select from dropdown"],
                help="Choose how you want to input the word",
            )

            if input_method == "Type word":
                search_query = st.text_input(
                    "Enter a word in English or Tigrinya:",
                    placeholder="Type here... (e.g., 'hello', 'water', 'ሰላም')",
                )

                # Search type selection
                search_type = st.radio(
                    "Search in:",
                    ["both", "english", "tigrinya"],
                    horizontal=True,
                    help="Choose which language to search in",
                )

            else:  # Dropdown selection
                # Category filter
                selected_category = st.selectbox(
                    "Choose category:",
                    ["all"] + list(VOCAB_CATEGORIES.keys()),
                    help="Filter words by category",
                )

                # Word selection based on category
                if selected_category == "all":
                    word_options = list(VOCAB_DICT.keys())
                else:
                    word_options = list(VOCAB_CATEGORIES[selected_category].keys())

                selected_word = st.selectbox(
                    "Select a word:",
                    [""] + sorted(word_options),
                    help="Choose a word from the vocabulary",
                )

                search_query = selected_word
                search_type = "english"

        with col2:
            # Display search results or selected word
            if input_method == "Type word" and search_query:
                results = search_vocabulary(search_query, search_type)

                if results:
                    st.success(f"Found {len(results)} result(s)")

                    # Display results
                    for i, result in enumerate(results[:5]):  # Show top 5 results
                        with st.expander(
                            f"{result['english']} - {result['tigrinya']}",
                            expanded=(i == 0),
                        ):
                            create_word_card(
                                result["english"],
                                result["tigrinya"],
                                result["phonetic"],
                            )

                            # Show category
                            st.caption(f"Category: {result['category'].title()}")

                            # Audio pronunciation placeholder
                            st.button(
                                "🔊 Play pronunciation",
                                key=f"audio_{i}",
                                help="Audio pronunciation (feature coming soon)",
                            )
                else:
                    st.warning(f"No results found for '{search_query}'")

                    # Suggest alternatives
                    st.info("💡 Try searching for:")
                    suggestions = [
                        "hello",
                        "water",
                        "thank you",
                        "mother",
                        "red",
                        "house",
                    ]
                    cols = st.columns(3)
                    for i, suggestion in enumerate(suggestions):
                        with cols[i % 3]:
                            if st.button(suggestion, key=f"suggest_{i}"):
                                st.rerun()

            elif input_method == "Select from dropdown" and selected_word:
                # Display selected word
                tigrinya_word = VOCAB_DICT[selected_word]
                phonetic = geez_to_latin_syllable(tigrinya_word)
                category = get_word_category(selected_word)

                create_word_card(selected_word, tigrinya_word, phonetic)
                st.caption(f"Category: {category.title()}")

                # Show related words from same category
                if category in VOCAB_CATEGORIES:
                    related_words = VOCAB_CATEGORIES[category]
                    related_list = [
                        w for w in related_words.keys() if w != selected_word
                    ][:3]

                    if related_list:
                        st.markdown("**Related words:**")
                        for word in related_list:
                            st.write(f"• {word} - {related_words[word]}")

    with tab2:
        st.markdown("### 🌐 Live Translation with Google Translate")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**English to Tigrinya**")
            english_text = st.text_area(
                "Enter English text:",
                placeholder="Type English text here...",
                height=100,
            )

            if st.button("Translate to Tigrinya", type="primary"):
                if english_text.strip():
                    with st.spinner("Translating..."):
                        tigrinya_translation = translate_with_google(
                            english_text, "en", "ti"
                        )
                        if tigrinya_translation:
                            st.success("Translation completed!")
                            st.markdown(
                                f"""
                            <div style='
                                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                                padding: 20px;
                                border-radius: 10px;
                                color: white;
                                font-size: 1.2em;
                                text-align: center;
                                margin: 10px 0;
                            '>
                                {tigrinya_translation}
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
                else:
                    st.warning("Please enter some text to translate")

        with col2:
            st.markdown("**Tigrinya to English**")
            tigrinya_text = st.text_area(
                "Enter Tigrinya text:", placeholder="ትግርኛ ጽሑፍ ኣብዚ ጸሓፍ...", height=100
            )

            if st.button("Translate to English", type="primary"):
                if tigrinya_text.strip():
                    with st.spinner("Translating..."):
                        english_translation = translate_with_google(
                            tigrinya_text, "ti", "en"
                        )
                        if english_translation:
                            st.success("Translation completed!")
                            st.markdown(
                                f"""
                            <div style='
                                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
                                padding: 20px;
                                border-radius: 10px;
                                color: white;
                                font-size: 1.2em;
                                text-align: center;
                                margin: 10px 0;
                            '>
                                {english_translation}
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )
                else:
                    st.warning("Please enter some text to translate")

        # Translation tips
        st.markdown("---")
        st.markdown("### 💡 Translation Tips")
        st.info("""
        • **Google Translate** provides general translations but may not be perfect for all Tigrinya dialects
        • **Use simple sentences** for better accuracy
        • **Check the vocabulary section** for verified word translations
        • **Combine with transliteration** for pronunciation help
        """)

    with tab3:
        st.markdown("### 📝 Geʽez Transliteration")
        st.markdown(
            "Convert between Latin script and Geʽez script using the built-in transliterator"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Latin to Geʽez**")
            latin_input = st.text_area(
                "Enter text in Latin script:",
                placeholder="Example: salam (for hello)",
                height=100,
                help="Use phonetic spelling: ch→č, sh→š, etc.",
            )

            if latin_input.strip():
                geez_output = latin_to_geez_syllable(latin_input)
                st.markdown("**Result:**")
                st.markdown(
                    f"""
                <div style='
                    background: #f0f2f6;
                    padding: 15px;
                    border-radius: 8px;
                    font-size: 1.5em;
                    text-align: center;
                    border-left: 4px solid #4CAF50;
                '>
                    {geez_output}
                </div>
                """,
                    unsafe_allow_html=True,
                )

        with col2:
            st.markdown("**Geʽez to Latin**")
            geez_input = st.text_area(
                "Enter text in Geʽez script:",
                placeholder="Example: ሰላም (for hello)",
                height=100,
            )

            if geez_input.strip():
                latin_output = geez_to_latin_syllable(geez_input)
                st.markdown("**Result:**")
                st.markdown(
                    f"""
                <div style='
                    background: #f0f2f6;
                    padding: 15px;
                    border-radius: 8px;
                    font-size: 1.5em;
                    text-align: center;
                    border-left: 4px solid #2196F3;
                '>
                    {latin_output}
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Transliteration guide
        st.markdown("---")
        st.markdown("### 📚 Transliteration Guide")

        guide_cols = st.columns(3)

        with guide_cols[0]:
            st.markdown("**Basic Consonants:**")
            st.markdown("""
            - h → ሀ
            - l → ለ
            - m → መ
            - r → ረ
            - s → ሰ
            - t → ተ
            """)

        with guide_cols[1]:
            st.markdown("**Special Characters:**")
            st.markdown("""
            - ch → č → ቸ
            - sh → š → ሸ
            - kh → x → ኀ
            - ts → ṣ → ፀ
            - ny → ñ → ኘ
            """)

        with guide_cols[2]:
            st.markdown("**Vowel Order:**")
            st.markdown("""
            - e (1st) → ለ
            - u (2nd) → ሉ
            - i (3rd) → ሊ
            - a (4th) → ላ
            - ē (5th) → ሌ
            - ə (6th) → ል
            - o (7th) → ሎ
            """)

    # Quick statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Words", len(VOCAB_DICT))
    with col2:
        st.metric("Categories", len(VOCAB_CATEGORIES))
    with col3:
        st.metric("Common Phrases", len(COMMON_PHRASES))
    with col4:
        if "search_count" not in st.session_state:
            st.session_state.search_count = 0
        if search_query:
            st.session_state.search_count += 1
        st.metric("Searches Today", st.session_state.search_count)


if __name__ == "__main__":
    render()
