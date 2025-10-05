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
    print("=== h99 Channel 00 Trimming (Remove first 62 seconds) ===")
    
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
        original_duration = len(audio) / 1000.0
        
        print(f"Original duration: {original_duration:.2f} seconds")
        
        trim_seconds = 62
        
        # Check if the file is long enough to trim
        if original_duration <= trim_seconds:
            print(f"⚠️  File too short to trim {trim_seconds}s, skipping")
            return
        
        # Create backup
        backup_path = h99_dir / "channel_00_backup.mp3"
        audio.export(backup_path, format="mp3", bitrate="192k")
        print(f"📁 Backed up to: {backup_path.name}")
        
        # Trim the first 62 seconds
        trim_ms = trim_seconds * 1000
        trimmed_audio = audio[trim_ms:]
        new_duration = len(trimmed_audio) / 1000.0
        
        print(f"Trimmed duration: {new_duration:.2f} seconds")
        print(f"Removed: {trim_seconds:.2f} seconds")
        
        # Save the trimmed audio
        trimmed_audio.export(channel_00_file, format="mp3", bitrate="192k")
        print(f"✅ Updated: {channel_00_file.name}")
        
        # Verify the result
        print(f"\n=== Verification ===")
        try:
            verify_audio = AudioSegment.from_mp3(channel_00_file)
            verify_duration = len(verify_audio) / 1000.0
            print(f"Final duration: {verify_duration:.2f} seconds")
        except:
            print("Error reading final duration")
        
        print("\n🎉 h99 channel_00 trimming completed successfully!")
        print("The first 62 seconds have been removed from channel_00.mp3!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
