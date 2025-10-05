#!/usr/bin/env python3
"""
Simple test script to verify MP3 files are created correctly.
"""

import os
from pathlib import Path

from pydub import AudioSegment


def test_mp3_files(directory):
    """Test if MP3 files are valid and playable."""
    directory = Path(directory)
    
    if not directory.exists():
        print(f"Directory {directory} does not exist")
        return
    
    mp3_files = list(directory.rglob("*.mp3"))
    
    if not mp3_files:
        print(f"No MP3 files found in {directory}")
        return
    
    print(f"Found {len(mp3_files)} MP3 files")
    
    valid_files = 0
    total_duration = 0
    
    for mp3_file in mp3_files:
        try:
            # Load the MP3 file
            audio = AudioSegment.from_mp3(str(mp3_file))
            duration = len(audio) / 1000.0  # Convert to seconds
            total_duration += duration
            
            print(f"✓ {mp3_file.name}: {duration:.2f}s, {len(audio)}ms")
            valid_files += 1
            
        except Exception as e:
            print(f"✗ {mp3_file.name}: Error - {e}")
    
    print(f"\nSummary:")
    print(f"Valid files: {valid_files}/{len(mp3_files)}")
    print(f"Total duration: {total_duration:.2f} seconds")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        test_mp3_files(sys.argv[1])
    else:
        test_mp3_files("test_output")
