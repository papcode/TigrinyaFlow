"""
Main Streamlit App - Modularized Version
This is the entry point that imports all page modules
"""

import base64

import streamlit as st

# Import page modules
from page_modules import (
    alphabet_page,
    browse_page,
    drag_drop_page,
    match_exercise_page,
    quiz_page,
    search_page,
    statistics_page,
)


def main():
    # Page configuration
    st.set_page_config(
        page_title="Tigrinya Vocabulary Learning App",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS for better styling
    st.markdown(
        """
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton > button {
        font-family: 'Noto Sans Ethiopic', serif;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    # Header with logo
    try:

        def get_base64_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()

        img_base64 = get_base64_image("tigrinya_learning_app/images/logo.png")

        st.markdown(
            f"""
            <h1 style='display: flex; align-items: center; gap: 10px;'>
                <img src='data:image/png;base64,{img_base64}' width='40'>
                English—Tigrinya Vocabulary Learning App
            </h1>
            """,
            unsafe_allow_html=True,
        )
    except:
        st.title("📚 English—Tigrinya Vocabulary Learning App")

    # Sidebar navigation
    st.sidebar.title("Navigation")
    st.sidebar.markdown("Choose a learning mode:")

    page = st.sidebar.radio(
        "Navigation",  # Shorter label since it's hidden anyway
        [
            "🔍 Search Translation",
            "📚 Browse Vocabulary",
            "✍️ ፊደላት (Alphabets)",
            "🎮 Drag & Drop",
            "🔗 Match the Following",
            "🎯 Quiz Mode",
            "📊 Statistics",
        ],
        label_visibility="collapsed",
    )

    # Page routing
    if page == "🔍 Search Translation":
        search_page()
    elif page == "📚 Browse Vocabulary":
        browse_page()
    elif page == "✍️ ፊደላት (Alphabets)":
        alphabet_page()
    elif page == "🎮 Drag & Drop":
        drag_drop_page()
    elif page == "🔗 Match the Following":
        match_exercise_page()
    elif page == "🎯 Quiz Mode":
        quiz_page()
    elif page == "📊 Statistics":
        statistics_page()

    # Sidebar information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💡 Tips")
    st.sidebar.info(
        "• Use the search to find specific words\n"
        "• Browse vocabulary by category\n"
        "• Click alphabet characters for handwriting animations\n"
        "• Play drag & drop to practice word building\n"
        "• Match images with Tigrinya text labels\n"
        "• Take quizzes to test your knowledge\n"
        "• Check statistics to track progress"
    )

    # Sidebar quick stats
    if "quiz_state" in st.session_state:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📈 Quick Stats")
        quiz_stats = st.session_state.quiz_state
        if quiz_stats["total"] > 0:
            accuracy = (quiz_stats["score"] / quiz_stats["total"]) * 100
            st.sidebar.metric("Quiz Accuracy", f"{accuracy:.0f}%")
            st.sidebar.metric("Best Streak", quiz_stats["best_streak"])

    if "drag_drop_state" in st.session_state:
        drag_stats = st.session_state.drag_drop_state
        if drag_stats["total_count"] > 0:
            accuracy = (drag_stats["correct_count"] / drag_stats["total_count"]) * 100
            st.sidebar.metric("Drag & Drop Accuracy", f"{accuracy:.0f}%")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "Built with ❤️ using Streamlit | Enhanced with interactive learning features"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()