#!/usr/bin/env python3
"""
Channel Cropper: Crop channel MP3s to match reference audio length
Takes the LAST part of each channel to match the reference duration.
"""

import argparse
import os
import tempfile
from pathlib import Path

import requests
from pydub import AudioSegment


class ChannelCropper:
    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.base_url = "https://troisanges.org/Musique/HymnesEtLouanges/MP3/"
        
    def download_reference_audio(self, hymn_number):
        """Download reference MP3 and return its duration in milliseconds."""
        try:
            # Format hymn number with leading zeros (H001, H002, etc.)
            hymn_id = f"H{hymn_number:03d}"
            url = f"{self.base_url}{hymn_id}.mp3"
            
            print(f"Downloading reference audio: {url}")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name
            
            # Get duration
            audio = AudioSegment.from_mp3(temp_path)
            duration_ms = len(audio)
            duration_seconds = duration_ms / 1000.0
            
            print(f"Reference audio duration: {duration_seconds:.2f} seconds")
            
            # Clean up temp file
            os.unlink(temp_path)
            
            return duration_ms
            
        except Exception as e:
            print(f"Error downloading reference audio for H{hymn_number:03d}: {e}")
            return None
    
    def crop_channel_audio(self, channel_path, target_duration_ms):
        """Crop channel audio to target duration, keeping the LAST part."""
        try:
            # Load the channel audio
            audio = AudioSegment.from_mp3(str(channel_path))
            current_duration_ms = len(audio)
            
            print(f"  Current duration: {current_duration_ms/1000:.2f}s, Target: {target_duration_ms/1000:.2f}s")
            
            if current_duration_ms <= target_duration_ms:
                print(f"  Channel already shorter than target, skipping")
                return False
            
            # Calculate how much to remove from the beginning
            trim_start_ms = current_duration_ms - target_duration_ms
            
            # Crop to keep the last part
            cropped_audio = audio[trim_start_ms:]
            
            # Save the cropped audio
            cropped_audio.export(str(channel_path), format="mp3", bitrate="192k")
            
            print(f"  Cropped: removed first {trim_start_ms/1000:.2f}s, kept last {target_duration_ms/1000:.2f}s")
            return True
            
        except Exception as e:
            print(f"  Error cropping {channel_path}: {e}")
            return False
    
    def process_hymn(self, hymn_number):
        """Process all channels for a specific hymn."""
        print(f"\n=== Processing Hymn {hymn_number} ===")
        
        # Get reference duration
        reference_duration_ms = self.download_reference_audio(hymn_number)
        if reference_duration_ms is None:
            print(f"Failed to get reference duration for hymn {hymn_number}")
            return
        
        # Find the hymn folder
        hymn_folder = self.output_dir / f"h{hymn_number}"
        if not hymn_folder.exists():
            print(f"Hymn folder not found: {hymn_folder}")
            return
        
        # Process all channel MP3s in the folder
        channel_files = list(hymn_folder.glob("channel_*.mp3"))
        if not channel_files:
            print(f"No channel files found in {hymn_folder}")
            return
        
        print(f"Found {len(channel_files)} channel files")
        
        cropped_count = 0
        for channel_file in sorted(channel_files):
            print(f"Processing {channel_file.name}...")
            if self.crop_channel_audio(channel_file, reference_duration_ms):
                cropped_count += 1
        
        print(f"Successfully cropped {cropped_count}/{len(channel_files)} channels")
    
    def process_hymns(self, hymn_numbers):
        """Process multiple hymns."""
        for hymn_number in hymn_numbers:
            self.process_hymn(hymn_number)


def main():
    parser = argparse.ArgumentParser(description="Crop channel MP3s to match reference audio length")
    parser.add_argument("hymns", nargs="+", type=int, help="Hymn numbers to process (e.g., 1 2 3)")
    parser.add_argument("--output-dir", default="output", help="Output directory containing hymn folders")
    
    args = parser.parse_args()
    
    cropper = ChannelCropper(args.output_dir)
    cropper.process_hymns(args.hymns)


if __name__ == "__main__":
    main()
