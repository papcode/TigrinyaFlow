"""
Matching exercise logic for connecting images with Tigrinya text labels
"""

import base64
import os
import random
from typing import Dict, List, Tuple

import streamlit as st

from utils.vocab_data import VOCAB_CATEGORIES


class ConnectionGame:
    """Manages matching exercises for connecting images with Tigrinya text"""

    def __init__(self):
        if "connection_game_state" not in st.session_state:
            self.reset_exercise()

    def reset_exercise(self):
        """Reset exercise state"""
        st.session_state.connection_game_state = {
            "connections": {},  # image_id -> text_id mapping
            "correct_answers": {},  # correct image_id -> text_id mapping
            "score": 0,
            "total_questions": 0,
            "current_round": 1,
            "exercise_complete": False,
            "feedback_shown": False,
            "selected_image": None,
            "selected_text": None,
            "force_new_puzzle": True,  # Flag to force new puzzle generation
        }

    def get_image_base64(self, image_path: str) -> str:
        """Convert image to base64 for embedding in HTML"""
        try:
            # Try multiple possible paths
            possible_paths = [
                image_path,  # Direct path
                f"tigrinya_learning_app/{image_path}",  # Relative to project root
                f"C:\\WORKSPACE\\AMAL\\trigano\\tigrinya_learning_app\\{image_path}",  # Absolute path
                os.path.join(
                    os.path.dirname(__file__), "..", image_path
                ),  # Relative to utils
            ]

            for full_path in possible_paths:
                if os.path.exists(full_path):
                    with open(full_path, "rb") as img_file:
                        return base64.b64encode(img_file.read()).decode()

            return ""
        except Exception as e:
            print(f"Error loading image {image_path}: {e}")
            return ""

    def generate_puzzle(self, category: str = "animals", count: int = 5) -> Dict:
        """Generate a new puzzle with images and shuffled text labels"""

        # Get vocabulary for the category
        if category not in VOCAB_CATEGORIES:
            category = "animals"  # fallback

        vocab = VOCAB_CATEGORIES[category]

        # Select random words that have corresponding images
        available_words = []

        # Base paths to try
        base_paths = [
            os.path.join(
                os.path.dirname(__file__), "..", "images", "vocabulary", category
            ),
            f"tigrinya_learning_app/images/vocabulary/{category}",
            f"C:\\WORKSPACE\\AMAL\\trigano\\tigrinya_learning_app\\images\\vocabulary\\{category}",
        ]

        for english_word, tigrinya_word in vocab.items():
            image_found = False

            # Try different extensions and paths
            for ext in ["jpeg", "jpg", "png", "gif"]:
                filename = f"{english_word}.{ext}"

                for base_path in base_paths:
                    full_path = os.path.join(base_path, filename)
                    if os.path.exists(full_path):
                        # Store relative path for consistency
                        relative_path = f"images/vocabulary/{category}/{filename}"
                        available_words.append(
                            (english_word, tigrinya_word, relative_path)
                        )
                        image_found = True
                        break

                if image_found:
                    break

        if len(available_words) < count:
            count = min(len(available_words), count)

        # Select random subset
        selected_words = random.sample(available_words, count)

        # Prepare puzzle data
        puzzle = {
            "category": category,
            "images": [],
            "texts": [],
            "correct_answers": {},
        }

        # Create image list
        for i, (english_word, tigrinya_word, image_path) in enumerate(selected_words):
            image_id = f"img_{i}"
            text_id = f"text_{i}"

            puzzle["images"].append(
                {
                    "id": image_id,
                    "english": english_word,
                    "image_path": image_path,
                    "image_base64": self.get_image_base64(image_path),
                }
            )

            puzzle["texts"].append(
                {
                    "id": text_id,
                    "tigrinya": tigrinya_word,
                    "english": english_word,  # for verification
                }
            )

            puzzle["correct_answers"][image_id] = text_id

        # Shuffle the text labels
        random.shuffle(puzzle["texts"])

        # Store correct answers in session state
        st.session_state.connection_game_state["correct_answers"] = puzzle[
            "correct_answers"
        ]
        st.session_state.connection_game_state["total_questions"] = count
        st.session_state.connection_game_state["connections"] = {}
        st.session_state.connection_game_state["exercise_complete"] = False
        st.session_state.connection_game_state["feedback_shown"] = False
        st.session_state.connection_game_state["force_new_puzzle"] = False

        return puzzle

    def check_connections(self) -> Dict:
        """Check all connections and return results"""
        state = st.session_state.connection_game_state
        connections = state["connections"]
        correct_answers = state["correct_answers"]

        results = {
            "correct": 0,
            "total": len(correct_answers),
            "details": {},
            "all_connected": len(connections) == len(correct_answers),
        }

        for image_id, text_id in connections.items():
            is_correct = correct_answers.get(image_id) == text_id
            results["details"][image_id] = {
                "connected_to": text_id,
                "correct": is_correct,
            }
            if is_correct:
                results["correct"] += 1

        # Update score
        if results["all_connected"]:
            state["score"] = results["correct"]
            state["exercise_complete"] = True

        return results

    def add_connection(self, image_id: str, text_id: str):
        """Add a connection between image and text"""
        st.session_state.connection_game_state["connections"][image_id] = text_id

    def remove_connection(self, image_id: str):
        """Remove a connection"""
        if image_id in st.session_state.connection_game_state["connections"]:
            del st.session_state.connection_game_state["connections"][image_id]

    def get_statistics(self) -> Dict:
        """Get exercise statistics"""
        state = st.session_state.connection_game_state
        return {
            "current_score": state["score"],
            "total_questions": state["total_questions"],
            "current_round": state["current_round"],
            "exercise_complete": state["exercise_complete"],
            "force_new_puzzle": state.get("force_new_puzzle", False),
        }

    def should_generate_new_puzzle(self) -> bool:
        """Check if a new puzzle should be generated"""
        return st.session_state.connection_game_state.get("force_new_puzzle", False)

    def increment_round(self):
        """Increment the current round number"""
        st.session_state.connection_game_state["current_round"] += 1

    def get_available_categories(self) -> List[str]:
        """Get list of available categories that have images"""
        categories = []

        # Try multiple possible base paths
        possible_base_paths = [
            os.path.join(os.path.dirname(__file__), "..", "images", "vocabulary"),
            "tigrinya_learning_app/images/vocabulary",
            "C:\\WORKSPACE\\AMAL\\trigano\\trigrinya_learning_app\\images\\vocabulary",
        ]

        for base_path in possible_base_paths:
            if os.path.exists(base_path):
                try:
                    for category in os.listdir(base_path):
                        category_path = os.path.join(base_path, category)
                        if (
                            os.path.isdir(category_path)
                            and category in VOCAB_CATEGORIES
                        ):
                            # Check if category has images
                            image_files = [
                                f
                                for f in os.listdir(category_path)
                                if f.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))
                            ]
                            if image_files and category not in categories:
                                categories.append(category)
                except Exception as e:
                    print(f"Error accessing {base_path}: {e}")
                    continue

                # If we found categories, break
                if categories:
                    break

        return categories if categories else ["animals"]  # fallback
