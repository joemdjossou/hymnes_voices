#!/usr/bin/env python3
"""
Script to check which hymn folders have less than 4 channels.
This helps identify missing or incomplete channel files.
"""

import argparse
from collections import defaultdict
from pathlib import Path


def check_channels_in_folders(output_dir="output", min_channels=4):
    """
    Check all hymn folders and report which ones have fewer than the minimum number of channels.
    
    Args:
        output_dir (str): Directory containing hymn folders
        min_channels (int): Minimum expected number of channels
    """
    output_path = Path(output_dir)
    
    if not output_path.exists():
        print(f"Error: Output directory '{output_dir}' does not exist!")
        return
    
    print(f"Checking hymn folders in: {output_path}")
    print(f"Looking for folders with less than {min_channels} channels")
    print("=" * 60)
    
    # Statistics
    total_folders = 0
    complete_folders = 0
    incomplete_folders = 0
    channel_counts = defaultdict(int)
    
    # Find all hymn folders (h1, h2, h3, etc.)
    hymn_folders = sorted([f for f in output_path.iterdir() 
                          if f.is_dir() and f.name.startswith('h') and f.name[1:].isdigit()])
    
    print(f"Found {len(hymn_folders)} hymn folders")
    print()
    
    # Check each folder
    for folder in hymn_folders:
        total_folders += 1
        
        # Find all channel files
        channel_files = list(folder.glob("channel_*.mp3"))
        channel_count = len(channel_files)
        
        # Track channel count distribution
        channel_counts[channel_count] += 1
        
        if channel_count < min_channels:
            incomplete_folders += 1
            print(f"❌ {folder.name}: {channel_count} channels (missing {min_channels - channel_count})")
            
            # List the actual channel files found
            if channel_files:
                channel_nums = sorted([int(f.stem.split('_')[1]) for f in channel_files])
                print(f"   Found channels: {channel_nums}")
                
                # Show which channels are missing
                expected_channels = list(range(min_channels))
                missing_channels = [ch for ch in expected_channels if ch not in channel_nums]
                if missing_channels:
                    print(f"   Missing channels: {missing_channels}")
            else:
                print(f"   No channel files found!")
        else:
            complete_folders += 1
            if channel_count > min_channels:
                print(f"✅ {folder.name}: {channel_count} channels (more than expected)")
            else:
                print(f"✅ {folder.name}: {channel_count} channels (complete)")
    
    # Summary statistics
    print()
    print("=" * 60)
    print("SUMMARY:")
    print(f"Total folders checked: {total_folders}")
    print(f"Complete folders (≥{min_channels} channels): {complete_folders}")
    print(f"Incomplete folders (<{min_channels} channels): {incomplete_folders}")
    print()
    
    print("Channel count distribution:")
    for count in sorted(channel_counts.keys()):
        folders = channel_counts[count]
        percentage = (folders / total_folders) * 100
        status = "✅" if count >= min_channels else "❌"
        print(f"  {status} {count} channels: {folders} folders ({percentage:.1f}%)")
    
    # List folders with specific channel counts if requested
    if incomplete_folders > 0:
        print()
        print("DETAILED BREAKDOWN:")
        for count in sorted(channel_counts.keys()):
            if count < min_channels:
                print(f"\nFolders with {count} channels:")
                for folder in hymn_folders:
                    channel_files = list(folder.glob("channel_*.mp3"))
                    if len(channel_files) == count:
                        print(f"  - {folder.name}")


def main():
    parser = argparse.ArgumentParser(description="Check which hymn folders have less than the expected number of channels.")
    parser.add_argument("--output_dir", type=str, default="output", 
                       help="Directory containing hymn folders (default: output)")
    parser.add_argument("--min_channels", type=int, default=4, 
                       help="Minimum expected number of channels (default: 4)")
    parser.add_argument("--show_all", action="store_true", 
                       help="Show all folders, not just incomplete ones")
    
    args = parser.parse_args()
    
    check_channels_in_folders(args.output_dir, args.min_channels)


if __name__ == "__main__":
    main()
