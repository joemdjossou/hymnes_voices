#!/usr/bin/env python3
"""
Script to split h391 channel_02.mp3 to extract channel_03 from the first 57 seconds.
"""

from pathlib import Path

from pydub import AudioSegment


def split_h391_channel02():
    """
    Split h391 channel_02.mp3 to extract channel_03 from the first 57 seconds.
    """
    hymn_dir = Path("output/h391")
    channel_02_file = hymn_dir / "channel_02.mp3"
    
    if not channel_02_file.exists():
        print(f"❌ File not found: {channel_02_file}")
        return False
    
    print("=== Splitting h391 channel_02.mp3 to extract channel_03 ===")
    
    try:
        # Load the audio file
        audio = AudioSegment.from_mp3(channel_02_file)
        total_duration = len(audio)
        
        print(f"Total duration: {total_duration / 1000.0:.2f} seconds")
        
        # Extract the first 57 seconds (this contains both channel 2 and 3)
        first_57_seconds = 57 * 1000  # Convert to milliseconds
        mixed_audio = audio[:first_57_seconds]
        
        # The remaining audio is pure channel 2
        pure_channel_2 = audio[first_57_seconds:]
        
        print(f"Mixed audio (first 57s): {len(mixed_audio) / 1000.0:.2f} seconds")
        print(f"Pure channel 2 (remaining): {len(pure_channel_2) / 1000.0:.2f} seconds")
        
        # For the mixed audio, we need to split it to separate channel 2 and 3
        # Let's try to find a good split point in the mixed section
        middle_point = len(mixed_audio) // 2
        search_window = min(3000, len(mixed_audio) // 4)  # 3 seconds or 25% of mixed audio
        
        start_search = max(0, middle_point - search_window // 2)
        end_search = min(len(mixed_audio), middle_point + search_window // 2)
        
        print(f"Searching for split point in mixed audio between {start_search/1000.0:.2f}s and {end_search/1000.0:.2f}s")
        
        # Find the quietest point in the mixed section
        min_volume = float('inf')
        best_split_point = middle_point
        
        for i in range(start_search, end_search, 100):  # Check every 100ms
            segment = mixed_audio[i:i+100]
            volume = segment.dBFS
            if volume < min_volume:
                min_volume = volume
                best_split_point = i
        
        print(f"Found split point at {best_split_point/1000.0:.2f}s (volume: {min_volume:.1f} dBFS)")
        
        # Split the mixed audio
        channel_2_part1 = mixed_audio[:best_split_point]
        channel_3_part1 = mixed_audio[best_split_point:]
        
        # Combine channel 2 parts
        complete_channel_2 = channel_2_part1 + pure_channel_2
        
        print(f"Channel 2 part 1: {len(channel_2_part1) / 1000.0:.2f} seconds")
        print(f"Channel 2 part 2: {len(pure_channel_2) / 1000.0:.2f} seconds")
        print(f"Complete channel 2: {len(complete_channel_2) / 1000.0:.2f} seconds")
        print(f"Channel 3: {len(channel_3_part1) / 1000.0:.2f} seconds")
        
        # Backup original file
        backup_path = hymn_dir / "channel_02_original_h391.mp3"
        audio.export(backup_path, format="mp3", bitrate="192k")
        print(f"📁 Backed up original to: {backup_path}")
        
        # Save the split files
        channel_2_path = hymn_dir / "channel_02.mp3"
        channel_3_path = hymn_dir / "channel_03.mp3"
        
        complete_channel_2.export(channel_2_path, format="mp3", bitrate="192k")
        channel_3_part1.export(channel_3_path, format="mp3", bitrate="192k")
        
        print(f"✅ Updated channel 2: {channel_2_path}")
        print(f"✅ Created channel 3: {channel_3_path}")
        
        # Verify the result
        print(f"\n=== Verification ===")
        channel_files = sorted(list(hymn_dir.glob("channel_*.mp3")))
        print(f"Channel files in h391: {[f.name for f in channel_files]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing h391 channel_02: {e}")
        return False


def main():
    success = split_h391_channel02()
    
    if success:
        print("\n🎉 h391 channel_02 splitting completed successfully!")
        print("Run 'python check_channels.py' to verify the results.")
    else:
        print("\n❌ h391 channel_02 splitting failed!")


if __name__ == "__main__":
    main()
