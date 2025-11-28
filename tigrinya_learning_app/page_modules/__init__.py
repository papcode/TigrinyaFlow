"""
Pages package initialization
Imports all page modules for easy access
"""

from page_modules.alphabet_page import render as alphabet_page
from page_modules.browse_page import render as browse_page
from page_modules.connection_game_page import render as match_exercise_page
from page_modules.enhanced_drag_drop_page import render as drag_drop_page
from page_modules.quiz_page import render as quiz_page
from page_modules.search_page import render as search_page
from page_modules.statistics_page import render as statistics_page

__all__ = [
    "search_page",
    "browse_page",
    "alphabet_page",
    "match_exercise_page",
    "drag_drop_page",
    "quiz_page",
    "statistics_page",
]
