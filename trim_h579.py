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
    print("=== h579 Channel Trimming (Remove first 24 seconds) ===")
    
    # Check h579 directory
    h579_dir = Path("output/h579")
    print(f"Looking for: {h579_dir}")
    print(f"Directory exists: {h579_dir.exists()}")
    
    if not h579_dir.exists():
        print("❌ h579 directory not found!")
        return
    
    # Find all channel files
    channel_files = sorted(list(h579_dir.glob("channel_*.mp3")))
    print(f"Found {len(channel_files)} channel files:")
    for f in channel_files:
        print(f"  - {f.name}")
    
    if not channel_files:
        print("❌ No channel files found!")
        return
    
    trim_seconds = 24
    success_count = 0
    
    for channel_file in channel_files:
        print(f"\nProcessing {channel_file.name}...")
        
        try:
            # Load the audio file
            audio = AudioSegment.from_mp3(channel_file)
            original_duration = len(audio) / 1000.0
            
            print(f"  Original duration: {original_duration:.2f} seconds")
            
            # Check if the file is long enough to trim
            if original_duration <= trim_seconds:
                print(f"  ⚠️  File too short to trim {trim_seconds}s, skipping")
                continue
            
            # Create backup
            backup_path = channel_file.parent / f"{channel_file.stem}_backup.mp3"
            audio.export(backup_path, format="mp3", bitrate="192k")
            print(f"  📁 Backed up to: {backup_path.name}")
            
            # Trim the first 24 seconds
            trim_ms = trim_seconds * 1000
            trimmed_audio = audio[trim_ms:]
            new_duration = len(trimmed_audio) / 1000.0
            
            print(f"  Trimmed duration: {new_duration:.2f} seconds")
            print(f"  Removed: {trim_seconds:.2f} seconds")
            
            # Save the trimmed audio
            trimmed_audio.export(channel_file, format="mp3", bitrate="192k")
            print(f"  ✅ Updated: {channel_file.name}")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ Error processing {channel_file.name}: {e}")
    
    print(f"\n=== Summary ===")
    print(f"Successfully processed: {success_count}/{len(channel_files)} files")
    
    # Verify the result
    print(f"\n=== Verification ===")
    updated_files = sorted(list(h579_dir.glob("channel_*.mp3")))
    print(f"Channel files in h579: {[f.name for f in updated_files]}")
    
    # Show durations of the updated files
    for f in updated_files:
        if not f.name.endswith("_backup.mp3"):
            try:
                file_audio = AudioSegment.from_mp3(f)
                duration = len(file_audio) / 1000.0
                print(f"  {f.name}: {duration:.2f} seconds")
            except:
                print(f"  {f.name}: Error reading duration")
    
    if success_count > 0:
        print("\n🎉 h579 trimming completed successfully!")
        print("All channels now have the first 24 seconds removed!")
    else:
        print("\n❌ No files were processed")

if __name__ == "__main__":
    main()
