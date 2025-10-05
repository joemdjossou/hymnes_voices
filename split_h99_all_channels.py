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
    print("=== h99 All Channels Splitting ===")
    
    # Check h99 directory
    h99_dir = Path("output/h99")
    print(f"Looking for: {h99_dir}")
    print(f"Directory exists: {h99_dir.exists()}")
    
    if not h99_dir.exists():
        print("❌ h99 directory not found!")
        return
    
    channel_00_file = h99_dir / "channel_00.mp3"
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
        
        # Split into 4 segments of 64 seconds each:
        # - 0-64s = channel_00.mp3
        # - 64-128s = channel_01.mp3
        # - 128-192s = channel_02.mp3
        # - 192-256s = channel_03.mp3
        segment_duration = 64 * 1000  # Convert to milliseconds
        
        channel_00_audio = audio[:segment_duration]  # First 64 seconds
        channel_01_audio = audio[segment_duration:segment_duration*2]  # Next 64 seconds
        channel_02_audio = audio[segment_duration*2:segment_duration*3]  # Following 64 seconds
        channel_03_audio = audio[segment_duration*3:]  # Last 64 seconds
        
        print(f"Channel 00 (0-64s): {len(channel_00_audio) / 1000.0:.2f} seconds")
        print(f"Channel 01 (64-128s): {len(channel_01_audio) / 1000.0:.2f} seconds")
        print(f"Channel 02 (128-192s): {len(channel_02_audio) / 1000.0:.2f} seconds")
        print(f"Channel 03 (192-256s): {len(channel_03_audio) / 1000.0:.2f} seconds")
        
        # Backup original file
        backup_path = h99_dir / "channel_00_original_h99.mp3"
        audio.export(backup_path, format="mp3", bitrate="192k")
        print(f"📁 Backed up original to: {backup_path.name}")
        
        # Save all the split files
        channel_00_path = h99_dir / "channel_00.mp3"
        channel_01_path = h99_dir / "channel_01.mp3"
        channel_02_path = h99_dir / "channel_02.mp3"
        channel_03_path = h99_dir / "channel_03.mp3"
        
        # Replace channel_00.mp3 with the first 64 seconds
        channel_00_audio.export(channel_00_path, format="mp3", bitrate="192k")
        
        # Create the other channel files
        channel_01_audio.export(channel_01_path, format="mp3", bitrate="192k")
        channel_02_audio.export(channel_02_path, format="mp3", bitrate="192k")
        channel_03_audio.export(channel_03_path, format="mp3", bitrate="192k")
        
        print(f"✅ Updated channel 0: {channel_00_path.name} (0-64 seconds)")
        print(f"✅ Created channel 1: {channel_01_path.name} (64-128 seconds)")
        print(f"✅ Created channel 2: {channel_02_path.name} (128-192 seconds)")
        print(f"✅ Created channel 3: {channel_03_path.name} (192-256 seconds)")
        
        # Verify the result
        print(f"\n=== Verification ===")
        channel_files = sorted(list(h99_dir.glob("channel_*.mp3")))
        print(f"Channel files in h99: {[f.name for f in channel_files]}")
        
        # Show durations of the new files
        for f in channel_files:
            if f.name.startswith("channel_") and not f.name.startswith("channel_00_original"):
                try:
                    file_audio = AudioSegment.from_mp3(f)
                    duration = len(file_audio) / 1000.0
                    print(f"  {f.name}: {duration:.2f} seconds")
                except:
                    print(f"  {f.name}: Error reading duration")
        
        print("\n🎉 h99 all channels splitting completed successfully!")
        print("Now h99 should have all 4 channels properly separated!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
