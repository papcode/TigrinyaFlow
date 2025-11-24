"""
Centralized vocabulary data
"""

# Enhanced vocabulary dictionary with categories
VOCAB_CATEGORIES = {
    "colors": {
        "red": "ቀይሕ", "blue": "ሰማያዊ", "green": "ቀጠልያ", "yellow": "ቢጫ",
        "black": "ጸሊም", "white": "ጻዕዳ", "orange": "ኣራንቾ", 
        "purple": "ሊላ", "brown": "ቡናዊ"
    },
    "animals": {
        "dog": "ከልቢ", "cat": "ድሙ", "cow": "ላም", "lion": "ኣንበሳ",
        "horse": "ፍረስ", "goat": "ጤል", "chicken": "ዶሮ", "fish": "ዓሳ",
        # ... more animals
    },
    "objects": {
        "book": "መጽሓፍ", "pen": "ብርዒ", "chair": "ኩርስ", "table": "ጣውላ",
        # ... more objects
    }
}

# Flatten vocabulary for easy access
VOCAB_DICT = {}
for category, words in VOCAB_CATEGORIES.items():
    VOCAB_DICT.update(words)
