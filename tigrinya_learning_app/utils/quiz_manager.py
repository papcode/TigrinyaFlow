"""
Quiz state management
"""

import random
from typing import Dict, List, Optional, Tuple

import streamlit as st

from utils.vocab_data import VOCAB_CATEGORIES, VOCAB_DICT


class QuizManager:
    """Manages quiz state and scoring"""

    def __init__(self):
        if "quiz_state" not in st.session_state:
            self.reset_quiz()

    def reset_quiz(self):
        """Reset quiz statistics"""
        st.session_state.quiz_state = {
            "score": 0,
            "total": 0,
            "current_streak": 0,
            "best_streak": 0,
            "current_question": None,
            "options": [],
            "correct_answer": "",
            "answered": False,
            "last_answer": None,
            "category": "all",
            "difficulty": "medium",
            "questions_history": [],
            "incorrect_words": [],
            "correct_words": [],
            "session_started": False,
        }

    def get_quiz_state(self) -> Dict:
        """Get current quiz state"""
        return st.session_state.quiz_state

    def update_score(self, is_correct: bool):
        """Update quiz scoring"""
        state = st.session_state.quiz_state
        state["total"] += 1

        if is_correct:
            state["score"] += 1
            state["current_streak"] += 1
            state["best_streak"] = max(state["best_streak"], state["current_streak"])
            state["correct_words"].append(state["current_question"])
        else:
            state["current_streak"] = 0
            state["incorrect_words"].append(state["current_question"])

    def generate_question(
        self, category: str = "all", quiz_type: str = "english_to_tigrinya"
    ) -> Dict:
        """Generate a new quiz question"""
        state = st.session_state.quiz_state

        # Select vocabulary based on category
        if category == "all":
            vocab_pool = VOCAB_DICT
        elif category in VOCAB_CATEGORIES:
            vocab_pool = VOCAB_CATEGORIES[category]
        else:
            vocab_pool = VOCAB_DICT

        if not vocab_pool:
            return None

        # Avoid repeating recent questions
        available_words = [
            word
            for word in vocab_pool.keys()
            if word not in state["questions_history"][-10:]  # Don't repeat last 10
        ]

        if not available_words:
            available_words = list(vocab_pool.keys())

        # Select random word
        correct_word = random.choice(available_words)
        correct_translation = vocab_pool[correct_word]

        # Generate options based on quiz type
        if quiz_type == "english_to_tigrinya":
            question = f"What is '{correct_word}' in Tigrinya?"
            correct_answer = correct_translation

            # Generate wrong options
            wrong_options = [
                translation
                for word, translation in vocab_pool.items()
                if word != correct_word
            ]
            options = random.sample(wrong_options, min(3, len(wrong_options)))
            options.append(correct_answer)

        else:  # tigrinya_to_english
            question = f"What does '{correct_translation}' mean in English?"
            correct_answer = correct_word

            # Generate wrong options
            wrong_options = [word for word in vocab_pool.keys() if word != correct_word]
            options = random.sample(wrong_options, min(3, len(wrong_options)))
            options.append(correct_answer)

        # Shuffle options
        random.shuffle(options)

        # Update state
        state["current_question"] = correct_word
        state["options"] = options
        state["correct_answer"] = correct_answer
        state["answered"] = False
        state["last_answer"] = None
        state["questions_history"].append(correct_word)
        state["session_started"] = True

        return {
            "question": question,
            "options": options,
            "correct_answer": correct_answer,
            "word": correct_word,
            "translation": correct_translation,
        }

    def submit_answer(self, selected_answer: str) -> Dict:
        """Process submitted answer"""
        state = st.session_state.quiz_state

        if state["answered"]:
            return {"error": "Question already answered"}

        is_correct = selected_answer == state["correct_answer"]
        self.update_score(is_correct)

        state["answered"] = True
        state["last_answer"] = selected_answer

        return {
            "is_correct": is_correct,
            "correct_answer": state["correct_answer"],
            "selected_answer": selected_answer,
            "score": state["score"],
            "total": state["total"],
            "current_streak": state["current_streak"],
        }

    def get_statistics(self) -> Dict:
        """Get comprehensive quiz statistics"""
        state = st.session_state.quiz_state

        if state["total"] == 0:
            return {
                "accuracy": 0,
                "total_questions": 0,
                "correct_answers": 0,
                "current_streak": 0,
                "best_streak": 0,
                "most_missed": [],
                "performance_trend": [],
            }

        accuracy = (state["score"] / state["total"]) * 100

        # Count most frequently missed words
        missed_counts = {}
        for word in state["incorrect_words"]:
            missed_counts[word] = missed_counts.get(word, 0) + 1

        most_missed = sorted(missed_counts.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]

        # Calculate performance trend (last 10 questions)
        recent_history = state["questions_history"][-10:]
        recent_correct = [
            word for word in recent_history if word in state["correct_words"]
        ]
        recent_accuracy = (
            (len(recent_correct) / len(recent_history)) * 100 if recent_history else 0
        )

        return {
            "accuracy": round(accuracy, 1),
            "total_questions": state["total"],
            "correct_answers": state["score"],
            "current_streak": state["current_streak"],
            "best_streak": state["best_streak"],
            "most_missed": most_missed,
            "recent_accuracy": round(recent_accuracy, 1),
            "questions_attempted": len(state["questions_history"]),
            "unique_words_seen": len(set(state["questions_history"])),
            "session_started": state["session_started"],
        }

    def get_performance_level(self) -> str:
        """Get performance level description"""
        stats = self.get_statistics()
        accuracy = stats["accuracy"]

        if accuracy >= 90:
            return "🌟 Excellent!"
        elif accuracy >= 80:
            return "🎯 Very Good!"
        elif accuracy >= 70:
            return "👍 Good!"
        elif accuracy >= 60:
            return "📈 Keep Practicing!"
        else:
            return "💪 Need More Practice!"

    def reset_session(self):
        """Reset only the current session while keeping overall stats"""
        state = st.session_state.quiz_state
        state.update(
            {
                "current_question": None,
                "options": [],
                "correct_answer": "",
                "answered": False,
                "last_answer": None,
                "current_streak": 0,
                "session_started": False,
            }
        )

    def export_statistics(self) -> Dict:
        """Export statistics for external use"""
        stats = self.get_statistics()
        state = st.session_state.quiz_state

        return {
            "quiz_stats": stats,
            "detailed_history": {
                "questions_history": state["questions_history"],
                "correct_words": state["correct_words"],
                "incorrect_words": state["incorrect_words"],
            },
            "settings": {
                "category": state["category"],
                "difficulty": state["difficulty"],
            },
        }

    def get_recommendation(self) -> str:
        """Get personalized learning recommendation"""
        stats = self.get_statistics()

        if stats["total_questions"] < 5:
            return "Take a few more questions to get personalized recommendations!"

        if stats["accuracy"] < 60:
            return "Focus on reviewing vocabulary cards before taking more quizzes."
        elif stats["current_streak"] < 3:
            return "Try to maintain focus and build your streak!"
        elif len(stats["most_missed"]) > 0:
            missed_word = stats["most_missed"][0][0]
            return f"Review the word '{missed_word}' - you've missed it {stats['most_missed'][0][1]} times."
        else:
            return "Great job! Try increasing difficulty or exploring new categories."
