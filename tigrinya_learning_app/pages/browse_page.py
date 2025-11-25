"""
Browse vocabulary page module
Provides category-based vocabulary browsing and exploration
"""

import random

import streamlit as st
from utils.image_loader import ImageLoader
from utils.vocab_data import VOCAB_CATEGORIES, VOCAB_DICT, VOCAB_STATS, get_random_words

from clientTranslation import geez_to_latin_syllable


def create_vocabulary_grid(words_dict, cols=3, key_prefix=""):
    """Create a grid layout for vocabulary words"""
    words = list(words_dict.items())

    # Create columns
    columns = st.columns(cols)

    for i, (english, tigrinya) in enumerate(words):
        col_idx = i % cols
        with columns[col_idx]:
            phonetic = geez_to_latin_syllable(tigrinya)

            st.markdown(
                f"""
            <div style='
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 10px;
                color: white;
                text-align: center;
                margin: 5px 0;
            '>
                <h3 style='margin: 0;'>{english.title()}</h3>
                <h2 style='margin: 10px 0; font-size: 2em;'>{tigrinya}</h2>
                <p style='margin: 0; opacity: 0.9;'>({phonetic})</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            # Add to practice session button
            if st.button(f"Add to Practice", key=f"{key_prefix}_practice_{english}_{i}"):
                if "practice_words" not in st.session_state:
                    st.session_state.practice_words = []

                word_item = {
                    "english": english,
                    "tigrinya": tigrinya,
                    "phonetic": phonetic,
                }
                if word_item not in st.session_state.practice_words:
                    st.session_state.practice_words.append(word_item)
                    st.success(f"Added '{english}' to practice session!")
                else:
                    st.info(f"'{english}' is already in your practice session")


def display_category_stats(category_name, words_dict):
    """Display statistics for a category"""
    st.markdown(
        f"""
    <div style='
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    '>
        <h4 style='margin: 0;'>📊 {category_name.title()} Statistics</h4>
        <p style='margin: 5px 0;'>Total Words: {len(words_dict)}</p>
        <p style='margin: 5px 0;'>Average Word Length: {sum(len(word) for word in words_dict.keys()) / len(words_dict):.1f} letters</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def create_word_of_the_day():
    """Create a word of the day section"""
    if "word_of_the_day" not in st.session_state:
        # Select a random word for the day
        random.seed()  # Use current time as seed
        daily_word = random.choice(list(VOCAB_DICT.items()))
        st.session_state.word_of_the_day = {
            "english": daily_word[0],
            "tigrinya": daily_word[1],
            "phonetic": geez_to_latin_syllable(daily_word[1]),
        }

    word_data = st.session_state.word_of_the_day

    st.markdown(
        f"""
    <div style='
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #ff9a56;
    '>
        <h2 style='margin: 0; color: #8b4513;'>🌟 Word of the Day</h2>
        <h1 style='margin: 15px 0; color: #8b4513; font-size: 2.5em;'>{word_data["english"].title()}</h1>
        <h1 style='margin: 15px 0; color: #8b4513; font-size: 3em;'>{word_data["tigrinya"]}</h1>
        <h3 style='margin: 0; color: #8b4513; opacity: 0.8;'>({word_data["phonetic"]})</h3>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Show image for word of the day
    image_loader = ImageLoader()
    image = image_loader.get_image(word_data["english"])
    if image:
        st.image(
            image,
            caption=f"{word_data['english']} - {word_data['tigrinya']}",
            width='stretch',
        )


def render():
    """Main render function for browse page"""
    st.subheader("📚 Browse Vocabulary by Category")

    # Word of the day section
    create_word_of_the_day()

    # Create tabs for different browsing modes
    tab1, tab2, tab3, tab4 = st.tabs(
        ["🗂️ By Category", "🎲 Random Words", "📈 Popular Words", "🎯 Practice Session"]
    )

    with tab1:
        st.markdown("### Browse by Category")

        # Category selection
        col1, col2 = st.columns([1, 2])

        with col1:
            selected_category = st.selectbox(
                "Choose a category:",
                ["all"] + list(VOCAB_CATEGORIES.keys()),
                format_func=lambda x: x.title() if x != "all" else "All Categories",
            )

            # Display category info
            if selected_category != "all":
                category_words = VOCAB_CATEGORIES[selected_category]
                display_category_stats(selected_category, category_words)

                # Quick category navigation
                st.markdown("**Quick Navigation:**")
                for cat in list(VOCAB_CATEGORIES.keys())[:5]:
                    if st.button(cat.title(), key=f"nav_{cat}"):
                        st.session_state.selected_category = cat
                        st.rerun()

        with col2:
            # Display words based on selection
            if selected_category == "all":
                st.markdown("### All Vocabulary")

                # Show overview statistics
                st.markdown(
                    f"""
                <div style='
                    background: #f0f2f6;
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px 0;
                '>
                    <h4>📊 Vocabulary Overview</h4>
                    <div style='display: flex; justify-content: space-between;'>
                        <div>Total Words: <strong>{VOCAB_STATS["total_words"]}</strong></div>
                        <div>Categories: <strong>{VOCAB_STATS["total_categories"]}</strong></div>
                        <div>Phrases: <strong>{VOCAB_STATS["total_phrases"]}</strong></div>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # Show sample from each category
                for category, words in list(VOCAB_CATEGORIES.items())[:3]:
                    st.markdown(f"**{category.title()} (Sample):**")
                    sample_words = dict(list(words.items())[:6])
                    create_vocabulary_grid(sample_words, cols=2, key_prefix=f"all_{category}")

                    if len(words) > 6:
                        st.caption(f"... and {len(words) - 6} more words in {category}")

            else:
                category_words = VOCAB_CATEGORIES[selected_category]
                st.markdown(
                    f"### {selected_category.title()} ({len(category_words)} words)"
                )

                # Search within category
                search_term = st.text_input(
                    f"Search within {selected_category}:",
                    placeholder=f"Search {selected_category} words...",
                )

                if search_term:
                    filtered_words = {
                        k: v
                        for k, v in category_words.items()
                        if search_term.lower() in k.lower() or search_term in v
                    }
                    if filtered_words:
                        st.success(f"Found {len(filtered_words)} matching words")
                        create_vocabulary_grid(filtered_words, key_prefix=f"{selected_category}_search")
                    else:
                        st.warning(f"No words found matching '{search_term}'")
                else:
                    # Display all words in category
                    create_vocabulary_grid(category_words, key_prefix=selected_category)

    with tab2:
        st.markdown("### 🎲 Random Word Discovery")

        col1, col2 = st.columns([1, 2])

        with col1:
            # Random word controls
            num_words = st.slider("Number of words:", 5, 20, 10)

            random_category = st.selectbox(
                "Category for random words:",
                ["all"] + list(VOCAB_CATEGORIES.keys()),
                key="random_category",
            )

            if st.button("🎲 Generate Random Words", type="primary"):
                if random_category == "all":
                    random_words = get_random_words(num_words)
                else:
                    random_words = get_random_words(num_words, random_category)

                st.session_state.random_words = random_words
                st.success(f"Generated {len(random_words)} random words!")

            # Difficulty filter for random words
            st.markdown("**Difficulty Level:**")
            difficulty = st.radio(
                "Choose difficulty:",
                ["mixed", "beginner", "intermediate", "advanced"],
                help="Filter random words by difficulty level",
            )

        with col2:
            # Display random words
            if "random_words" in st.session_state:
                st.markdown(f"### Random Words ({len(st.session_state.random_words)})")
                create_vocabulary_grid(st.session_state.random_words, key_prefix="random")

                # Practice all random words button
                if st.button("📝 Practice All These Words"):
                    if "practice_words" not in st.session_state:
                        st.session_state.practice_words = []

                    for eng, tig in st.session_state.random_words.items():
                        word_item = {
                            "english": eng,
                            "tigrinya": tig,
                            "phonetic": geez_to_latin_syllable(tig),
                        }
                        if word_item not in st.session_state.practice_words:
                            st.session_state.practice_words.append(word_item)

                    st.success(
                        f"Added {len(st.session_state.random_words)} words to practice session!"
                    )
            else:
                st.info("Click 'Generate Random Words' to see random vocabulary!")

    with tab3:
        st.markdown("### 📈 Popular and Frequently Used Words")

        # Most common words by category
        st.markdown("#### Most Essential Words by Category")

        essential_words = {
            "greetings": ["hello", "thank you", "goodbye"],
            "family": ["mother", "father", "child"],
            "food": ["water", "bread", "milk"],
            "colors": ["red", "blue", "white"],
            "numbers": ["one", "two", "three"],
        }

        for category, word_list in essential_words.items():
            if category in VOCAB_CATEGORIES:
                st.markdown(f"**{category.title()}:**")
                essential_category_words = {
                    word: VOCAB_CATEGORIES[category][word]
                    for word in word_list
                    if word in VOCAB_CATEGORIES[category]
                }
                create_vocabulary_grid(essential_category_words, cols=3, key_prefix=category)

        # Learning recommendations
        st.markdown("---")
        st.markdown("### 💡 Learning Recommendations")

        recommendations = [
            "Start with **greetings** - essential for basic conversation",
            "Learn **family** terms - used frequently in daily life",
            "Master **numbers 1-10** - foundation for counting and time",
            "Practice **colors** - helpful for describing objects",
            "Focus on **food** vocabulary - useful for daily needs",
        ]

        for rec in recommendations:
            st.markdown(f"• {rec}")

    with tab4:
        st.markdown("### 🎯 Your Practice Session")

        if "practice_words" not in st.session_state:
            st.session_state.practice_words = []

        practice_words = st.session_state.practice_words

        if practice_words:
            st.success(f"You have {len(practice_words)} words in your practice session")

            # Practice session controls
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📝 Start Quiz", type="primary"):
                    st.session_state.practice_mode = "quiz"
                    st.info(
                        "Quiz mode activated! Go to the Quiz page to practice these words."
                    )

            with col2:
                if st.button("🔄 Shuffle Words"):
                    random.shuffle(st.session_state.practice_words)
                    st.success("Words shuffled!")

            with col3:
                if st.button("🗑️ Clear Session"):
                    st.session_state.practice_words = []
                    st.success("Practice session cleared!")
                    st.rerun()

            # Display practice words
            st.markdown("#### Words in Practice Session:")

            # Convert to dictionary format for grid display
            practice_dict = {
                word["english"]: word["tigrinya"] for word in practice_words
            }
            create_vocabulary_grid(practice_dict, key_prefix="practice")

            # Remove individual words
            st.markdown("#### Manage Practice Words:")
            for i, word in enumerate(practice_words):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(
                        f"{word['english']} - {word['tigrinya']} ({word['phonetic']})"
                    )
                with col2:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.practice_words.pop(i)
                        st.rerun()

        else:
            st.info(
                "Your practice session is empty. Browse vocabulary and add words to practice!"
            )

            # Quick add popular words
            st.markdown("#### Quick Add Popular Words:")
            popular_words = ["hello", "thank you", "water", "mother", "red"]

            cols = st.columns(len(popular_words))
            for i, word in enumerate(popular_words):
                with cols[i]:
                    if word in VOCAB_DICT:
                        tigrinya = VOCAB_DICT[word]
                        phonetic = geez_to_latin_syllable(tigrinya)

                        if st.button(f"+ {word}", key=f"quick_add_{i}"):
                            if "practice_words" not in st.session_state:
                                st.session_state.practice_words = []

                            word_item = {
                                "english": word,
                                "tigrinya": tigrinya,
                                "phonetic": phonetic,
                            }
                            st.session_state.practice_words.append(word_item)
                            st.success(f"Added '{word}'!")
                            st.rerun()

    # Footer statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Categories Available", len(VOCAB_CATEGORIES))
    with col2:
        st.metric("Total Vocabulary", len(VOCAB_DICT))
    with col3:
        practice_count = len(st.session_state.get("practice_words", []))
        st.metric("Words in Practice", practice_count)
    with col4:
        if "browse_sessions" not in st.session_state:
            st.session_state.browse_sessions = 0
        st.session_state.browse_sessions += 1
        st.metric("Browse Sessions", st.session_state.browse_sessions)


if __name__ == "__main__":
    render()
