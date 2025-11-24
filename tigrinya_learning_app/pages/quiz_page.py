"""
Quiz page module
Provides interactive quizzes with multiple choice questions and progress tracking
"""

import streamlit as st
from utils.image_loader import ImageLoader
from utils.quiz_manager import QuizManager
from utils.vocab_data import VOCAB_CATEGORIES

from clientTranslation import geez_to_latin_syllable


def display_quiz_question(quiz_data):
    """Display quiz question with options"""
    if not quiz_data:
        return None

    st.markdown(f"### 🎯 {quiz_data['question']}")

    # Display image if available for the word
    image_loader = ImageLoader()
    image = image_loader.get_image(quiz_data["word"])
    if image:
        st.image(image, width=200, caption=f"Visual hint for: {quiz_data['word']}")

    # Display options as radio buttons
    selected_option = st.radio(
        "Choose your answer:", quiz_data["options"], key="quiz_answer"
    )

    return selected_option


def display_quiz_stats(quiz_manager):
    """Display current quiz statistics"""
    stats = quiz_manager.get_statistics()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Score", f"{stats['correct_answers']}/{stats['total_questions']}")
    with col2:
        accuracy = stats["accuracy"] if stats["total_questions"] > 0 else 0
        st.metric("Accuracy", f"{accuracy}%")
    with col3:
        st.metric("Current Streak", stats["current_streak"])
    with col4:
        st.metric("Best Streak", stats["best_streak"])


def display_performance_analysis(quiz_manager):
    """Display detailed performance analysis"""
    stats = quiz_manager.get_statistics()

    if stats["total_questions"] == 0:
        st.info("Take some quiz questions to see your performance analysis!")
        return

    st.markdown("### 📊 Performance Analysis")

    # Performance level
    performance_level = quiz_manager.get_performance_level()
    st.markdown(f"**Current Level:** {performance_level}")

    # Progress bar
    accuracy = stats["accuracy"]
    progress_color = (
        "green" if accuracy >= 80 else "orange" if accuracy >= 60 else "red"
    )
    st.progress(accuracy / 100)

    # Most missed words
    if stats["most_missed"]:
        st.markdown("#### 🎯 Words to Review:")
        for word, count in stats["most_missed"][:3]:
            if word in st.session_state.quiz_state["current_question"]:
                continue
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{word}** - missed {count} time{'s' if count > 1 else ''}")
            with col2:
                if st.button("Review", key=f"review_{word}"):
                    st.info(f"'{word}' will be included in your next practice session")

    # Recommendations
    recommendation = quiz_manager.get_recommendation()
    st.info(f"💡 **Recommendation:** {recommendation}")


def render():
    """Main render function for quiz page"""
    st.subheader("🎯 Quiz Mode - Test Your Knowledge")

    # Initialize quiz manager
    quiz_manager = QuizManager()

    # Create tabs for different quiz modes
    tab1, tab2, tab3 = st.tabs(["🎮 Quick Quiz", "📊 Performance", "⚙️ Settings"])

    with tab1:
        # Quiz settings
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("#### Quiz Settings")

            # Category selection
            category = st.selectbox(
                "Choose category:",
                ["all"] + list(VOCAB_CATEGORIES.keys()),
                format_func=lambda x: x.title() if x != "all" else "All Categories",
            )

            # Quiz type
            quiz_type = st.radio(
                "Quiz type:",
                ["english_to_tigrinya", "tigrinya_to_english"],
                format_func=lambda x: "English → Tigrinya"
                if x == "english_to_tigrinya"
                else "Tigrinya → English",
            )

            # Display current stats
            display_quiz_stats(quiz_manager)

            # Quiz controls
            st.markdown("---")

            if st.button("🎲 New Question", type="primary"):
                quiz_data = quiz_manager.generate_question(category, quiz_type)
                if quiz_data:
                    st.session_state["current_quiz"] = quiz_data
                    # Clear previous answer
                    if "quiz_answer" in st.session_state:
                        del st.session_state["quiz_answer"]
                else:
                    st.error(
                        "Could not generate question. Please check your category selection."
                    )

            if st.button("🔄 Reset Quiz"):
                quiz_manager.reset_quiz()
                st.success("Quiz reset! Start fresh with a new question.")
                st.rerun()

        with col2:
            # Display current question or start screen
            if (
                "current_quiz" in st.session_state
                and not quiz_manager.get_quiz_state()["answered"]
            ):
                quiz_data = st.session_state["current_quiz"]

                # Display question
                selected_answer = display_quiz_question(quiz_data)

                # Submit button
                if st.button(
                    "✅ Submit Answer", type="primary", disabled=not selected_answer
                ):
                    if selected_answer:
                        result = quiz_manager.submit_answer(selected_answer)
                        st.session_state["quiz_result"] = result
                        st.rerun()

            elif (
                quiz_manager.get_quiz_state()["answered"]
                and "quiz_result" in st.session_state
            ):
                # Show result
                result = st.session_state["quiz_result"]
                quiz_data = st.session_state["current_quiz"]

                if result["is_correct"]:
                    st.success("🎉 Correct!")
                else:
                    st.error("❌ Incorrect")

                # Show correct answer
                st.markdown(f"**Correct Answer:** {result['correct_answer']}")
                st.markdown(f"**Your Answer:** {result['selected_answer']}")

                # Show word details
                st.markdown("---")
                st.markdown(
                    f"**Word:** {quiz_data['word']} → {quiz_data['translation']}"
                )
                phonetic = geez_to_latin_syllable(quiz_data["translation"])
                st.markdown(f"**Pronunciation:** {phonetic}")

                # Show image
                image_loader = ImageLoader()
                image = image_loader.get_image(quiz_data["word"])
                if image:
                    st.image(
                        image,
                        width=300,
                        caption=f"{quiz_data['word']} - {quiz_data['translation']}",
                    )

                # Current score
                st.markdown(
                    f"**Current Score:** {result['score']}/{result['total']} ({result['current_streak']} streak)"
                )

                # Next question button
                if st.button("➡️ Next Question", type="primary"):
                    # Clear answered state for next question
                    quiz_manager.reset_session()
                    if "quiz_result" in st.session_state:
                        del st.session_state["quiz_result"]
                    if "current_quiz" in st.session_state:
                        del st.session_state["current_quiz"]
                    st.rerun()

            else:
                # Start screen
                st.markdown("""
                ### 🎯 Welcome to Quiz Mode!

                Test your Tigrinya vocabulary knowledge with interactive quizzes.

                **How it works:**
                1. Choose your preferred category and quiz type
                2. Click "New Question" to start
                3. Select your answer from the multiple choices
                4. Submit and see your results instantly
                5. Track your progress and improve over time

                **Tips for better scores:**
                - Start with familiar categories
                - Review vocabulary cards before quizzing
                - Pay attention to pronunciation hints
                - Practice regularly to build streaks
                """)

                # Quick start buttons for popular categories
                st.markdown("#### 🚀 Quick Start")

                quick_categories = ["colors", "family", "greetings", "food", "numbers"]
                cols = st.columns(len(quick_categories))

                for i, cat in enumerate(quick_categories):
                    if cat in VOCAB_CATEGORIES:
                        with cols[i]:
                            if st.button(f"{cat.title()}", key=f"quick_{cat}"):
                                quiz_data = quiz_manager.generate_question(
                                    cat, quiz_type
                                )
                                if quiz_data:
                                    st.session_state["current_quiz"] = quiz_data
                                    st.rerun()

    with tab2:
        st.markdown("### 📊 Your Performance Dashboard")

        # Overall performance analysis
        display_performance_analysis(quiz_manager)

        stats = quiz_manager.get_statistics()

        if stats["total_questions"] > 0:
            # Performance charts
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 📈 Progress Overview")
                st.markdown(f"**Questions Attempted:** {stats['total_questions']}")
                st.markdown(f"**Correct Answers:** {stats['correct_answers']}")
                st.markdown(f"**Overall Accuracy:** {stats['accuracy']}%")
                st.markdown(f"**Best Streak:** {stats['best_streak']}")
                st.markdown(f"**Recent Accuracy:** {stats['recent_accuracy']}%")

            with col2:
                st.markdown("#### 🎯 Learning Insights")

                # Category performance (if available)
                quiz_state = quiz_manager.get_quiz_state()
                if quiz_state["questions_history"]:
                    st.markdown(f"**Words Practiced:** {stats['unique_words_seen']}")
                    st.markdown(
                        f"**Session Active:** {'Yes' if stats['session_started'] else 'No'}"
                    )

                # Performance trend
                if stats["recent_accuracy"] > stats["accuracy"]:
                    st.success("📈 Your performance is improving!")
                elif stats["recent_accuracy"] < stats["accuracy"]:
                    st.warning("📉 Recent performance needs attention")
                else:
                    st.info("📊 Your performance is consistent")

            # Detailed statistics
            with st.expander("📋 Detailed Statistics", expanded=False):
                st.json(
                    {
                        "Total Questions": stats["total_questions"],
                        "Correct Answers": stats["correct_answers"],
                        "Accuracy Percentage": f"{stats['accuracy']}%",
                        "Current Streak": stats["current_streak"],
                        "Best Streak": stats["best_streak"],
                        "Questions This Session": len(quiz_state["questions_history"]),
                        "Unique Words Seen": stats["unique_words_seen"],
                        "Most Missed Words": dict(stats["most_missed"][:5]),
                    }
                )

            # Export statistics
            if st.button("📥 Export Statistics"):
                export_data = quiz_manager.export_statistics()
                st.json(export_data)
                st.success(
                    "Statistics exported! Copy the JSON data above to save your progress."
                )

        else:
            st.info("Take some quizzes to see your performance statistics!")

    with tab3:
        st.markdown("### ⚙️ Quiz Settings & Preferences")

        # Difficulty settings
        st.markdown("#### 🎚️ Difficulty Settings")

        # Custom difficulty (placeholder for future implementation)
        difficulty_level = st.select_slider(
            "Choose difficulty level:",
            ["Beginner", "Intermediate", "Advanced"],
            value="Intermediate",
            help="Difficulty affects word complexity and question types",
        )

        # Time limits
        enable_timer = st.checkbox(
            "Enable time limit per question", help="Add time pressure to your quizzes"
        )

        if enable_timer:
            time_limit = st.slider("Time limit (seconds):", 10, 60, 30)
            st.info(f"Each question will have a {time_limit} second time limit")

        # Quiz preferences
        st.markdown("#### 🎛️ Quiz Preferences")

        show_hints = st.checkbox(
            "Show image hints when available",
            value=True,
            help="Display images related to quiz words as visual hints",
        )

        show_pronunciation = st.checkbox(
            "Show pronunciation guide",
            value=True,
            help="Display romanized pronunciation for Tigrinya words",
        )

        immediate_feedback = st.checkbox(
            "Show immediate feedback after each answer",
            value=True,
            help="Display correct answer and explanation after each question",
        )

        # Category weights
        st.markdown("#### 📊 Category Focus")

        st.markdown("Choose which categories to emphasize in quizzes:")

        category_weights = {}
        for category in VOCAB_CATEGORIES.keys():
            weight = st.slider(
                f"{category.title()}:",
                0,
                10,
                5,
                key=f"weight_{category}",
                help=f"Higher values increase likelihood of {category} words in quizzes",
            )
            category_weights[category] = weight

        # Save preferences
        if st.button("💾 Save Preferences"):
            # Store preferences in session state
            st.session_state["quiz_preferences"] = {
                "difficulty_level": difficulty_level,
                "enable_timer": enable_timer,
                "time_limit": time_limit if enable_timer else None,
                "show_hints": show_hints,
                "show_pronunciation": show_pronunciation,
                "immediate_feedback": immediate_feedback,
                "category_weights": category_weights,
            }
            st.success("Preferences saved for this session!")

        # Reset all data
        st.markdown("---")
        st.markdown("#### 🔄 Reset Options")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🗑️ Clear Quiz History", type="secondary"):
                if st.button("⚠️ Confirm Clear History"):
                    quiz_manager.reset_quiz()
                    st.success("Quiz history cleared!")
                    st.rerun()

        with col2:
            if st.button("🔧 Reset All Settings", type="secondary"):
                if st.button("⚠️ Confirm Reset Settings"):
                    # Clear preferences
                    if "quiz_preferences" in st.session_state:
                        del st.session_state["quiz_preferences"]
                    st.success("Settings reset to defaults!")
                    st.rerun()

    # Footer with quick statistics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    stats = quiz_manager.get_statistics()

    with col1:
        st.metric("Total Questions", stats["total_questions"])
    with col2:
        accuracy = stats["accuracy"] if stats["total_questions"] > 0 else 0
        st.metric("Accuracy", f"{accuracy:.1f}%")
    with col3:
        st.metric("Best Streak", stats["best_streak"])
    with col4:
        categories_used = len(
            set([quiz_manager.get_quiz_state().get("category", "all")])
        )
        st.metric("Categories Practiced", categories_used)


if __name__ == "__main__":
    render()
