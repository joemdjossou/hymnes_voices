#!/usr/bin/env python3
"""
Script to download all MP3 files from https://troisanges.org/Musique/HymnesEtLouanges/MP3/
from H001.mp3 to H654.mp3
"""

import os
import time
from pathlib import Path

import requests


def download_mp3_files():
    """Download all MP3 files from H001 to H654"""
    
    # Create audio directory if it doesn't exist
    audio_dir = Path("audio")
    audio_dir.mkdir(exist_ok=True)
    
    base_url = "https://troisanges.org/Musique/HymnesEtLouanges/MP3/"
    
    # Download files from H001 to H654
    downloaded_count = 0
    failed_count = 0
    failed_files = []
    
    print("Starting download of MP3 files...")
    print(f"Downloading to: {audio_dir.absolute()}")
    
    for i in range(1, 655):  # H001 to H654
        filename = f"H{i:03d}.mp3"
        url = f"{base_url}{filename}"
        filepath = audio_dir / filename
        
        # Skip if file already exists
        if filepath.exists():
            print(f"✓ {filename} already exists, skipping...")
            downloaded_count += 1
            continue
        
        try:
            print(f"Downloading {filename}...", end=" ")
            
            # Make request with timeout
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save file
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Success ({len(response.content)} bytes)")
            downloaded_count += 1
            
            # Small delay to be respectful to the server
            time.sleep(0.1)
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed: {e}")
            failed_count += 1
            failed_files.append(filename)
            
            # If file was partially downloaded, remove it
            if filepath.exists():
                filepath.unlink()
        
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            failed_count += 1
            failed_files.append(filename)
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Download Summary:")
    print(f"✓ Successfully downloaded: {downloaded_count} files")
    print(f"✗ Failed downloads: {failed_count} files")
    
    if failed_files:
        print(f"\nFailed files:")
        for filename in failed_files:
            print(f"  - {filename}")
    
    print(f"\nFiles saved to: {audio_dir.absolute()}")

if __name__ == "__main__":
    download_mp3_files()
