# Hymnes Voices - MIDI Channel Extractor & Web Player

This project extracts individual channels from MIDI files and converts each channel to a separate MP3 file. It includes a modern web interface for browsing and playing the extracted audio files.

## 🌐 Live Website

Visit the live website: **[Hymnes Voices Player](https://joemdjossou.github.io/hymnes_voices)**

## Features

### MIDI Processing

- Extracts all channels from MIDI files (excluding drum channel 10)
- Converts each channel to high-quality MP3 format
- Organizes output in separate folders for each MIDI file
- Handles large batches of MIDI files
- Preserves original timing and tempo

### Web Interface

- Browse 654 hymnes with individual channel access
- Search functionality to find specific hymnes
- Modern audio player with play/pause controls
- Responsive design for mobile and desktop
- Volume control and progress tracking
- Keyboard shortcuts (Space to play/pause, Escape to close modal)

## Quick Start

### 1. Extract MIDI Channels

```bash
# Install dependencies
pip install -r requirements.txt

# Process all MIDI files
python midi_channel_extractor.py midi output
```

### 2. Deploy Web Interface

```bash
# Generate hymnes data
python generate_data.py

# Commit and push to GitHub
git add .
git commit -m "Add web interface"
git push origin main
```

The website will be automatically deployed to GitHub Pages!

## Installation

1. Install Python 3.7 or higher
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### MIDI Processing

Process all MIDI files in the `midi` folder and save to `output` folder:

```bash
python midi_channel_extractor.py
```

Specify custom input and output directories:

```bash
python midi_channel_extractor.py /path/to/midi/files /path/to/output
```

Advanced options:

```bash
python midi_channel_extractor.py midi output --sample-rate 48000
```

### Web Interface

Generate hymnes data for the web interface:

```bash
python generate_data.py
```

Then deploy to GitHub Pages (see [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions).

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

## Project Structure

```
hymnes_voices/
├── index.html              # Main website interface
├── styles.css              # Styling and responsive design
├── script.js               # JavaScript functionality
├── hymnes_data.json        # Generated hymnes metadata
├── generate_data.py        # Script to generate hymnes data
├── midi_channel_extractor.py  # MIDI processing script
├── output/                 # MP3 files directory
│   ├── h1/
│   │   ├── channel_00.mp3
│   │   ├── channel_01.mp3
│   │   └── ...
│   ├── h2/
│   └── ...
├── .github/workflows/deploy.yml  # GitHub Actions workflow
├── _config.yml             # Jekyll configuration
└── DEPLOYMENT.md           # Deployment guide
```

## Example

To process your hymnes MIDI files and deploy the web interface:

```bash
# Install dependencies
pip install -r requirements.txt

# Process all MIDI files
python midi_channel_extractor.py midi output

# Generate web interface data
python generate_data.py

# Deploy to GitHub Pages
git add .
git commit -m "Add web interface"
git push origin main
```

This will create:

- MP3 files: `output/h1/channel_00.mp3`, `channel_01.mp3`, etc.
- Web interface accessible at: `https://yourusername.github.io/hymnes_voices`
