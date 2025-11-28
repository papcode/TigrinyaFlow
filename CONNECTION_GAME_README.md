# 🔗 Match the Following Feature

## Overview

The Match the Following is a new interactive learning feature that allows users to connect images with their corresponding Tigrinya text labels using an HTML5 canvas interface. This exercise enhances vocabulary learning through visual association and interactive engagement.

## Features

### Core Functionality
- **Image-Text Matching**: Connect images on the left with Tigrinya text labels on the right
- **Interactive Canvas**: Draw colorful connection lines between matched pairs
- **Multiple Categories**: Choose from animals, colors, and objects
- **Adjustable Difficulty**: Select 3-6 items per exercise session
- **Real-time Feedback**: Visual indicators for correct/incorrect matches

### Visual Elements
- **Responsive Design**: Works on different screen sizes
- **Colorful Animations**: Smooth transitions and hover effects
- **Status Indicators**: 
  - Blue glow for selected items
  - Green for correct matches
  - Red for incorrect matches
  - Gray for connected items

### Exercise Controls
- **Check Answers**: Verify all connections and show results
- **Reset**: Clear all connections and start over
- **New Exercise**: Generate a fresh puzzle with different items

## How to Play

1. **Select Category**: Choose from available categories (animals, colors, objects)
2. **Choose Difficulty**: Select 3-6 items for the matching challenge
3. **Make Connections**: 
   - Click an image to select it (highlighted in blue)
   - Click a Tigrinya text label to create a connection
   - A curved line will appear connecting the pair
4. **Check Results**: Click "Check Answers" when all connections are made
5. **Review Feedback**: Green lines indicate correct matches, red lines indicate incorrect ones

## Technical Implementation

### Files Structure
```
trigrinya_learning_app/
├── utils/
│   └── connection_game.py          # Exercise logic and state management
├── page_modules/
│   └── connection_game_page.py     # UI rendering and HTML generation
└── images/vocabulary/              # Image assets organized by category
    ├── animals/
    ├── colors/
    └── objects/
```

### Key Classes
- **ConnectionGame**: Manages exercise state, puzzle generation, and scoring
- **HTML Canvas Integration**: Custom JavaScript for drawing connections and handling interactions

### Features
- **Base64 Image Encoding**: Images are embedded directly in HTML for seamless display
- **Session State Management**: Exercise progress is maintained across interactions
- **Path Resolution**: Robust image loading with multiple fallback paths
- **Vocabulary Integration**: Uses centralized vocabulary data from `vocab_data.py`

## Educational Benefits

### Learning Objectives
- **Visual Association**: Connect images with Tigrinya text to build visual memory
- **Script Recognition**: Familiarize with Tigrinya writing system
- **Category Learning**: Focus on specific vocabulary groups
- **Interactive Learning**: Exercise mechanics make learning enjoyable

### Cognitive Benefits
- **Pattern Recognition**: Identify Tigrinya character patterns
- **Memory Enhancement**: Visual-textual associations improve retention
- **Cultural Connection**: Learn vocabulary in meaningful cultural contexts

## Usage Instructions

### For Users
1. Navigate to "🔗 Match the Following" in the sidebar
2. Select your preferred category and number of items
3. Click "📝 Start New Exercise" to begin
4. Follow the on-screen instructions to make connections
5. Use the control buttons to check answers or reset

### For Developers
```python
# Import the matching exercise
from utils.connection_game import ConnectionGame

# Create exercise instance
exercise = ConnectionGame()

# Generate puzzle
puzzle = exercise.generate_puzzle("animals", 5)

# Check available categories
categories = game.get_available_categories()
```

## Customization Options

### Adding New Categories
1. Add vocabulary to `vocab_data.py` under `VOCAB_CATEGORIES`
2. Create corresponding image folder in `images/vocabulary/`
3. Add image files matching the English vocabulary keys

### Supported Image Formats
- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)

### Styling Customization
The HTML template in `connection_game_page.py` contains CSS that can be modified for:
- Colors and themes
- Animation speeds
- Layout responsions
- Typography

## Integration with Main App

The matching exercise is fully integrated into the main Tigrinya learning application:

- **Navigation**: Available in the sidebar menu
- **Session Management**: Uses Streamlit session state
- **Statistics Tracking**: Exercise results are tracked and displayable
- **Responsive Design**: Works seamlessly with the app's layout

## Future Enhancements

### Potential Improvements
- **Audio Integration**: Add pronunciation playback
- **Difficulty Levels**: Implement adaptive difficulty based on performance
- **Timer Challenges**: Add time-based exercise modes
- **Progress Tracking**: Long-term learning progress visualization
- **Collaborative Mode**: Shared learning exercises

### Technical Improvements
- **Performance Optimization**: Lazy loading for large image sets
- **Accessibility**: Enhanced screen reader support
- **Mobile Optimization**: Touch-friendly interactions
- **Offline Support**: Local storage for exercise progress

## Troubleshooting

### Common Issues
- **No Images Loading**: Check that image files exist in the vocabulary folders
- **JavaScript Errors**: Ensure browsers support HTML5 Canvas
- **Performance Issues**: Reduce number of items or optimize images

### Error Handling
- Graceful fallbacks when images are missing
- Clear error messages for configuration issues
- Robust path resolution for different deployment environments

## Testing

The matching exercise includes comprehensive testing:
- **Import Tests**: Verify all modules load correctly
- **Exercise Logic Tests**: Validate puzzle generation and scoring
- **HTML Generation Tests**: Ensure proper template rendering
- **Image Directory Tests**: Confirm image assets are accessible

Run tests with: `python test_connection_game.py`

---

## Credits

Developed as part of the Tigrinya Learning App to enhance vocabulary acquisition through interactive visual learning experiences.