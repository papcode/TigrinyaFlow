# Tigrinya Learning App 📚

A comprehensive interactive web application for learning Tigrinya vocabulary, alphabet, and language skills using Streamlit.

## Features

### 🔍 **Search & Translation**
- **Word Search**: Search vocabulary in English or Tigrinya
- **Live Translation**: Google Translate integration for real-time translation
- **Transliteration**: Convert between Latin and Geʽez scripts
- **Image Support**: Visual learning with word images
- **Phonetic Guide**: Romanized pronunciation for all words

### 📚 **Browse Vocabulary**
- **Category Browsing**: Explore words by categories (colors, animals, family, etc.)
- **Random Discovery**: Generate random word sets for practice
- **Practice Sessions**: Build personal word collections
- **Word of the Day**: Daily featured vocabulary

### ✍️ **Alphabet Learning**
- **Interactive Alphabet**: Complete Geʽez character system
- **Handwriting Animations**: Visual character formation
- **Character Recognition**: Practice identifying characters
- **Vowel Forms**: Learn consonant-vowel combinations
- **Progressive Learning**: Structured learning path

### 🎯 **Quiz System**
- **Multiple Choice Quizzes**: English ↔ Tigrinya translation quizzes
- **Category-based**: Focus on specific vocabulary areas
- **Progress Tracking**: Detailed performance analytics
- **Streak Building**: Gamified learning experience
- **Difficulty Levels**: Adaptive question complexity

### 🎮 **Interactive Games**
- **Drag & Drop**: Word building and matching games
- **Character Practice**: Interactive alphabet exercises
- **Visual Learning**: Image-based vocabulary games

### 📊 **Progress Analytics**
- **Detailed Statistics**: Comprehensive learning metrics
- **Performance Charts**: Visual progress tracking
- **Achievement System**: Milestone badges and rewards
- **Learning Insights**: Personalized recommendations
- **Study Schedule**: Structured learning plans

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd tigrinya_learning_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

4. **Access the app**
   Open your browser to `http://localhost:8501`

## Project Structure

```
tigrinya_learning_app/
├── main.py                 # Main application entry point
├── clientTranslation.py    # Geʽez transliteration engine
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── pages/                 # Page modules
│   ├── __init__.py
│   ├── search_page.py     # Search and translation
│   ├── browse_page.py     # Vocabulary browsing
│   ├── alphabet_page.py   # Alphabet learning
│   ├── quiz_page.py       # Quiz system
│   ├── statistics_page.py # Progress analytics
│   └── drag_drop_page.py  # Interactive games
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── vocab_data.py      # Vocabulary database
│   ├── image_loader.py    # Image handling
│   ├── quiz_manager.py    # Quiz logic
│   └── drag_drop_game.py  # Game mechanics
├── assets/                # Static assets
├── images/                # Word images (optional)
└── myenv/                 # Virtual environment (if used)
```

## Usage Guide

### Getting Started
1. **Navigation**: Use the sidebar to switch between different learning modes
2. **Search Words**: Start with the Search page to explore vocabulary
3. **Browse Categories**: Explore vocabulary by themes like colors, family, food
4. **Learn Alphabet**: Practice Geʽez characters with interactive animations
5. **Take Quizzes**: Test your knowledge with multiple-choice questions
6. **Track Progress**: Monitor your learning with detailed statistics

### Learning Path Recommendations
1. **Beginners**: Start with greetings, numbers, and colors
2. **Intermediate**: Explore family, food, and common phrases
3. **Advanced**: Practice with full sentences and complex vocabulary

### Features Deep Dive

#### **Transliteration System**
- Uses phonetic Latin input (e.g., "salam" → "ሰላም")
- Supports special characters: ch→č, sh→š, kh→x, etc.
- Bidirectional conversion: Latin ↔ Geʽez

#### **Quiz System**
- **English→Tigrinya**: Translate English words to Tigrinya
- **Tigrinya→English**: Translate Tigrinya words to English
- **Categories**: Focus on specific vocabulary areas
- **Difficulty**: Adaptive based on your performance

#### **Progress Tracking**
- **Accuracy Metrics**: Track your quiz performance
- **Streak Counters**: Monitor consecutive correct answers
- **Word Mastery**: See which words you've learned
- **Category Progress**: Track learning across different topics

## Vocabulary Database

The app includes over 300+ words across categories:
- **Colors** (14 words): Basic and extended color vocabulary
- **Animals** (21 words): Common animals and pets
- **Family** (15 words): Family relationships and terms
- **Food** (22 words): Daily food items and meals
- **Body Parts** (16 words): Human body vocabulary
- **Numbers** (16 words): Numbers 1-1000
- **Greetings** (13 words): Essential conversation starters
- **Places** (16 words): Locations and buildings
- **Nature** (19 words): Natural world vocabulary
- **Time** (12 words): Time-related terms
- **Verbs** (20 words): Common action words
- **Objects** (20 words): Everyday items

## Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Plotly**: Interactive charts and graphs
- **Pandas**: Data manipulation
- **Pillow**: Image processing
- **Deep Translator**: Google Translate API
- **Requests**: HTTP requests for images

### Image Support
- Local image loading from `images/` folder
- Unsplash API integration (requires API key)
- Automatic image display for vocabulary words

### Data Persistence
- Session-based statistics (resets on browser refresh)
- Local storage for user preferences
- Export functionality for progress data

## Customization

### Adding New Vocabulary
Edit `utils/vocab_data.py` to add new words:
```python
VOCAB_CATEGORIES = {
    "your_category": {
        "english_word": "ትግርኛ_translation",
        # ... more words
    }
}
```

### Adding Images
Place images in the `images/` folder with filenames matching English words:
- `dog.jpg` for the word "dog"
- `red.png` for the word "red"
- Supported formats: JPG, PNG, WebP, GIF

### Unsplash Integration
To enable automatic image fetching:
1. Get a free API key from [Unsplash](https://unsplash.com/developers)
2. Update `utils/image_loader.py`:
   ```python
   self.unsplash_access_key = "your_actual_api_key_here"
   ```

## Troubleshooting

### Common Issues

1. **App won't start**
   - Check Python version (3.8+ required)
   - Install all dependencies: `pip install -r requirements.txt`
   - Try: `python -m streamlit run main.py`

2. **Images not loading**
   - Check `images/` folder exists
   - Verify image file names match vocabulary words
   - For Unsplash: add valid API key

3. **Translation errors**
   - Check internet connection for Google Translate
   - Verify `deep_translator` is installed correctly

4. **Performance issues**
   - Reduce number of vocabulary words if needed
   - Clear browser cache
   - Restart the Streamlit server

### Error Messages
- **"Module not found"**: Install missing dependency with pip
- **"No results found"**: Check vocabulary database spelling
- **"Translation error"**: Check internet connection

## Contributing

To contribute to this project:
1. Fork the repository
2. Create feature branches
3. Follow existing code style
4. Test thoroughly
5. Submit pull requests

### Development Setup
```bash
# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run main.py --server.runOnSave true
```

## License

This project is open source. See LICENSE file for details.

## Acknowledgments

- **Geʽez Script**: Ancient Ethiopian/Eritrean writing system
- **Tigrinya Language**: Spoken in Eritrea and northern Ethiopia
- **Community**: Thanks to all contributors and language learners
- **Streamlit**: For the amazing web framework
- **Google Translate**: For translation API services

## Support

For questions, issues, or feature requests:
1. Check this README for common solutions
2. Search existing issues in the repository
3. Create a new issue with detailed description
4. Join the community discussion

## Recent Updates

### ✅ Advanced Handwriting Animation System Complete (Latest)
**Issue Resolved:** The alphabet page now has the EXACT same advanced handwriting animation system as `interface_reference.py` with all sophisticated features.

**Complete Implementation:**
- **Full Fluid Path System**: Advanced contour extraction and intelligent path connection
- **Multi-Canvas Compositing**: Glyph canvas, mask canvas, and main canvas layers
- **Pressure-Sensitive Rendering**: Dynamic pen pressure based on speed and position
- **Auto-Starting Animations**: Characters automatically begin sophisticated handwriting simulation
- **Bezier Curve Processing**: Quadratic and cubic Bezier curve sampling for smooth paths
- **Intelligent Entry Points**: Optimal stroke order determination for natural writing
- **Path Resampling**: Fixed step-size resampling for consistent animation speed
- **Canvas Auto-Scrolling**: Viewport follows pen movement during writing

**Advanced Features Confirmed:**
- ✅ **33,929-character HTML**: Complete JavaScript animation system
- ✅ **OpenType.js Integration**: Full font loading and path extraction
- ✅ **Fluid Path Generation**: `convertToFluidPath`, `extractPathContours`, `createFluidContourPath`
- ✅ **Advanced Algorithms**: `findOptimalEntryPoint`, `reorderContourFromPoint`, `interpolatePoints`
- ✅ **Realistic Pen Rendering**: Gradient fills, shadows, pressure variation, speed calculation
- ✅ **Multi-Style Support**: Realistic, Simple, and Brush pen styles
- ✅ **Progressive Animation**: Frame counting, progress tracking, auto-completion
- ✅ **Canvas Compositing**: Mask-based ink revelation system

**Technical Architecture:**
- **Complete `create_auto_start_handwriting_html`** function (878 lines) extracted from original
- **Advanced path processing** with contour analysis and optimal stroke ordering  
- **Multi-layer rendering** system with glyph pre-rendering and mask compositing
- **Performance optimization** with requestAnimationFrame and dynamic timing
- **Cross-browser compatibility** with proper canvas context configuration

---

**Happy Learning! 🎉**

*Start your Tigrinya learning journey today with interactive vocabulary, alphabet practice, and engaging quizzes.*