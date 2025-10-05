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
    print("=== h579 Channel 00 Splitting ===")
    
    # Check h579 directory
    h579_dir = Path("output/h579")
    print(f"Looking for: {h579_dir}")
    print(f"Directory exists: {h579_dir.exists()}")
    
    if not h579_dir.exists():
        print("❌ h579 directory not found!")
        return
    
    channel_00_file = h579_dir / "channel_00.mp3"
    print(f"Channel 00 file exists: {channel_00_file.exists()}")
    
    if not channel_00_file.exists():
        print("❌ channel_00.mp3 not found!")
        return
    
    try:
        # Load the audio file
        print("Loading channel_00.mp3...")
        audio = AudioSegment.from_mp3(channel_00_file)
        total_duration = len(audio)
        
        print(f"Total duration: {total_duration / 1000.0:.2f} seconds")
        
        # Split at 26 seconds:
        # - First 26 seconds = channel_00.mp3 (keep as is)
        # - Remaining 27 seconds = channel_01.mp3
        split_point = 26 * 1000  # Convert to milliseconds
        
        channel_00_audio = audio[:split_point]  # First 26 seconds
        channel_01_audio = audio[split_point:]  # Remaining 27 seconds
        
        print(f"Channel 00 (first 26s): {len(channel_00_audio) / 1000.0:.2f} seconds")
        print(f"Channel 01 (remaining 27s): {len(channel_01_audio) / 1000.0:.2f} seconds")
        
        # Backup original file
        backup_path = h579_dir / "channel_00_original_h579.mp3"
        audio.export(backup_path, format="mp3", bitrate="192k")
        print(f"📁 Backed up original to: {backup_path.name}")
        
        # Save the split files
        channel_00_path = h579_dir / "channel_00.mp3"
        channel_01_path = h579_dir / "channel_01.mp3"
        
        # Replace channel_00.mp3 with the first 26 seconds
        channel_00_audio.export(channel_00_path, format="mp3", bitrate="192k")
        
        # Create channel_01.mp3 from the remaining 27 seconds
        channel_01_audio.export(channel_01_path, format="mp3", bitrate="192k")
        
        print(f"✅ Updated channel 0: {channel_00_path.name} (first 26 seconds)")
        print(f"✅ Created channel 1: {channel_01_path.name} (remaining 27 seconds)")
        
        # Verify the result
        print(f"\n=== Verification ===")
        channel_files = sorted(list(h579_dir.glob("channel_*.mp3")))
        print(f"Channel files in h579: {[f.name for f in channel_files]}")
        
        # Show durations of the new files
        for f in channel_files:
            if f.name.startswith("channel_") and not f.name.startswith("channel_00_original"):
                try:
                    file_audio = AudioSegment.from_mp3(f)
                    duration = len(file_audio) / 1000.0
                    print(f"  {f.name}: {duration:.2f} seconds")
                except:
                    print(f"  {f.name}: Error reading duration")
        
        print("\n🎉 h579 channel_00 splitting completed successfully!")
        print("Now h579 should have all 4 channels properly separated!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()