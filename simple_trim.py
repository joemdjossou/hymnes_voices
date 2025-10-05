#!/usr/bin/env python3
from pathlib import Path

from pydub import AudioSegment

# Check h391 directory
h391_dir = Path('output/h391')
print(f"Checking directory: {h391_dir}")
print(f"Directory exists: {h391_dir.exists()}")

if h391_dir.exists():
    files = list(h391_dir.glob('channel_*.mp3'))
    print(f"Found {len(files)} files:")
    
    for f in files:
        try:
            audio = AudioSegment.from_mp3(f)
            duration = len(audio) / 1000.0
            print(f"  {f.name}: {duration:.2f}s")
        except Exception as e:
            print(f"  {f.name}: Error - {e}")
else:
    print("h391 directory not found")
