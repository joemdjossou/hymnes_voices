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
    print("=== h567 Channel 02 Correct Splitting ===")
    
    # Check h567 directory
    h567_dir = Path("output/h567")
    print(f"Looking for: {h567_dir}")
    print(f"Directory exists: {h567_dir.exists()}")
    
    if not h567_dir.exists():
        print("❌ h567 directory not found!")
        return
    
    channel_02_file = h567_dir / "channel_02.mp3"
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
        
        # Split at 29 seconds:
        # - First 29 seconds = channel_02.mp3 (keep as is)
        # - Last 26 seconds = channel_03.mp3
        split_point = 29 * 1000  # Convert to milliseconds
        
        channel_02_audio = audio[:split_point]  # First 29 seconds
        channel_03_audio = audio[split_point:]  # Last 26 seconds
        
        print(f"Channel 02 (first 29s): {len(channel_02_audio) / 1000.0:.2f} seconds")
        print(f"Channel 03 (last 26s): {len(channel_03_audio) / 1000.0:.2f} seconds")
        
        # Backup original file
        backup_path = h567_dir / "channel_02_original_h567.mp3"
        audio.export(backup_path, format="mp3", bitrate="192k")
        print(f"📁 Backed up original to: {backup_path.name}")
        
        # Save the split files
        channel_02_path = h567_dir / "channel_02.mp3"
        channel_03_path = h567_dir / "channel_03.mp3"
        
        # Replace channel_02.mp3 with the first 28 seconds
        channel_02_audio.export(channel_02_path, format="mp3", bitrate="192k")
        
        # Create channel_03.mp3 from the last 27 seconds
        channel_03_audio.export(channel_03_path, format="mp3", bitrate="192k")
        
        print(f"✅ Updated channel 2: {channel_02_path.name} (first 29 seconds)")
        print(f"✅ Created channel 3: {channel_03_path.name} (last 26 seconds)")
        
        # Verify the result
        print(f"\n=== Verification ===")
        channel_files = sorted(list(h567_dir.glob("channel_*.mp3")))
        print(f"Channel files in h567: {[f.name for f in channel_files]}")
        
        # Show durations of the new files
        for f in channel_files:
            if f.name.startswith("channel_") and not f.name.startswith("channel_02_original"):
                try:
                    file_audio = AudioSegment.from_mp3(f)
                    duration = len(file_audio) / 1000.0
                    print(f"  {f.name}: {duration:.2f} seconds")
                except:
                    print(f"  {f.name}: Error reading duration")
        
        print("\n🎉 h567 channel_02 splitting completed successfully!")
        print("Now h567 should have all 4 channels properly separated!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
