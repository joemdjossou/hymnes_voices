#!/usr/bin/env python3
"""
Direct script to trim h391 channels
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    from pydub import AudioSegment
    print("✅ pydub imported successfully")
except ImportError as e:
    print(f"❌ Error importing pydub: {e}")
    sys.exit(1)

def main():
    print("=== h391 Channel Trimming Script ===")
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check h391 directory
    h391_dir = current_dir / "output" / "h391"
    print(f"Looking for: {h391_dir}")
    print(f"Directory exists: {h391_dir.exists()}")
    
    if not h391_dir.exists():
        print("❌ h391 directory not found!")
        return
    
    # Find channel files
    channel_files = list(h391_dir.glob("channel_*.mp3"))
    print(f"Found {len(channel_files)} channel files:")
    
    for f in channel_files:
        print(f"  - {f.name}")
    
    if not channel_files:
        print("❌ No channel files found!")
        return
    
    # Process each file
    trim_seconds = 54
    success_count = 0
    
    for channel_file in channel_files:
        print(f"\nProcessing {channel_file.name}...")
        
        try:
            # Load audio
            audio = AudioSegment.from_mp3(channel_file)
            original_duration = len(audio) / 1000.0
            print(f"  Original duration: {original_duration:.2f} seconds")
            
            if original_duration <= trim_seconds:
                print(f"  ⚠️  File too short to trim {trim_seconds}s")
                continue
            
            # Create backup
            backup_path = channel_file.parent / f"{channel_file.stem}_backup.mp3"
            audio.export(backup_path, format="mp3", bitrate="192k")
            print(f"  📁 Backed up to: {backup_path.name}")
            
            # Trim first 54 seconds
            trim_ms = trim_seconds * 1000
            trimmed_audio = audio[trim_ms:]
            new_duration = len(trimmed_audio) / 1000.0
            
            print(f"  New duration: {new_duration:.2f} seconds")
            
            # Save trimmed audio
            trimmed_audio.export(channel_file, format="mp3", bitrate="192k")
            print(f"  ✅ Updated: {channel_file.name}")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n=== Summary ===")
    print(f"Successfully processed: {success_count}/{len(channel_files)} files")
    
    if success_count > 0:
        print("🎉 Trimming completed!")
    else:
        print("❌ No files were processed")

if __name__ == "__main__":
    main()
