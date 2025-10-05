#!/usr/bin/env python3
"""
Script to split a mixed channel MP3 file into two separate channels.
This is useful when channel_00.mp3 contains both channel 0 and channel 1 mixed together.
"""

import argparse
from pathlib import Path

import numpy as np
from pydub import AudioSegment


def split_mixed_channel(input_file, output_dir, split_ratio=0.5):
    """
    Split a mixed channel MP3 into two separate files.
    
    Args:
        input_file (Path): Path to the mixed channel MP3 file
        output_dir (Path): Directory to save the split files
        split_ratio (float): Ratio to split the audio (0.5 = split in half)
    """
    print(f"Splitting {input_file.name}...")
    
    try:
        # Load the audio file
        audio = AudioSegment.from_mp3(input_file)
        total_duration = len(audio)
        
        print(f"Original duration: {total_duration / 1000.0:.2f} seconds")
        
        # Calculate split point
        split_point_ms = int(total_duration * split_ratio)
        
        # Split the audio
        channel_0 = audio[:split_point_ms]
        channel_1 = audio[split_point_ms:]
        
        print(f"Split point: {split_point_ms / 1000.0:.2f} seconds")
        print(f"Channel 0 duration: {len(channel_0) / 1000.0:.2f} seconds")
        print(f"Channel 1 duration: {len(channel_1) / 1000.0:.2f} seconds")
        
        # Save the split files
        channel_0_path = output_dir / "channel_00_split.mp3"
        channel_1_path = output_dir / "channel_01_split.mp3"
        
        channel_0.export(channel_0_path, format="mp3", bitrate="192k")
        channel_1.export(channel_1_path, format="mp3", bitrate="192k")
        
        print(f"✅ Saved channel 0: {channel_0_path}")
        print(f"✅ Saved channel 1: {channel_1_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error splitting {input_file.name}: {e}")
        return False


def split_h111_channels():
    """
    Specifically split the h111 channel_00.mp3 file.
    """
    h111_dir = Path("output/h111")
    channel_00_file = h111_dir / "channel_00.mp3"
    
    if not channel_00_file.exists():
        print(f"❌ File not found: {channel_00_file}")
        return False
    
    print("=== Splitting h111 channel_00.mp3 ===")
    
    # First, let's analyze the audio to find a good split point
    try:
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
        backup_path = h111_dir / "channel_00_original.mp3"
        audio.export(backup_path, format="mp3", bitrate="192k")
        print(f"📁 Backed up original to: {backup_path}")
        
        # Save the split files
        channel_0_path = h111_dir / "channel_00.mp3"
        channel_1_path = h111_dir / "channel_01.mp3"
        
        channel_0.export(channel_0_path, format="mp3", bitrate="192k")
        channel_1.export(channel_1_path, format="mp3", bitrate="192k")
        
        print(f"✅ Updated channel 0: {channel_0_path}")
        print(f"✅ Created channel 1: {channel_1_path}")
        
        # Verify the result
        print("\n=== Verification ===")
        channel_files = sorted(list(h111_dir.glob("channel_*.mp3")))
        print(f"Channel files in h111: {[f.name for f in channel_files]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing h111: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Split mixed channel MP3 files into separate channels.")
    parser.add_argument("--hymn", type=str, help="Specific hymn to process (e.g., h111)")
    parser.add_argument("--input", type=str, help="Input MP3 file to split")
    parser.add_argument("--output_dir", type=str, default="output", help="Output directory")
    parser.add_argument("--split_ratio", type=float, default=0.5, help="Split ratio (0.5 = split in half)")
    
    args = parser.parse_args()
    
    if args.hymn:
        if args.hymn == "h111":
            split_h111_channels()
        else:
            print(f"Specific hymn processing for {args.hymn} not implemented yet.")
    elif args.input:
        input_file = Path(args.input)
        output_dir = Path(args.output_dir)
        split_mixed_channel(input_file, output_dir, args.split_ratio)
    else:
        print("Please specify either --hymn or --input file")
        print("Example: python split_mixed_channel.py --hymn h111")


if __name__ == "__main__":
    main()
