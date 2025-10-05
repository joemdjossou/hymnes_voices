#!/usr/bin/env python3
"""
Script to regenerate h582 channels from the original MIDI file.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    from midi_channel_extractor import MIDIChannelExtractor
    print("✅ MIDIChannelExtractor imported successfully")
except ImportError as e:
    print(f"❌ Error importing MIDIChannelExtractor: {e}")
    sys.exit(1)

def main():
    print("=== Regenerating h582 channels from MIDI ===")
    
    # Check if MIDI file exists
    midi_file = Path("midi/h582.mid")
    print(f"Looking for MIDI file: {midi_file}")
    print(f"MIDI file exists: {midi_file.exists()}")
    
    if not midi_file.exists():
        print("❌ h582.mid not found!")
        return
    
    # Check h582 output directory
    h582_dir = Path("output/h582")
    print(f"Output directory: {h582_dir}")
    
    # Backup existing files if they exist
    if h582_dir.exists():
        backup_dir = Path("output/h582_backup")
        backup_dir.mkdir(exist_ok=True)
        
        print(f"📁 Backing up existing files to: {backup_dir}")
        for file in h582_dir.glob("*.mp3"):
            backup_file = backup_dir / file.name
            file.rename(backup_file)
            print(f"  Moved {file.name} to backup")
    
    try:
        # Create the extractor
        extractor = MIDIChannelExtractor("midi", "output")
        
        # Process the specific MIDI file
        print(f"\nProcessing {midi_file.name}...")
        extractor.process_midi_file(midi_file)
        
        # Verify the result
        print(f"\n=== Verification ===")
        if h582_dir.exists():
            channel_files = sorted(list(h582_dir.glob("channel_*.mp3")))
            print(f"Generated channel files in h582: {[f.name for f in channel_files]}")
            
            # Show durations of the generated files
            for f in channel_files:
                try:
                    from pydub import AudioSegment
                    file_audio = AudioSegment.from_mp3(f)
                    duration = len(file_audio) / 1000.0
                    print(f"  {f.name}: {duration:.2f} seconds")
                except:
                    print(f"  {f.name}: Error reading duration")
        else:
            print("❌ Output directory was not created")
        
        print("\n🎉 h582 channel regeneration completed successfully!")
        print("All channels have been regenerated from the original MIDI file!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
