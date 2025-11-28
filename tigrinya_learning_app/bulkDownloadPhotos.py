"""
Download images for vocabulary words using Unsplash API
Based on official Unsplash API documentation
"""

import requests
import os
import time
from pathlib import Path
from typing import Dict, List, Optional
import json

# Import your vocabulary data
from utils.vocab_data import VOCAB_CATEGORIES, VOCAB_DICT

# Configuration
UNSPLASH_ACCESS_KEY = "Wjqm9UdMChNSK_dTNNxaDqHLUa1nuGysaw1K99XuB1c"  # Get free key at https://unsplash.com/developers
OUTPUT_DIR = "vocab_images"
DELAY_BETWEEN_REQUESTS = 145  # seconds. Unsplash demo limit is 50 reqs/hr. Each word is 2 reqs. (3600s/hr / (50req/hr / 2req/word)) = 144s/word.
API_BASE_URL = "https://api.unsplash.com"


class VocabularyImageDownloader:
    def __init__(self, access_key: str, output_dir: str = OUTPUT_DIR):
        self.access_key = access_key
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.download_log = []
        self.requests_made = 0
        self.existing_words = self._get_existing_image_words()
        if self.existing_words:
            print(f"  Found {len(self.existing_words)} existing images. These will be skipped.")
        
    def _get_existing_image_words(self, image_dir: str = "images") -> List[str]:
        """
        Scans a directory recursively for image files and returns a list of
        word stems from the filenames.
        """
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        existing_words = set()
        image_path = Path(image_dir)
        
        if not image_path.is_dir():
            # It's fine if the directory doesn't exist yet
            return []

        for p in image_path.rglob('*'):
            if p.suffix.lower() in image_extensions:
                existing_words.add(p.stem)
        
        return list(existing_words)

    def search_image(self, word: str, per_page: int = 1) -> Optional[Dict]:
        """
        Search for an image using Unsplash API
        Returns the first matching photo object or None
        """
        url = f"{API_BASE_URL}/search/photos"
        
        # Use Authorization header as recommended by Unsplash
        headers = {
            "Authorization": f"Client-ID {self.access_key}",
            "Accept-Version": "v1"
        }
        
        params = {
            "query": word,
            "per_page": per_page,
            "orientation": "landscape",
            "content_filter": "high"  # Filter for appropriate content
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            self.requests_made += 1
            
            # Check rate limit headers
            rate_limit_remaining = response.headers.get('X-Ratelimit-Remaining')
            if rate_limit_remaining:
                print(f"  [Rate limit remaining: {rate_limit_remaining}]")
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("results") and len(data["results"]) > 0:
                return data["results"][0]
            else:
                print(f"  No image found for: {word}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"  Error searching for {word}: {e}")
            return None
    
    def download_image(self, photo: Dict, filename: str) -> bool:
        """
        Download image from photo object
        Uses the 'regular' size URL (1080px width)
        """
        try:
            # Get the regular size image URL
            image_url = photo["urls"]["regular"]
            
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            filepath = self.output_dir / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  ✓ Downloaded: {filename}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Error downloading {filename}: {e}")
            return False
    
    def trigger_download_tracking(self, photo: Dict) -> None:
        """
        Trigger download tracking as required by Unsplash API guidelines
        This increments the download counter for the photo
        """
        try:
            download_location = photo["links"]["download_location"]
            
            headers = {
                "Authorization": f"Client-ID {self.access_key}",
                "Accept-Version": "v1"
            }
            
            response = requests.get(download_location, headers=headers)
            self.requests_made += 1
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            print(f"  Warning: Could not track download: {e}")
    
    def get_attribution(self, photo: Dict) -> Dict[str, str]:
        """
        Get photographer attribution information as required by Unsplash guidelines
        """
        user = photo.get("user", {})
        return {
            "photographer_name": user.get("name", "Unknown"),
            "photographer_username": user.get("username", ""),
            "photographer_url": user.get("links", {}).get("html", ""),
            "photo_url": photo.get("links", {}).get("html", ""),
            "unsplash_url": "https://unsplash.com"
        }
    
    def download_vocabulary_images(self, categories: Optional[List[str]] = None):
        """Download images for vocabulary words, skipping existing ones."""
        
        if categories:
            vocab_to_download = {}
            for cat in categories:
                if cat in VOCAB_CATEGORIES:
                    vocab_to_download.update(VOCAB_CATEGORIES[cat])
        else:
            vocab_to_download = VOCAB_DICT
            
        # Filter out words that already have an image
        vocab_to_process = {
            eng: tig for eng, tig in vocab_to_download.items()
            if eng not in self.existing_words
        }

        total_in_list = len(vocab_to_download)
        total_to_download = len(vocab_to_process)
        skipped_count = total_in_list - total_to_download
        
        if skipped_count > 0:
            print(f"\nSkipped {skipped_count} words that already have images.")

        if total_to_download == 0:
            print("✅ All vocabulary words in the selected list already have images. Nothing to download.")
            return
            
        success = 0
        failed = 0
        
        print(f"\n📥 Starting download of {total_to_download} new vocabulary images...")
        print(f"⚠️  Demo mode rate limit: 50 requests/hour")
        print(f"   This will take approximately {(total_to_download * DELAY_BETWEEN_REQUESTS / 60):.1f} minutes\n")
        
        for idx, (english_word, tigrinya_word) in enumerate(vocab_to_process.items(), 1):
            print(f"\n[{idx}/{total_to_download}] Processing: {english_word} ({tigrinya_word})")
            
            # Search for image
            photo = self.search_image(english_word)
            
            if photo:
                # Create safe filename
                safe_word = english_word.replace(" ", "_").lower()
                filename = f"{safe_word}.jpg"
                
                # Get attribution info
                attribution = self.get_attribution(photo)
                
                # Trigger download tracking (required by Unsplash)
                self.trigger_download_tracking(photo)
                
                # Download image
                if self.download_image(photo, filename):
                    success += 1
                    self.download_log.append({
                        "english": english_word,
                        "tigrinya": tigrinya_word,
                        "filename": filename,
                        "status": "success",
                        "attribution": attribution
                    })
                    print(f"  📸 Photo by {attribution['photographer_name']} on Unsplash")
                else:
                    failed += 1
                    self.download_log.append({
                        "english": english_word,
                        "tigrinya": tigrinya_word,
                        "filename": filename,
                        "status": "download_failed"
                    })
            else:
                failed += 1
                self.download_log.append({
                    "english": english_word,
                    "tigrinya": tigrinya_word,
                    "filename": None,
                    "status": "no_image_found"
                })
            
            # Delay to respect rate limits
            print(f"  ⏳ Waiting {DELAY_BETWEEN_REQUESTS}s...")
            time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Save download log
        self.save_log()
        
        # Print summary
        print("\n" + "="*60)
        print("📊 DOWNLOAD SUMMARY")
        print("="*60)
        print(f"Total words in vocabulary list: {total_in_list}")
        print(f"Skipped (image already exists): {skipped_count}")
        print(f"New images to download: {total_to_download}")
        print("-" * 20)
        print(f"✓ Successful downloads: {success}")
        print(f"✗ Failed downloads: {failed}")
        if total_to_download > 0:
            print(f"Success rate on new downloads: {(success/total_to_download*100):.1f}%")
        print(f"Total API requests made: {self.requests_made}")
        print(f"\nImages saved to: {self.output_dir.absolute()}")
        print(f"Download log saved to: {self.output_dir / 'download_log.json'}")
        print(f"Attribution info saved to: {self.output_dir / 'attributions.txt'}")
        
        # Save attribution file
        self.save_attributions()
        
    def save_log(self):
        """Save download log to JSON file"""
        log_path = self.output_dir / "download_log.json"
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.download_log, f, indent=2, ensure_ascii=False)
    
    def save_attributions(self):
        """
        Save attribution information as required by Unsplash API guidelines
        """
        attr_path = self.output_dir / "attributions.txt"
        with open(attr_path, 'w', encoding='utf-8') as f:
            f.write("PHOTO ATTRIBUTIONS\n")
            f.write("="*60 + "\n\n")
            f.write("As required by Unsplash API Guidelines:\n")
            f.write("All photos must be attributed to their photographers.\n\n")
            
            for entry in self.download_log:
                if entry["status"] == "success" and "attribution" in entry:
                    attr = entry["attribution"]
                    f.write(f"{entry['english']} ({entry['tigrinya']})\n")
                    f.write(f"  Photo by {attr['photographer_name']}\n")
                    f.write(f"  {attr['photo_url']}\n")
                    f.write(f"  Unsplash: {attr['unsplash_url']}\n\n")
    
    def download_by_category(self, category: str):
        """Download images for a specific category"""
        if category not in VOCAB_CATEGORIES:
            print(f"❌ Category '{category}' not found!")
            print(f"Available categories: {', '.join(VOCAB_CATEGORIES.keys())}")
            return
        
        print(f"\n📁 Downloading images for category: {category}")
        
        # Create category subfolder
        category_dir = self.output_dir / category
        category_dir.mkdir(exist_ok=True)
        
        # Temporarily change output directory
        original_dir = self.output_dir
        self.output_dir = category_dir
        
        # Download images
        self.download_vocabulary_images([category])
        
        # Restore original directory
        self.output_dir = original_dir


def main():
    """Main function"""
    
    # Check if API key is set
    if UNSPLASH_ACCESS_KEY == "YOUR_ACCESS_KEY_HERE":
        print("⚠️  Please set your Unsplash Access Key!")
        print("\n📝 Steps to get a free API key:")
        print("1. Go to https://unsplash.com/developers")
        print("2. Register for a free developer account")
        print("3. Create a new application")
        print("4. Copy your Access Key (not the Secret key)")
        print("5. Replace YOUR_ACCESS_KEY_HERE in this script\n")
        print("📊 Rate Limits:")
        print("   - Demo mode: 50 requests per hour")
        print("   - Production mode: 5000 requests per hour (requires approval)")
        print("\n⚖️  Important: You must follow Unsplash API Guidelines")
        print("   - Properly attribute photographers")
        print("   - Trigger download tracking")
        print("   - Link back to Unsplash")
        return
    
    downloader = VocabularyImageDownloader(UNSPLASH_ACCESS_KEY)
    
    # Example usage options:
    
    # Option 1: Download all vocabulary images (will take ~4-5 hours in demo mode!)
    # downloader.download_vocabulary_images()
    
    # Option 2: Download images for specific categories (RECOMMENDED for testing)
    # downloader.download_vocabulary_images(categories=["colors", "animals"])
    
    # Option 3: Download images for one category at a time
    #downloader.download_by_category("colors")
    downloader.download_vocabulary_images(categories=VOCAB_CATEGORIES.keys())

    print("\n✅ Done! Check the output folder for images and attribution info.")


if __name__ == "__main__":
    main()