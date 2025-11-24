"""
Centralized vocabulary data with comprehensive categories
"""

# Enhanced vocabulary dictionary with extensive categories
VOCAB_CATEGORIES = {
    "colors": {
        "red": "ቀይሕ",
        "blue": "ሰማያዊ",
        "green": "ቀጠልያ",
        "yellow": "ቢጫ",
        "black": "ጸሊም",
        "white": "ጻዕዳ",
        "orange": "ኣራንቾ",
        "purple": "ሊላ",
        "brown": "ቡናዊ",
        "gray": "ሓመድ",
        "pink": "ሮዛ",
        "silver": "ብሩር",
        "gold": "ወርቂ",
    },
    "animals": {
        "dog": "ከልቢ",
        "cat": "ድሙ",
        "cow": "ላም",
        "lion": "ኣንበሳ",
        "horse": "ፍረስ",
        "goat": "ጤል",
        "chicken": "ዶሮ",
        "fish": "ዓሳ",
        "bird": "ዑፍ",
        "elephant": "ሓሳዊ",
        "monkey": "ድርኺ",
        "rabbit": "ማንቲለ",
        "sheep": "በጊዕ",
        "camel": "ገመል",
        "donkey": "ኣድጊ",
        "pig": "ሓዝ",
        "snake": "ተመን",
        "leopard": "ነብሪ",
        "deer": "ምድሪ ጥቢ",
        "bear": "ድቢ",
    },
    "body_parts": {
        "head": "ርእሲ",
        "eye": "ዓይኒ",
        "nose": "ኣንፍ",
        "mouth": "ኣፍ",
        "ear": "እዝኒ",
        "hand": "ኢድ",
        "foot": "እግሪ",
        "arm": "ኣእዳው",
        "leg": "እግሪ",
        "hair": "ሰዓር",
        "face": "ገጽ",
        "neck": "ክሳድ",
        "back": "ሕቖ",
        "stomach": "ከብዲ",
        "heart": "ልቢ",
        "finger": "ጸባዕ",
    },
    "family": {
        "mother": "እንዳ",
        "father": "ኣቦ",
        "son": "ወዲ",
        "daughter": "ጓል",
        "brother": "ወዲ",
        "sister": "ሓብታ",
        "grandmother": "ኣያ",
        "grandfather": "ኣያ",
        "uncle": "ሓው",
        "aunt": "ሓብታ",
        "cousin": "ወዲ ሓው",
        "wife": "በዓልቲ ቤት",
        "husband": "በዓል ቤት",
        "child": "ቆልዓ",
        "baby": "ህጻን",
    },
    "food": {
        "bread": "ኣቦ",
        "water": "ማይ",
        "milk": "ጸባ",
        "meat": "ስጋ",
        "rice": "ሩዝ",
        "coffee": "ቡን",
        "tea": "ሻሂ",
        "sugar": "ሽኮር",
        "salt": "ጨው",
        "oil": "ዘይቲ",
        "butter": "ቦኸን",
        "honey": "ማር",
        "egg": "እንቋቑሖ",
        "fish": "ዓሳ",
        "chicken": "ዶሮ",
        "banana": "ሙዝ",
        "orange": "ኣራንቾ",
        "apple": "ፖም",
        "tomato": "ቲማቲም",
        "onion": "ሽጉርቲ",
        "garlic": "ሽጉርቲ ጸሊም",
    },
    "objects": {
        "book": "መጽሓፍ",
        "pen": "ብርዒ",
        "chair": "ኩርስ",
        "table": "ጣውላ",
        "door": "ማዕዶ",
        "window": "መስኮት",
        "house": "ቤት",
        "car": "መኪና",
        "phone": "ተለፎን",
        "computer": "ኮምፒተር",
        "television": "ተለቪዥን",
        "radio": "ራድዮ",
        "clock": "ሰዓት",
        "mirror": "መስሓሊ",
        "bag": "ሻንጣ",
        "shoes": "ጫማ",
        "clothes": "ክዳን",
        "hat": "ባርኔጣ",
        "glasses": "መጽሓሊ",
        "key": "ቁልፊ",
    },
    "nature": {
        "sun": "ጸሓይ",
        "moon": "ወርሒ",
        "star": "ኮኾብ",
        "sky": "ሰማይ",
        "earth": "መሬት",
        "water": "ማይ",
        "fire": "ሓዊ",
        "air": "ኣየር",
        "mountain": "ደብሪ",
        "river": "ወንዝ",
        "sea": "ባሕሪ",
        "tree": "ዛፍ",
        "flower": "ዕምባባ",
        "grass": "ሳዕሪ",
        "stone": "ድንጋጽ",
        "sand": "ሓሸሻ",
        "cloud": "ደመና",
        "rain": "ዝናብ",
        "wind": "ንፋስ",
    },
    "time": {
        "day": "መዓልቲ",
        "night": "ለይቲ",
        "morning": "ንግሆ",
        "evening": "ምሸት",
        "today": "ሎሚ",
        "yesterday": "ትማሊ",
        "tomorrow": "ትማሊ",
        "week": "ሰሙን",
        "month": "ወርሒ",
        "year": "ዓመት",
        "hour": "ሰዓት",
        "minute": "ደቂቃ",
        "second": "ካልኢት",
    },
    "numbers": {
        "one": "ሓደ",
        "two": "ክልተ",
        "three": "ሰለስተ",
        "four": "ኣርባዕተ",
        "five": "ሓሙሽተ",
        "six": "ሽድሽተ",
        "seven": "ሸውዓተ",
        "eight": "ሸሞንተ",
        "nine": "ትሽዓተ",
        "ten": "ዓሰርተ",
        "twenty": "ዕስራ",
        "thirty": "ሰላሳ",
        "forty": "ኣርብዓ",
        "fifty": "ሓምሳ",
        "hundred": "ሚእቲ",
        "thousand": "ሺሕ",
    },
    "verbs": {
        "eat": "በልዕ",
        "drink": "ሰተ",
        "walk": "ኸይድ",
        "run": "ጎዪ",
        "sleep": "ደቅስ",
        "wake": "ተንሳ",
        "sit": "ኣቐመጥ",
        "stand": "ተንሳ",
        "speak": "ዛረብ",
        "listen": "ሰምዕ",
        "see": "ርኢ",
        "read": "ኣንብብ",
        "write": "ጽሓፍ",
        "learn": "ተመሃር",
        "teach": "ሓብር",
        "work": "ሰርሕ",
        "play": "ጻወት",
        "sing": "ዘምር",
        "dance": "ሰዓል",
        "laugh": "ሰሓቕ",
    },
    "greetings": {
        "hello": "ሰላም",
        "goodbye": "ሰላም",
        "good morning": "ሓዳር ይባርከልና",
        "good evening": "ሓዳር ምሸት",
        "thank you": "የቐንየለይ",
        "please": "በጃኻ",
        "excuse me": "ይቕሬታ",
        "sorry": "ይቕሬታ",
        "yes": "እወ",
        "no": "ኣይፋልን",
        "how are you": "ከመይ ኣለኻ",
        "what is your name": "ስምካ እንታይ ይበሃል",
        "nice to meet you": "ብምርካብካ ሓጐስኩ",
    },
    "places": {
        "school": "ቤት ትምህርቲ",
        "hospital": "ሆስፒታል",
        "church": "ቤተ ክርስትያን",
        "mosque": "ጅሚዓ",
        "market": "ሱቕ",
        "restaurant": "ቤት ምግቢ",
        "hotel": "ሆቴል",
        "bank": "ባንክ",
        "office": "ቢሮ",
        "farm": "ሓርሽ",
        "city": "ከተማ",
        "village": "ዓድሺ",
        "country": "ሃገር",
        "park": "መናፈሻ",
        "beach": "ባሕርያዊ",
        "forest": "ዳግላ",
    },
}

# Flatten vocabulary for easy access
VOCAB_DICT = {}
for category, words in VOCAB_CATEGORIES.items():
    VOCAB_DICT.update(words)

# Common phrases and expressions
COMMON_PHRASES = {
    "How are you?": "ከመይ ኣለኻ?",
    "I am fine": "ጽቡቕ እየ",
    "What is this?": "እዚ እንታይ ይበሃል?",
    "I don't understand": "ኣይተረድኣንን",
    "Can you help me?": "ክትሕግዘኒ ትኽእል?",
    "Where is the bathroom?": "ሓሚሞ ኣበይ ኣሎ?",
    "How much does this cost?": "እዚ ክንደይ ይከፈል?",
    "I am hungry": "ጽማዐ ኣሎኒ",
    "I am thirsty": "ጸምኢ ኣሎኒ",
    "Good luck": "ፍቕሪ ይሃብካ",
}

# Difficulty levels for words (based on frequency and complexity)
DIFFICULTY_LEVELS = {
    "beginner": [
        "hello",
        "goodbye",
        "thank you",
        "yes",
        "no",
        "water",
        "bread",
        "mother",
        "father",
        "one",
        "two",
        "three",
        "red",
        "blue",
        "sun",
        "moon",
    ],
    "intermediate": [
        "beautiful",
        "difficult",
        "important",
        "understand",
        "restaurant",
        "hospital",
        "school",
        "computer",
        "telephone",
        "tomorrow",
        "yesterday",
    ],
    "advanced": [
        "democracy",
        "philosophy",
        "technology",
        "environment",
        "development",
        "conversation",
        "opportunity",
        "responsibility",
        "understanding",
    ],
}

# Word frequency data (approximate usage frequency)
WORD_FREQUENCY = {
    # High frequency (most common)
    "water": 10,
    "bread": 10,
    "mother": 10,
    "father": 10,
    "hello": 10,
    "thank you": 10,
    "yes": 10,
    "no": 10,
    "good": 9,
    "bad": 9,
    # Medium frequency
    "book": 7,
    "house": 7,
    "car": 6,
    "phone": 6,
    "school": 8,
    "hospital": 5,
    "restaurant": 5,
    "market": 7,
    # Lower frequency (specialized or less common)
    "elephant": 3,
    "leopard": 2,
    "philosophy": 1,
    "democracy": 1,
}


# Function to get words by difficulty
def get_words_by_difficulty(level: str):
    """Get words filtered by difficulty level"""
    if level in DIFFICULTY_LEVELS:
        difficulty_words = DIFFICULTY_LEVELS[level]
        return {
            word: VOCAB_DICT[word] for word in difficulty_words if word in VOCAB_DICT
        }
    return VOCAB_DICT


# Function to get words by category
def get_words_by_category(category: str):
    """Get words from a specific category"""
    if category in VOCAB_CATEGORIES:
        return VOCAB_CATEGORIES[category]
    return {}


# Function to get random words
def get_random_words(count: int = 10, category: str = None):
    """Get random words for practice"""
    import random

    if category and category in VOCAB_CATEGORIES:
        word_pool = VOCAB_CATEGORIES[category]
    else:
        word_pool = VOCAB_DICT

    if len(word_pool) <= count:
        return word_pool

    random_keys = random.sample(list(word_pool.keys()), count)
    return {key: word_pool[key] for key in random_keys}


# Statistics about the vocabulary
VOCAB_STATS = {
    "total_words": len(VOCAB_DICT),
    "total_categories": len(VOCAB_CATEGORIES),
    "total_phrases": len(COMMON_PHRASES),
    "words_per_category": {cat: len(words) for cat, words in VOCAB_CATEGORIES.items()},
    "difficulty_distribution": {
        level: len(words) for level, words in DIFFICULTY_LEVELS.items()
    },
}
