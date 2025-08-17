# 📚 English-Tigrinya Vocabulary Learning App

A interactive Streamlit application for learning Tigrinya vocabulary with visual aids. Type in English words to see their Tigrinya translations alongside corresponding images.

## 🌟 Features

- **🔍 Word Translation**: Search for English words and see their Tigrinya translations
- **🖼️ Visual Learning**: Each word displays with a corresponding image
- **📋 Browse Mode**: View all vocabulary organized by categories (Colors, Animals, Things)
- **🎯 Quiz Mode**: Test your knowledge with interactive multiple-choice questions
- **📊 Progress Tracking**: See which words have images and track quiz performance
- **🎨 Clean Interface**: Modern, responsive design with intuitive navigation

## 📥 Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Install Required Packages
```bash
pip install streamlit pillow
```

## 🚀 Quick Start

1. **Clone or download** this repository
2. **Create the images folder** in the same directory as `app.py`:
   ```
   mkdir images
   ```
3. **Add your image files** to the `images` folder (see Image Setup below)
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```
5. **Open your browser** and navigate to `http://localhost:8501`

## 📁 Project Structure

```
tigrinya-vocab-app/
├── app.py                 # Main Streamlit application
├── images/                # Image files folder
│   ├── house.png
│   ├── cat.jpg
│   ├── dog.jpeg
│   ├── red.png
│   └── ... (more images)
├── README.md              # This file
└── requirements.txt       # Python dependencies (optional)
```

## 🖼️ Image Setup

### Supported Formats
- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- GIF (`.gif`)
- BMP (`.bmp`)
- WebP (`.webp`)

### Naming Convention
Name your image files exactly like the English words in the vocabulary:

- `house.png` → for the word "house"
- `cat.jpg` → for the word "cat"
- `red.jpeg` → for the word "red"
- etc.

**Note**: Case doesn't matter - `House.PNG`, `house.png`, and `HOUSE.jpg` will all work.

### Complete Word List
The app includes 47 words across three categories:

**Colors (9 words):**
`red`, `blue`, `green`, `yellow`, `black`, `white`, `orange`, `purple`, `brown`

**Animals (20 words):**
`dog`, `cat`, `cow`, `lion`, `horse`, `goat`, `chicken`, `fish`, `sheep`, `camel`, `elephant`, `monkey`, `zebra`, `giraffe`, `snake`, `tiger`, `bear`, `donkey`, `rabbit`, `mouse`

**Things (18 words):**
`book`, `pen`, `chair`, `table`, `car`, `bus`, `phone`, `hat`, `shoe`, `house`, `apple`, `banana`, `bed`, `cup`, `key`, `door`, `bag`

## 🎮 How to Use

### 1. Search Translation Mode
- **Type Method**: Enter an English word in the text box
- **Dropdown Method**: Select from the complete vocabulary list
- View the Tigrinya translation and corresponding image

### 2. Browse All Words Mode
- **Filter by Category**: Choose Colors, Animals, Things, or view All
- **Visual Indicators**: 🖼️ icon shows words with available images, 📝 for words without images
- **Quick View**: Click "View [word]" buttons to see images

### 3. Quiz Mode
- **Generate Questions**: Click "Generate New Question" for random multiple-choice questions
- **Track Progress**: View your score and accuracy percentage
- **Visual Feedback**: See the correct image after each answer

## 🔧 Customization

### Adding New Words
1. **Edit the vocabulary dictionary** in `app.py`:
   ```python
   vocab_dict = {
       # Add your new words here
       "new_word": "ትግርኛ_translation",
       # ... existing words
   }
   ```
2. **Add corresponding images** to the `images` folder
3. **Restart the app** to see changes

### Changing Image Folder
Modify the `images_folder` parameter in the `get_local_image()` function calls if you want to use a different folder name.

## 🛠️ Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pillow (PIL)**: Image processing library
- **os, glob**: File system operations (built-in Python modules)

### Performance Notes
- Images are loaded on-demand for better performance
- Supports various image formats automatically
- Responsive design works on desktop and mobile devices

## 🐛 Troubleshooting

### Common Issues

**"Images folder not found" warning:**
- Create an `images` folder in the same directory as `app.py`
- Make sure the folder name is exactly `images` (lowercase)

**"No image found for [word]" warning:**
- Check that your image file name exactly matches the English word
- Verify the file extension is supported (png, jpg, jpeg, gif, bmp, webp)
- Case doesn't matter: `House.PNG` and `house.png` both work

**Quiz not working:**
- Make sure you have multiple words in your vocabulary (minimum 4 for multiple choice)
- Check that the vocabulary dictionary is properly formatted

**App won't start:**
- Verify Python 3.7+ is installed: `python --version`
- Install missing packages: `pip install streamlit pillow`
- Check for syntax errors in `app.py`

### Getting Help
1. Check the **sidebar stats** in the app to see which images are missing
2. Use the **"Show Missing Images"** button to get a list of needed files
3. Ensure image files are in the correct folder and named properly

## 📈 Future Enhancements

Potential features for future versions:
- Audio pronunciation using text-to-speech
- Spaced repetition learning algorithm
- Progress tracking and statistics
- Export/import custom vocabulary lists
- Multiple language support
- Image upload interface
- Offline mobile app version

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding more vocabulary words
- Improving the user interface
- Adding new features
- Reporting bugs or issues
- Suggesting enhancements

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Tigrinya language support for educational purposes
- Community contributions welcome

---

**Happy Learning! 🎓✨**

*For questions or support, please open an issue in this repository.*