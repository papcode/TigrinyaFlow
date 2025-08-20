import os
import time
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import ddg_images
from PIL import Image
from io import BytesIO

# Vocabulary dictionary
vocab_dict = {
    "red": "ቀይሕ", "blue": "ሰማያዊ", "green": "ቀጠልያ", "yellow": "ቢጫ",
    "black": "ጸሊም", "white": "ቀይሕ", "orange": "ኣራንቾኒ", "purple": "ሊላ",
    "brown": "ቡናዊ", "dog": "ከልቢ", "cat": "ድሙ", "cow": "ላም",
    "lion": "ኣንበሳ", "horse": "ፈረስ", "goat": "ጤል", "chicken": "ዶርሆ",
    "fish": "ዓሳ", "sheep": "በጊዕ", "camel": "ገመል", "elephant": "ሓርማዝ",
    "monkey": "ህበይ", "zebra": "ኣድጊ በረኻ", "giraffe": "ዘራፍ", "snake": "ተመን",
    "tiger": "ነብሪ", "bear": "ድቢ", "donkey": "ኣድጊ", "rabbit": "ማንቲለ",
    "mouse": "ኣንጭዋ", "book": "መጽሓፍ", "pen": "ብርዒ", "chair": "ኩርሲ",
    "table": "ጣውላ", "car": "መኪና", "bus": "ኣውቶቡስ", "phone": "ተሌፎን",
    "hat": "ቆብዕ", "shoe": "ሳእኒ", "house": "ገዛ", "apple": "ቱፋሕ",
    "banana": "ባናና", "bed": "ዓራት", "cup": "ቢኬሪ", "key": "መፍትሕ",
    "door": "ማዕጾ", "bag": "ቦርሳ"
}

os.makedirs("images", exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0"}

def save_as_jpeg(img_bytes, filename):
    """Convert any format (PNG, WEBP, etc.) to JPEG and save"""
    try:
        image = Image.open(BytesIO(img_bytes)).convert("RGB")
        image.save(filename, "JPEG")
        print(f"✅ Saved {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to save {filename}: {e}")
        return False

def fetch_bing(query):
    """Scrape Bing Images for the first valid photo"""
    try:
        url = f"https://www.bing.com/images/search?q={query}+photo"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Look for real image links (not logos/base64)
        for img in soup.find_all("img"):
            img_url = img.get("src") or img.get("data-src")
            if not img_url:
                continue
            if img_url.startswith("http") and not img_url.endswith(".svg"):
                return img_url
    except Exception as e:
        print(f"⚠️ Bing failed for {query}: {e}")
    return None

def fetch_duckduckgo(query):
    """Fallback: DuckDuckGo Images"""
    try:
        results = ddg_images(query, region="wt-wt", safesearch="Off", max_results=3)
        if results:
            for r in results:
                url = r.get("image")
                if url and url.startswith("http"):
                    return url
    except Exception as e:
        print(f"⚠️ DuckDuckGo failed for {query}: {e}")
    return None

for word in vocab_dict.keys():
    filepath = os.path.join("images", f"{word}.jpg")
    if os.path.exists(filepath):
        continue

    print(f"🔎 Searching for '{word}'...")
    img_url = fetch_bing(word)

    if not img_url:
        print(f"Falling back to DuckDuckGo for {word}")
        img_url = fetch_duckduckgo(word)

    if img_url:
        try:
            r = requests.get(img_url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                save_as_jpeg(r.content, filepath)
            else:
                print(f"❌ Bad response for {word}: {r.status_code}")
        except Exception as e:
            print(f"❌ Error downloading {word}: {e}")
    else:
        print(f"❌ No image found for '{word}'")

    time.sleep(1)  # be polite
