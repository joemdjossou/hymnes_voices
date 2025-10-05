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
    print("=== h391 Channel 02 Correct Splitting ===")
    
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
        
        # Split at 57 seconds:
        # - First 57 seconds = channel_03.mp3
        # - Remaining 56 seconds = real channel_02.mp3
        split_point = 57 * 1000  # Convert to milliseconds
        
        channel_03_audio = audio[:split_point]  # First 57 seconds
        real_channel_02_audio = audio[split_point:]  # Remaining 56 seconds
        
        print(f"Channel 03 (first 57s): {len(channel_03_audio) / 1000.0:.2f} seconds")
        print(f"Real Channel 02 (remaining): {len(real_channel_02_audio) / 1000.0:.2f} seconds")
        
        # Backup original file
        backup_path = h391_dir / "channel_02_original_h391.mp3"
        audio.export(backup_path, format="mp3", bitrate="192k")
        print(f"📁 Backed up original to: {backup_path.name}")
        
        # Save the split files
        channel_02_path = h391_dir / "channel_02.mp3"
        channel_03_path = h391_dir / "channel_03.mp3"
        
        # Replace channel_02.mp3 with the real channel 2 (remaining 56 seconds)
        real_channel_02_audio.export(channel_02_path, format="mp3", bitrate="192k")
        
        # Create channel_03.mp3 from the first 57 seconds
        channel_03_audio.export(channel_03_path, format="mp3", bitrate="192k")
        
        print(f"✅ Updated channel 2: {channel_02_path.name} (real channel 2, 56 seconds)")
        print(f"✅ Created channel 3: {channel_03_path.name} (extracted from first 57 seconds)")
        
        # Verify the result
        print(f"\n=== Verification ===")
        channel_files = sorted(list(h391_dir.glob("channel_*.mp3")))
        print(f"Channel files in h391: {[f.name for f in channel_files]}")
        
        # Show durations of the new files
        for f in channel_files:
            if f.name.startswith("channel_") and not f.name.startswith("channel_02_original"):
                try:
                    file_audio = AudioSegment.from_mp3(f)
                    duration = len(file_audio) / 1000.0
                    print(f"  {f.name}: {duration:.2f} seconds")
                except:
                    print(f"  {f.name}: Error reading duration")
        
        print("\n🎉 h391 channel_02 splitting completed successfully!")
        print("Now h391 should have all 4 channels properly separated!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
