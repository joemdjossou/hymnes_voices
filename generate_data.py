#!/usr/bin/env python3
"""
Generate hymnes data for the web interface.
This script scans the output directory and creates a JSON file with all hymnes and their channels.
"""

import json
import os
from pathlib import Path


def generate_hymnes_data():
    """Generate hymnes data from the output directory."""
    output_dir = Path("output")
    hymnes_data = []
    
    if not output_dir.exists():
        print("Output directory not found!")
        return []
    
    # Get all hymne directories
    hymne_dirs = sorted([d for d in output_dir.iterdir() if d.is_dir() and d.name.startswith('h')])
    
    for hymne_dir in hymne_dirs:
        hymne_name = hymne_dir.name
        hymne_number = int(hymne_name[1:])  # Extract number from 'h1', 'h2', etc.
        
        # Get all MP3 files in this hymne directory
        mp3_files = list(hymne_dir.glob("*.mp3"))
        channels = []
        
        for mp3_file in sorted(mp3_files):
            channel_name = mp3_file.stem  # e.g., 'channel_00'
            channel_number = int(channel_name.split('_')[1])  # Extract number from 'channel_00'
            
            channels.append({
                "number": channel_number,
                "name": f"Channel {channel_number:02d}",
                "filename": mp3_file.name,
                "url": f"output/{hymne_name}/{mp3_file.name}"
            })
        
        hymnes_data.append({
            "name": hymne_name,
            "number": hymne_number,
            "channels": len(channels),
            "channelFiles": channels
        })
    
    return hymnes_data

def main():
    """Main function to generate and save hymnes data."""
    print("Generating hymnes data...")
    
    hymnes_data = generate_hymnes_data()
    
    if not hymnes_data:
        print("No hymnes data found!")
        return
    
    # Save to JSON file
    output_file = "hymnes_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(hymnes_data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated data for {len(hymnes_data)} hymnes")
    print(f"Data saved to {output_file}")
    
    # Print summary
    total_channels = sum(hymne['channels'] for hymne in hymnes_data)
    print(f"Total channels: {total_channels}")

if __name__ == "__main__":
    main()
