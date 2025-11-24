"""
Pages package initialization
Imports all page modules for easy access
"""

from pages.search_page import render as search_page
from pages.browse_page import render as browse_page
from pages.alphabet_page import render as alphabet_page
from pages.drag_drop_page import render as drag_drop_page
from pages.quiz_page import render as quiz_page
from pages.statistics_page import render as statistics_page

__all__ = [
    'search_page',
    'browse_page',
    'alphabet_page',
    'drag_drop_page',
    'quiz_page',
    'statistics_page'
]
