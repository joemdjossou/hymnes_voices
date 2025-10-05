#!/usr/bin/env python3
"""
Script to trim the first 54 seconds from all channels in h391.
"""

from pathlib import Path

from pydub import AudioSegment


def trim_h391_channels():
    """
    Remove the first 54 seconds from all channel files in h391.
    """
    hymn_dir = Path("output/h391")
    trim_seconds = 54
    
    if not hymn_dir.exists():
        print(f"❌ Directory not found: {hymn_dir}")
        return False
    
    print(f"=== Trimming h391 channels (removing first {trim_seconds} seconds) ===")
    
    # Find all channel files
    channel_files = sorted(list(hymn_dir.glob("channel_*.mp3")))
    
    if not channel_files:
        print(f"❌ No channel files found in {hymn_dir}")
        return False
    
    print(f"Found {len(channel_files)} channel files:")
    for f in channel_files:
        print(f"  - {f.name}")
    
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
            
            # Trim the first 54 seconds
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
    updated_files = sorted(list(hymn_dir.glob("channel_*.mp3")))
    print(f"Channel files in h391: {[f.name for f in updated_files]}")
    
    return success_count > 0


def main():
    success = trim_h391_channels()
    
    if success:
        print("\n🎉 h391 trimming completed successfully!")
        print("Run 'python check_channels.py' to verify the results.")
    else:
        print("\n❌ h391 trimming failed!")


if __name__ == "__main__":
    main()
