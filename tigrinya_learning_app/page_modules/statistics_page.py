"""
Statistics page module
Provides comprehensive learning analytics and progress tracking
"""

from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.quiz_manager import QuizManager
from utils.vocab_data import VOCAB_CATEGORIES, VOCAB_DICT, VOCAB_STATS

from clientTranslation import geez_to_latin_syllable


def get_session_stats():
    """Get statistics from all session data"""
    stats = {
        "total_searches": st.session_state.get("search_count", 0),
        "browse_sessions": st.session_state.get("browse_sessions", 0),
        "practice_words": len(st.session_state.get("practice_words", [])),
        "drag_drop_stats": st.session_state.get("drag_drop_state", {}),
        "quiz_stats": QuizManager().get_statistics(),
    }
    return stats


def create_progress_chart(quiz_stats):
    """Create progress visualization chart"""
    if quiz_stats["total_questions"] == 0:
        return None

    # Create sample progress data (in real app, this would come from stored history)
    dates = [datetime.now() - timedelta(days=x) for x in range(7, 0, -1)]
    daily_accuracy = [
        max(0, quiz_stats["accuracy"] + (i % 3 - 1) * 10)  # Simulate variation
        for i in range(7)
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=daily_accuracy,
            mode="lines+markers",
            name="Daily Accuracy",
            line=dict(color="#667eea", width=3),
            marker=dict(size=8, color="#667eea"),
        )
    )

    fig.update_layout(
        title="Learning Progress Over Time",
        xaxis_title="Date",
        yaxis_title="Accuracy (%)",
        height=400,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_category_performance_chart(quiz_stats):
    """Create category performance visualization"""
    # Sample category performance data
    categories = list(VOCAB_CATEGORIES.keys())[:6]
    performance = [
        quiz_stats["accuracy"] + (i % 4 - 2) * 5 for i in range(len(categories))
    ]

    fig = px.bar(
        x=categories,
        y=performance,
        title="Performance by Category",
        color=performance,
        color_continuous_scale="RdYlBu",
    )

    fig.update_layout(
        height=400,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def display_achievement_badges(quiz_stats):
    """Display achievement badges based on performance"""
    achievements = []

    # Define achievements
    if quiz_stats["total_questions"] >= 10:
        achievements.append(("🎯", "Quiz Master", "Answered 10+ questions"))

    if quiz_stats["best_streak"] >= 5:
        achievements.append(("🔥", "Streak Master", "5+ correct answers in a row"))

    if quiz_stats["accuracy"] >= 80:
        achievements.append(("🌟", "Accuracy Star", "80%+ accuracy rate"))

    if quiz_stats["accuracy"] >= 90:
        achievements.append(("💎", "Perfectionist", "90%+ accuracy rate"))

    if quiz_stats["unique_words_seen"] >= 25:
        achievements.append(("📚", "Vocabulary Explorer", "Practiced 25+ unique words"))

    if len(achievements) == 0:
        achievements.append(("🚀", "Getting Started", "Begin your learning journey"))

    # Display achievements
    st.markdown("### 🏆 Achievements")

    cols = st.columns(min(len(achievements), 4))
    for i, (emoji, title, description) in enumerate(achievements):
        with cols[i % 4]:
            st.markdown(
                f"""
            <div style='
                background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                margin: 10px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            '>
                <div style='font-size: 2.5em; margin-bottom: 10px;'>{emoji}</div>
                <div style='font-weight: bold; color: #2d3436;'>{title}</div>
                <div style='font-size: 0.9em; color: #636e72; margin-top: 5px;'>{description}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )


def display_learning_insights(session_stats):
    """Display personalized learning insights"""
    quiz_stats = session_stats["quiz_stats"]

    insights = []

    # Generate insights based on data
    if quiz_stats["total_questions"] > 0:
        if quiz_stats["accuracy"] < 60:
            insights.append(
                "🎯 Focus on reviewing vocabulary cards before taking quizzes"
            )
        elif quiz_stats["accuracy"] > 85:
            insights.append("🌟 Excellent performance! Try more challenging categories")

        if quiz_stats["current_streak"] < 3:
            insights.append("🔥 Work on building longer answer streaks")

        if len(quiz_stats["most_missed"]) > 0:
            most_missed = quiz_stats["most_missed"][0][0]
            insights.append(
                f"📝 Review the word '{most_missed}' - it needs more practice"
            )

    if session_stats["practice_words"] > 10:
        insights.append("💪 Great job building your practice word collection!")

    if session_stats["browse_sessions"] > 5:
        insights.append("🔍 You're actively exploring vocabulary - keep it up!")

    # Default insight
    if not insights:
        insights.append(
            "🚀 Start exploring vocabulary and taking quizzes to get personalized insights!"
        )

    # Display insights
    st.markdown("### 💡 Learning Insights")
    for insight in insights:
        st.info(insight)


def create_vocabulary_mastery_overview():
    """Create vocabulary mastery overview"""
    st.markdown("### 📊 Vocabulary Mastery Overview")

    # Display category progress
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 📚 Category Coverage")
        for category, words in VOCAB_CATEGORIES.items():
            total_words = len(words)
            # Simulate learning progress
            learned_words = min(
                total_words, max(0, total_words // 3 + (hash(category) % 5))
            )
            progress = learned_words / total_words if total_words > 0 else 0

            st.markdown(f"**{category.title()}**")
            st.progress(progress)
            st.caption(f"{learned_words}/{total_words} words ({progress * 100:.0f}%)")

    with col2:
        st.markdown("#### 🎯 Learning Priorities")

        # Recommend categories to focus on
        priorities = [
            ("greetings", "Essential for communication"),
            ("numbers", "Foundation for counting"),
            ("family", "Common in daily conversation"),
            ("colors", "Descriptive vocabulary"),
            ("food", "Daily life essentials"),
        ]

        for category, reason in priorities:
            if category in VOCAB_CATEGORIES:
                word_count = len(VOCAB_CATEGORIES[category])
                st.markdown(f"• **{category.title()}** ({word_count} words) - {reason}")


def display_study_recommendations():
    """Display personalized study recommendations"""
    st.markdown("### 📝 Study Recommendations")

    session_stats = get_session_stats()
    quiz_stats = session_stats["quiz_stats"]

    recommendations = []

    # Generate recommendations
    if quiz_stats["total_questions"] < 5:
        recommendations.append(
            {
                "title": "🎯 Take Your First Quiz",
                "description": 'Start with a simple category like "greetings" or "colors"',
                "action": "Go to Quiz Mode",
                "priority": "high",
            }
        )

    if session_stats["practice_words"] == 0:
        recommendations.append(
            {
                "title": "📚 Build Practice Collection",
                "description": "Browse vocabulary and add interesting words to your practice session",
                "action": "Browse Vocabulary",
                "priority": "medium",
            }
        )

    if quiz_stats["accuracy"] < 70 and quiz_stats["total_questions"] > 5:
        recommendations.append(
            {
                "title": "📖 Review Vocabulary Cards",
                "description": "Spend more time studying words before taking quizzes",
                "action": "Search & Study",
                "priority": "high",
            }
        )

    if quiz_stats["best_streak"] < 3:
        recommendations.append(
            {
                "title": "🔥 Build Consistency",
                "description": "Focus on accuracy over speed to build longer streaks",
                "action": "Practice Daily",
                "priority": "medium",
            }
        )

    recommendations.append(
        {
            "title": "✍️ Learn the Alphabet",
            "description": "Understanding Geʽez characters will improve your reading",
            "action": "Alphabet Practice",
            "priority": "low",
        }
    )

    # Display recommendations
    for rec in recommendations:
        priority_color = {"high": "#ff7675", "medium": "#fdcb6e", "low": "#74b9ff"}

        color = priority_color.get(rec["priority"], "#74b9ff")

        st.markdown(
            f"""
        <div style='
            background: {color}20;
            border-left: 4px solid {color};
            padding: 15px;
            margin: 10px 0;
            border-radius: 0 10px 10px 0;
        '>
            <h4 style='margin: 0; color: {color};'>{rec["title"]}</h4>
            <p style='margin: 5px 0; color: #2d3436;'>{rec["description"]}</p>
            <small style='color: #636e72;'>👉 {rec["action"]}</small>
        </div>
        """,
            unsafe_allow_html=True,
        )


def render():
    """Main render function for statistics page"""
    st.subheader("📊 Learning Statistics & Progress")

    # Get all session statistics
    session_stats = get_session_stats()
    quiz_stats = session_stats["quiz_stats"]

    # Overview metrics
    st.markdown("### 🎯 Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Quiz Questions", quiz_stats["total_questions"])
    with col2:
        accuracy = quiz_stats["accuracy"] if quiz_stats["total_questions"] > 0 else 0
        st.metric("Quiz Accuracy", f"{accuracy:.1f}%")
    with col3:
        st.metric("Words Practiced", quiz_stats["unique_words_seen"])
    with col4:
        st.metric("Search Count", session_stats["total_searches"])

    # Create tabs for different statistics views
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Progress", "🏆 Achievements", "📚 Vocabulary", "🎯 Recommendations"]
    )

    with tab1:
        st.markdown("### 📈 Learning Progress")

        if quiz_stats["total_questions"] > 0:
            # Progress charts
            col1, col2 = st.columns(2)

            with col1:
                progress_fig = create_progress_chart(quiz_stats)
                if progress_fig:
                    st.plotly_chart(progress_fig, use_container_width=True)

            with col2:
                category_fig = create_category_performance_chart(quiz_stats)
                if category_fig:
                    st.plotly_chart(category_fig, use_container_width=True)

            # Detailed progress metrics
            st.markdown("#### 📊 Detailed Metrics")

            progress_col1, progress_col2 = st.columns(2)

            with progress_col1:
                st.markdown("**Quiz Performance:**")
                st.write(f"• Total Questions: {quiz_stats['total_questions']}")
                st.write(f"• Correct Answers: {quiz_stats['correct_answers']}")
                st.write(f"• Current Streak: {quiz_stats['current_streak']}")
                st.write(f"• Best Streak: {quiz_stats['best_streak']}")
                st.write(f"• Recent Accuracy: {quiz_stats['recent_accuracy']:.1f}%")

            with progress_col2:
                st.markdown("**Session Activity:**")
                st.write(f"• Vocabulary Searches: {session_stats['total_searches']}")
                st.write(f"• Browse Sessions: {session_stats['browse_sessions']}")
                st.write(f"• Practice Words: {session_stats['practice_words']}")

                # Drag & Drop stats if available
                drag_stats = session_stats["drag_drop_stats"]
                if drag_stats and drag_stats.get("total_count", 0) > 0:
                    accuracy = (
                        drag_stats["correct_count"] / drag_stats["total_count"]
                    ) * 100
                    st.write(f"• Drag & Drop Accuracy: {accuracy:.1f}%")

            # Learning insights
            display_learning_insights(session_stats)

        else:
            st.info(
                "Start taking quizzes to see your progress charts and detailed analytics!"
            )

            # Show vocabulary overview instead
            st.markdown("#### 📚 Available Learning Content")
            overview_col1, overview_col2, overview_col3 = st.columns(3)

            with overview_col1:
                st.metric("Total Words", VOCAB_STATS["total_words"])
            with overview_col2:
                st.metric("Categories", VOCAB_STATS["total_categories"])
            with overview_col3:
                st.metric("Common Phrases", VOCAB_STATS["total_phrases"])

    with tab2:
        # Display achievements
        display_achievement_badges(quiz_stats)

        # Learning milestones
        st.markdown("### 🎯 Learning Milestones")

        milestones = [
            (5, "First Quiz Taker", "Complete your first 5 quiz questions"),
            (25, "Vocabulary Explorer", "Practice 25 different words"),
            (50, "Dedicated Learner", "Answer 50 quiz questions"),
            (10, "Streak Builder", "Achieve a 10-question correct streak"),
            (100, "Quiz Master", "Complete 100 quiz questions"),
            (90, "Accuracy Expert", "Maintain 90%+ accuracy over 20 questions"),
        ]

        for threshold, title, description in milestones:
            if title == "Accuracy Expert":
                achieved = (
                    quiz_stats["accuracy"] >= 90 and quiz_stats["total_questions"] >= 20
                )
                progress = (
                    min(100, quiz_stats["accuracy"])
                    if quiz_stats["total_questions"] >= 20
                    else 0
                )
            elif title == "Streak Builder":
                achieved = quiz_stats["best_streak"] >= threshold
                progress = min(100, (quiz_stats["best_streak"] / threshold) * 100)
            elif title == "Vocabulary Explorer":
                achieved = quiz_stats["unique_words_seen"] >= threshold
                progress = min(100, (quiz_stats["unique_words_seen"] / threshold) * 100)
            else:
                achieved = quiz_stats["total_questions"] >= threshold
                progress = min(100, (quiz_stats["total_questions"] / threshold) * 100)

            status = "✅" if achieved else "🎯"

            st.markdown(
                f"""
            <div style='
                background: {"linear-gradient(135deg, #00b894 0%, #00cec9 100%)" if achieved else "linear-gradient(135deg, #ddd 0%, #bbb 100%)"};
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                color: white;
            '>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h4 style='margin: 0;'>{status} {title}</h4>
                        <p style='margin: 5px 0;'>{description}</p>
                    </div>
                    <div style='font-size: 1.2em; font-weight: bold;'>
                        {progress:.0f}%
                    </div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with tab3:
        # Vocabulary mastery overview
        create_vocabulary_mastery_overview()

        # Most practiced words
        if quiz_stats["total_questions"] > 0:
            st.markdown("### 🔄 Most Practiced")

            # Get words from quiz history (simulated)
            if quiz_stats.get("questions_history"):
                from collections import Counter

                word_counts = Counter(
                    quiz_stats["questions_history"][-20:]
                )  # Last 20 questions
                most_common = word_counts.most_common(5)

                if most_common:
                    for word, count in most_common:
                        if word in VOCAB_DICT:
                            translation = VOCAB_DICT[word]
                            phonetic = geez_to_latin_syllable(translation)

                            st.markdown(
                                f"""
                            <div style='
                                background: linear-gradient(135deg, #a29bfe 0%, #6c5ce7 100%);
                                padding: 15px;
                                border-radius: 10px;
                                color: white;
                                margin: 10px 0;
                                display: flex;
                                justify-content: space-between;
                                align-items: center;
                            '>
                                <div>
                                    <strong>{word}</strong> → {translation} ({phonetic})
                                </div>
                                <div style='
                                    background: rgba(255,255,255,0.2);
                                    padding: 5px 15px;
                                    border-radius: 20px;
                                    font-weight: bold;
                                '>
                                    {count}x
                                </div>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

        # Words that need more practice
        if quiz_stats.get("most_missed"):
            st.markdown("### 🎯 Words Needing Practice")

            for word, miss_count in quiz_stats["most_missed"][:3]:
                if word in VOCAB_DICT:
                    translation = VOCAB_DICT[word]
                    phonetic = geez_to_latin_syllable(translation)

                    st.markdown(
                        f"""
                    <div style='
                        background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%);
                        padding: 15px;
                        border-radius: 10px;
                        color: white;
                        margin: 10px 0;
                    '>
                        <strong>{word}</strong> → {translation} ({phonetic})
                        <br><small>Missed {miss_count} time{"s" if miss_count > 1 else ""}</small>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

    with tab4:
        # Study recommendations
        display_study_recommendations()

        # Learning schedule suggestion
        st.markdown("### 📅 Suggested Learning Schedule")

        schedule = [
            ("Monday", "🔤", "Alphabet Practice", "15 minutes learning new characters"),
            (
                "Tuesday",
                "📚",
                "Vocabulary Building",
                "Browse and add 10 new words to practice",
            ),
            ("Wednesday", "🎯", "Quiz Day", "Take quizzes in 2-3 different categories"),
            ("Thursday", "🔄", "Review Session", "Practice words you've missed before"),
            (
                "Friday",
                "🎮",
                "Fun Practice",
                "Drag & drop games and interactive activities",
            ),
            (
                "Saturday",
                "📖",
                "Reading Practice",
                "Try to read simple Tigrinya words/phrases",
            ),
            (
                "Sunday",
                "📊",
                "Progress Review",
                "Check your statistics and plan next week",
            ),
        ]

        for day, emoji, activity, description in schedule:
            st.markdown(
                f"""
            <div style='
                background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
                padding: 15px;
                border-radius: 10px;
                color: white;
                margin: 10px 0;
            '>
                <div style='display: flex; align-items: center; gap: 15px;'>
                    <div style='font-size: 2em;'>{emoji}</div>
                    <div>
                        <h4 style='margin: 0;'>{day}: {activity}</h4>
                        <p style='margin: 5px 0; opacity: 0.9;'>{description}</p>
                    </div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Learning tips
        st.markdown("### 💡 Learning Tips")
        tips = [
            "🕐 **Consistency over intensity** - 15 minutes daily beats 2 hours weekly",
            "🎯 **Set specific goals** - Aim for 80% accuracy before moving to harder categories",
            "📝 **Use multiple methods** - Combine reading, writing, and audio practice",
            "🔄 **Review regularly** - Revisit words you've learned to strengthen memory",
            "🎉 **Celebrate progress** - Acknowledge your achievements, no matter how small",
            "👥 **Practice with others** - Find language partners or study groups",
        ]

        for tip in tips:
            st.markdown(tip)

    # Footer with export options
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("📥 Export Progress Data"):
            export_data = {
                "session_stats": session_stats,
                "export_date": datetime.now().isoformat(),
                "vocab_stats": VOCAB_STATS,
            }
            st.json(export_data)

    with col2:
        if st.button("🔄 Reset All Statistics"):
            if st.button("⚠️ Confirm Reset", key="confirm_reset"):
                # Reset quiz statistics
                QuizManager().reset_quiz()
                # Reset other session data
                for key in [
                    "search_count",
                    "browse_sessions",
                    "practice_words",
                    "drag_drop_state",
                ]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.success("All statistics have been reset!")
                st.rerun()

    with col3:
        st.markdown("**Last Updated:** " + datetime.now().strftime("%Y-%m-%d %H:%M"))


if __name__ == "__main__":
    render()
