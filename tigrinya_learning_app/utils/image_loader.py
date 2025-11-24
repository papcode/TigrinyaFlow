"""
Image loading utilities with caching
"""

import streamlit as st
import os
import requests
from typing import Optional

class ImageLoader:
    """Handles image loading from various sources"""
    
    def __init__(self, images_folder: str = "images"):
        self.images_folder = images_folder
    
    @st.cache_data
    def get_local_image(_self, word: str) -> Optional[bytes]:
        """Load image from local folder"""
        # Implementation from original code
        pass
    
    @st.cache_data
    def get_unsplash_image(_self, query: str) -> Optional[bytes]:
        """Fetch image from Unsplash"""
        # Implementation from original code
        pass
