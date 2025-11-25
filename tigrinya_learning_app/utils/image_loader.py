"""
Image loading utilities with caching
"""

import base64
import os
from io import BytesIO
from typing import Optional

import requests
import streamlit as st
from PIL import Image
from utils.vocab_data import VOCAB_CATEGORIES


class ImageLoader:
    """Handles image loading from various sources"""

    def __init__(self, images_folder: str = "images"):
        self.images_folder = images_folder
        self.unsplash_access_key = "YOUR_UNSPLASH_ACCESS_KEY"  # Replace with actual key

    @st.cache_data
    def get_local_image(_self, word: str) -> Optional[bytes]:
        """Load image from local folder"""
        try:
            # Find which category the word belongs to
            word_category = None
            for category, words in VOCAB_CATEGORIES.items():
                if word.lower() in words:
                    word_category = category
                    break

            extensions = [".jpg", ".jpeg", ".png", ".webp", ".gif"]

            # If category is found, search in the category folder first
            if word_category:
                for ext in extensions:
                    image_path = os.path.join(
                        _self.images_folder, "vocabulary", word_category, f"{word.lower()}{ext}"
                    )
                    if os.path.exists(image_path):
                        with open(image_path, "rb") as file:
                            return file.read()

            # Fallback to original search logic
            for ext in extensions:
                image_path = os.path.join(_self.images_folder, f"{word.lower()}{ext}")
                if os.path.exists(image_path):
                    with open(image_path, "rb") as file:
                        return file.read()

            # Try with different naming conventions
            for ext in extensions:
                image_path = os.path.join(
                    _self.images_folder, f"{word.replace(' ', '_').lower()}{ext}"
                )
                if os.path.exists(image_path):
                    with open(image_path, "rb") as file:
                        return file.read()

            return None

        except Exception as e:
            st.error(f"Error loading local image for '{word}': {str(e)}")
            return None

    @st.cache_data
    def get_unsplash_image(_self, query: str) -> Optional[bytes]:
        """Fetch image from Unsplash"""
        try:
            if _self.unsplash_access_key == "YOUR_UNSPLASH_ACCESS_KEY":
                return None

            url = "https://api.unsplash.com/search/photos"
            headers = {"Authorization": f"Client-ID {_self.unsplash_access_key}"}
            params = {"query": query, "per_page": 1, "orientation": "squarish"}

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data["results"]:
                    photo_url = data["results"][0]["urls"]["regular"]

                    # Download the image
                    img_response = requests.get(photo_url, timeout=10)
                    if img_response.status_code == 200:
                        # Resize image for better performance
                        img = Image.open(BytesIO(img_response.content))
                        img.thumbnail((400, 400), Image.Resampling.LANCZOS)

                        # Convert back to bytes
                        img_bytes = BytesIO()
                        img.save(img_bytes, format="JPEG", quality=85)
                        return img_bytes.getvalue()

            return None

        except Exception as e:
            st.error(f"Error fetching image from Unsplash for '{query}': {str(e)}")
            return None

    def get_image(self, word: str) -> Optional[bytes]:
        """Get image from local first, then Unsplash"""
        # Try local first
        image = self.get_local_image(word)
        if image:
            return image

        # Fallback to Unsplash
        return self.get_unsplash_image(word)

    @st.cache_data
    def get_base64_image(_self, image_path: str) -> Optional[str]:
        """Convert image to base64 for HTML embedding"""
        try:
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    return base64.b64encode(img_file.read()).decode()
            return None
        except Exception as e:
            st.error(f"Error converting image to base64: {str(e)}")
            return None

    def display_image_with_caption(self, word: str, translation: str, phonetic: str):
        """Display image with styled caption"""
        image = self.get_image(word)
        if image:
            st.image(image, width='stretch')
            st.markdown(
                f"""
            <div style='
                text-align: center;
                font-size: 1.4em;
                font-weight: bold;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.2);
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            '>
                {word.title()} - {translation} - ({phonetic})
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.info(f"No image available for '{word}'")
            st.markdown(
                f"""
            <div style='
                text-align: center;
                font-size: 1.4em;
                font-weight: bold;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin-top: 10px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.2);
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            '>
                {word.title()} - {translation} - ({phonetic})
            </div>
            """,
                unsafe_allow_html=True,
            )
