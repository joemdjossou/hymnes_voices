# MIDI Channel Extractor

This Python script extracts individual channels from MIDI files and converts each channel to a separate MP3 file. For each MIDI file, it creates a folder containing all the individual channels as MP3 files.

## Features

- Extracts all channels from MIDI files (excluding drum channel 10)
- Converts each channel to high-quality MP3 format
- Organizes output in separate folders for each MIDI file
- Handles large batches of MIDI files
- Preserves original timing and tempo

## Installation

1. Install Python 3.7 or higher
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Process all MIDI files in the `midi` folder and save to `output` folder:

```bash
python midi_channel_extractor.py
```

### Custom Directories

Specify custom input and output directories:

```bash
python midi_channel_extractor.py /path/to/midi/files /path/to/output
```

### Advanced Options

```bash
python midi_channel_extractor.py midi output --sample-rate 48000
```

## Output Structure

For each MIDI file (e.g., `h1.mid`), the script creates:

```
output/
└── h1/
    ├── channel_00.mp3
    ├── channel_01.mp3
    ├── channel_02.mp3
    └── ...
```

## Requirements

- **mido**: MIDI file processing
- **pretty_midi**: MIDI to audio synthesis
- **librosa**: Audio processing
- **soundfile**: Audio file I/O
- **pydub**: Audio format conversion
- **numpy**: Numerical operations

## How It Works

1. **Analysis**: The script analyzes each MIDI file to identify which channels contain musical data
2. **Extraction**: For each channel, it creates a temporary MIDI file containing only that channel's data
3. **Synthesis**: Each channel is converted to audio using a high-quality synthesizer
4. **Conversion**: The audio is exported as MP3 format with 192kbps bitrate
5. **Organization**: All channels for each MIDI file are saved in a dedicated folder

## Notes

- The script skips MIDI channel 10 (drum channel) as it typically contains percussion data
- Each channel is processed independently to ensure clean separation
- The output maintains the original timing and tempo of the MIDI file
- Large batches of files are processed sequentially to avoid memory issues

## Troubleshooting

If you encounter issues:

1. **Missing dependencies**: Run `pip install -r requirements.txt`
2. **Audio quality**: Adjust the sample rate with `--sample-rate` parameter
3. **Memory issues**: Process files in smaller batches
4. **File permissions**: Ensure write permissions for the output directory

## Example

To process your hymnes MIDI files:

```bash
# Install dependencies
pip install -r requirements.txt

# Process all MIDI files
python midi_channel_extractor.py midi output

# This will create folders like:
# output/h1/channel_00.mp3, channel_01.mp3, etc.
# output/h2/channel_00.mp3, channel_01.mp3, etc.
# ... and so on for all 654 MIDI files
```
