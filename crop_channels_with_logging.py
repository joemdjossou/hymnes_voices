#!/usr/bin/env python3
"""
Enhanced MIDI Channel Cropper with detailed logging
Crops MIDI channels to match reference MP3 lengths, keeping the last part of audio.
"""

import argparse
import os
import tempfile
import time
from datetime import datetime
from pathlib import Path

import requests
from pydub import AudioSegment
from pydub.playback import play


class ChannelCropperWithLogging:
    def __init__(self, output_dir="output", reference_base_url="https://troisanges.org/Musique/HymnesEtLouanges/MP3/"):
        self.output_dir = Path(output_dir)
        self.reference_base_url = reference_base_url
        self.temp_dir = Path(tempfile.mkdtemp())
        self.processed_folders = []
        self.failed_folders = []
        self.start_time = datetime.now()
        
        # Create log file
        self.log_file = Path("cropping_log.txt")
        self.log(f"=== CROPPING SESSION STARTED at {self.start_time} ===")

    def __del__(self):
        # Clean up temporary directory
        if self.temp_dir.exists():
            for item in self.temp_dir.iterdir():
                if item.is_file():
                    item.unlink()
            self.temp_dir.rmdir()

    def log(self, message):
        """Log message to both console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        print(log_message)
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

    def get_reference_audio_duration(self, hymn_number):
        """
        Downloads the reference MP3 and returns its duration in seconds.
        """
        hymn_str = f"H{hymn_number:03d}"
        reference_url = f"{self.reference_base_url}{hymn_str}.mp3"
        temp_ref_path = self.temp_dir / f"{hymn_str}.mp3"

        self.log(f"Downloading reference audio: {reference_url}")
        try:
            response = requests.get(reference_url, stream=True, timeout=30)
            response.raise_for_status()
            with open(temp_ref_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            audio = AudioSegment.from_mp3(temp_ref_path)
            duration = len(audio) / 1000.0  # duration in seconds
            self.log(f"Reference audio duration: {duration:.2f} seconds")
            return duration
        except requests.exceptions.RequestException as e:
            self.log(f"ERROR downloading reference audio {reference_url}: {e}")
            return None
        except Exception as e:
            self.log(f"ERROR processing reference audio {reference_url}: {e}")
            return None
        finally:
            if temp_ref_path.exists():
                temp_ref_path.unlink()

    def crop_channel_files(self, hymn_number, target_duration):
        """
        Crops all channel MP3s for a given hymn to the target duration, keeping the last part.
        """
        hymn_folder = self.output_dir / f"h{hymn_number}"
        
        # Log folder check
        self.log(f"CHECKING FOLDER: {hymn_folder}")
        
        if not hymn_folder.is_dir():
            self.log(f"FOLDER NOT FOUND: {hymn_folder} - SKIPPING")
            self.failed_folders.append(f"h{hymn_number} (folder not found)")
            return 0

        channel_files = sorted(list(hymn_folder.glob("channel_*.mp3")))
        if not channel_files:
            self.log(f"NO CHANNEL FILES FOUND in {hymn_folder} - SKIPPING")
            self.failed_folders.append(f"h{hymn_number} (no channel files)")
            return 0

        self.log(f"FOLDER PROCESSED: {hymn_folder} - Found {len(channel_files)} channel files")
        self.processed_folders.append(f"h{hymn_number}")

        cropped_count = 0
        for channel_file in channel_files:
            self.log(f"  Processing {channel_file.name}...")
            try:
                audio = AudioSegment.from_mp3(channel_file)
                current_duration = len(audio) / 1000.0

                if current_duration > target_duration:
                    # Keep the last 'target_duration' seconds
                    start_trim_ms = int((current_duration - target_duration) * 1000)
                    cropped_audio = audio[start_trim_ms:]
                    cropped_audio.export(channel_file, format="mp3", bitrate="192k")
                    self.log(f"    CROPPED: removed first {start_trim_ms / 1000.0:.2f}s, kept last {target_duration:.2f}s")
                    cropped_count += 1
                else:
                    self.log(f"    SKIPPED: Current duration: {current_duration:.2f}s, Target: {target_duration:.2f}s (already shorter)")
            except Exception as e:
                self.log(f"    ERROR cropping {channel_file.name}: {e}")
                self.failed_folders.append(f"h{hymn_number}/{channel_file.name} (error: {e})")
        
        self.log(f"SUCCESS: Cropped {cropped_count}/{len(channel_files)} channels in h{hymn_number}")
        return cropped_count

    def process_hymns(self, start_hymn, end_hymn):
        """
        Processes a range of hymns to crop their channels.
        """
        total_hymns = end_hymn - start_hymn + 1
        self.log(f"=== STARTING BATCH PROCESSING ===")
        self.log(f"Processing {total_hymns} hymns: h{start_hymn} to h{end_hymn}")
        self.log(f"This will take some time as we need to download reference files and crop all channels...")

        for i in range(start_hymn, end_hymn + 1):
            self.log(f"\n=== PROCESSING HYMN {i} ({i-start_hymn+1}/{total_hymns}) ===")
            target_duration = self.get_reference_audio_duration(i)
            if target_duration is not None:
                cropped_count = self.crop_channel_files(i, target_duration)
                total_channels = len(list((self.output_dir / f'h{i}').glob('channel_*.mp3'))) if (self.output_dir / f'h{i}').exists() else 0
                self.log(f"HYMN {i} COMPLETE: Successfully cropped {cropped_count}/{total_channels} channels")
            else:
                self.log(f"HYMN {i} FAILED: Could not get reference duration, skipping cropping.")
                self.failed_folders.append(f"h{i} (reference download failed)")

        # Final summary
        end_time = datetime.now()
        duration = end_time - self.start_time
        self.log(f"\n=== BATCH PROCESSING COMPLETE ===")
        self.log(f"Total time: {duration}")
        self.log(f"Processed folders: {len(self.processed_folders)}")
        self.log(f"Failed folders: {len(self.failed_folders)}")
        
        if self.processed_folders:
            self.log(f"Successfully processed: {', '.join(self.processed_folders)}")
        
        if self.failed_folders:
            self.log(f"Failed to process: {', '.join(self.failed_folders)}")


def main():
    parser = argparse.ArgumentParser(description="Crop MIDI channels to match reference MP3 lengths with detailed logging.")
    parser.add_argument("--start", type=int, default=1, help="Starting hymn number (e.g., 1 for H001)")
    parser.add_argument("--end", type=int, default=654, help="Ending hymn number (e.g., 654 for H654)")
    parser.add_argument("--output_dir", type=str, default="output", help="Directory containing processed hymn channels")
    parser.add_argument("--reference_url", type=str,
                        default="https://troisanges.org/Musique/HymnesEtLouanges/MP3/",
                        help="Base URL for reference MP3s")
    
    args = parser.parse_args()

    cropper = ChannelCropperWithLogging(args.output_dir, args.reference_url)
    cropper.process_hymns(args.start, args.end)


if __name__ == "__main__":
    main()
