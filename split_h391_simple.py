#!/usr/bin/env python3
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
    print("=== h391 Channel 02 Splitting ===")
    
    # Check h391 directory
    h391_dir = Path("output/h391")
    print(f"Looking for: {h391_dir}")
    print(f"Directory exists: {h391_dir.exists()}")
    
    if not h391_dir.exists():
        print("❌ h391 directory not found!")
        return
    
    channel_02_file = h391_dir / "channel_02.mp3"
    print(f"Channel 02 file exists: {channel_02_file.exists()}")
    
    if not channel_02_file.exists():
        print("❌ channel_02.mp3 not found!")
        return
    
    try:
        # Load the audio file
        print("Loading channel_02.mp3...")
        audio = AudioSegment.from_mp3(channel_02_file)
        total_duration = len(audio)
        
        print(f"Total duration: {total_duration / 1000.0:.2f} seconds")
        
        # Extract first 57 seconds (mixed channel 2 and 3)
        first_57_seconds = 57 * 1000  # Convert to milliseconds
        mixed_audio = audio[:first_57_seconds]
        
        # Remaining audio is pure channel 2
        pure_channel_2 = audio[first_57_seconds:]
        
        print(f"Mixed audio (first 57s): {len(mixed_audio) / 1000.0:.2f} seconds")
        print(f"Pure channel 2 (remaining): {len(pure_channel_2) / 1000.0:.2f} seconds")
        
        # Split the mixed audio in half to separate channel 2 and 3
        split_point = len(mixed_audio) // 2
        channel_2_part1 = mixed_audio[:split_point]
        channel_3_part1 = mixed_audio[split_point:]
        
        print(f"Channel 2 part 1: {len(channel_2_part1) / 1000.0:.2f} seconds")
        print(f"Channel 3 part 1: {len(channel_3_part1) / 1000.0:.2f} seconds")
        
        # Combine channel 2 parts
        complete_channel_2 = channel_2_part1 + pure_channel_2
        
        print(f"Complete channel 2: {len(complete_channel_2) / 1000.0:.2f} seconds")
        
        # Backup original file
        backup_path = h391_dir / "channel_02_original_h391.mp3"
        audio.export(backup_path, format="mp3", bitrate="192k")
        print(f"📁 Backed up original to: {backup_path.name}")
        
        # Save the split files
        channel_2_path = h391_dir / "channel_02.mp3"
        channel_3_path = h391_dir / "channel_03.mp3"
        
        complete_channel_2.export(channel_2_path, format="mp3", bitrate="192k")
        channel_3_part1.export(channel_3_path, format="mp3", bitrate="192k")
        
        print(f"✅ Updated channel 2: {channel_2_path.name}")
        print(f"✅ Created channel 3: {channel_3_path.name}")
        
        # Verify the result
        print(f"\n=== Verification ===")
        channel_files = sorted(list(h391_dir.glob("channel_*.mp3")))
        print(f"Channel files in h391: {[f.name for f in channel_files]}")
        
        print("\n🎉 h391 channel_02 splitting completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
