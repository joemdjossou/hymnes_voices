#!/usr/bin/env python3
"""
Script to split mixed channel MP3 files for specific hymns (h125, h579).
Uses intelligent audio analysis to find the best split point.
"""

from pathlib import Path

from pydub import AudioSegment


def split_hymn_channel(hymn_number):
    """
    Split the channel_00.mp3 file for a specific hymn using intelligent audio analysis.
    """
    hymn_dir = Path(f"output/h{hymn_number}")
    channel_00_file = hymn_dir / "channel_00.mp3"
    
    if not channel_00_file.exists():
        print(f"❌ File not found: {channel_00_file}")
        return False
    
    print(f"=== Splitting h{hymn_number} channel_00.mp3 ===")
    
    try:
        # Load the audio file
        audio = AudioSegment.from_mp3(channel_00_file)
        total_duration = len(audio)
        
        print(f"Total duration: {total_duration / 1000.0:.2f} seconds")
        
        # Try to find a natural split point by analyzing the audio
        # Look for a quiet section in the middle
        middle_point = total_duration // 2
        search_window = min(5000, total_duration // 10)  # 5 seconds or 10% of total
        
        start_search = max(0, middle_point - search_window // 2)
        end_search = min(total_duration, middle_point + search_window // 2)
        
        print(f"Searching for quiet section between {start_search/1000.0:.2f}s and {end_search/1000.0:.2f}s")
        
        # Find the quietest point in the search window
        min_volume = float('inf')
        best_split_point = middle_point
        
        for i in range(start_search, end_search, 100):  # Check every 100ms
            segment = audio[i:i+100]
            volume = segment.dBFS
            if volume < min_volume:
                min_volume = volume
                best_split_point = i
        
        print(f"Found quietest point at {best_split_point/1000.0:.2f}s (volume: {min_volume:.1f} dBFS)")
        
        # Split at the quietest point
        channel_0 = audio[:best_split_point]
        channel_1 = audio[best_split_point:]
        
        print(f"Channel 0 duration: {len(channel_0) / 1000.0:.2f} seconds")
        print(f"Channel 1 duration: {len(channel_1) / 1000.0:.2f} seconds")
        
        # Backup original file
        backup_path = hymn_dir / f"channel_00_original_h{hymn_number}.mp3"
        audio.export(backup_path, format="mp3", bitrate="192k")
        print(f"📁 Backed up original to: {backup_path}")
        
        # Save the split files
        channel_0_path = hymn_dir / "channel_00.mp3"
        channel_1_path = hymn_dir / "channel_01.mp3"
        
        channel_0.export(channel_0_path, format="mp3", bitrate="192k")
        channel_1.export(channel_1_path, format="mp3", bitrate="192k")
        
        print(f"✅ Updated channel 0: {channel_0_path}")
        print(f"✅ Created channel 1: {channel_1_path}")
        
        # Verify the result
        print(f"\n=== Verification for h{hymn_number} ===")
        channel_files = sorted(list(hymn_dir.glob("channel_*.mp3")))
        print(f"Channel files in h{hymn_number}: {[f.name for f in channel_files]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing h{hymn_number}: {e}")
        return False


def main():
    # Process h125
    print("Processing h125...")
    success_125 = split_hymn_channel(125)
    
    print("\n" + "="*60 + "\n")
    
    # Process h579
    print("Processing h579...")
    success_579 = split_hymn_channel(579)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY:")
    print(f"h125: {'✅ Success' if success_125 else '❌ Failed'}")
    print(f"h579: {'✅ Success' if success_579 else '❌ Failed'}")
    
    if success_125 and success_579:
        print("\n🎉 Both hymns processed successfully!")
        print("Run 'python check_channels.py' to verify the results.")


if __name__ == "__main__":
    main()
