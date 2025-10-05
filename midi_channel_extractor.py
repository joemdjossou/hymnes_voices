#!/usr/bin/env python3
"""
MIDI Channel Extractor and MP3 Converter

This script processes MIDI files and extracts each channel as a separate MP3 file.
For each MIDI file, it creates a folder containing all the individual channels as MP3 files.

Requirements:
- mido: For MIDI file processing
- pretty_midi: For MIDI to audio conversion
- librosa: For audio processing
- soundfile: For audio file I/O
- pydub: For audio format conversion

Usage:
    python midi_channel_extractor.py [input_directory] [output_directory]
"""

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path

import mido
import numpy as np
import pretty_midi
import soundfile as sf
from pydub import AudioSegment
from pydub.generators import Sine


class MIDIChannelExtractor:
    def __init__(self, input_dir, output_dir, sample_rate=44100):
        """
        Initialize the MIDI channel extractor.
        
        Args:
            input_dir (str): Directory containing MIDI files
            output_dir (str): Directory to save extracted channels
            sample_rate (int): Sample rate for audio conversion (default: 44100)
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.sample_rate = sample_rate
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def get_midi_files(self):
        """Get all MIDI files from the input directory."""
        return list(self.input_dir.glob("*.mid")) + list(self.input_dir.glob("*.midi"))
    
    def analyze_midi_channels(self, midi_file):
        """
        Analyze a MIDI file to find which channels contain data and when the first note starts.
        
        Args:
            midi_file (Path): Path to the MIDI file
            
        Returns:
            tuple: (list of channel numbers, first_note_time_in_seconds)
        """
        try:
            mid = mido.MidiFile(str(midi_file))
            channels_with_data = set()
            first_note_time = None
            
            # Convert ticks to seconds
            ticks_per_beat = mid.ticks_per_beat
            tempo = 500000  # Default tempo (120 BPM)
            
            current_time_ticks = 0
            current_time_seconds = 0
            
            for track in mid.tracks:
                current_time_ticks = 0
                current_time_seconds = 0
                
                for msg in track:
                    # Update time
                    current_time_ticks += msg.time
                    current_time_seconds = mido.tick2second(current_time_ticks, ticks_per_beat, tempo)
                    
                    # Check for tempo changes
                    if msg.type == 'set_tempo':
                        tempo = msg.tempo
                        current_time_seconds = mido.tick2second(current_time_ticks, ticks_per_beat, tempo)
                    
                    # Check for note events
                    if hasattr(msg, 'channel') and msg.type in ['note_on', 'note_off', 'control_change', 'program_change']:
                        if msg.channel != 9:  # Skip drum channel (channel 10, 0-indexed)
                            channels_with_data.add(msg.channel)
                            
                            # Track the first note_on event
                            if msg.type == 'note_on' and msg.velocity > 0 and first_note_time is None:
                                first_note_time = current_time_seconds
            
            return sorted(list(channels_with_data)), first_note_time or 0.0
        except Exception as e:
            print(f"Error analyzing {midi_file}: {e}")
            return [], 0.0
    
    def create_channel_midi(self, midi_file, target_channel):
        """
        Create a new MIDI file containing only the specified channel.
        
        Args:
            midi_file (Path): Original MIDI file
            target_channel (int): Channel number to extract
            
        Returns:
            Path: Path to the temporary MIDI file with only the target channel
        """
        try:
            mid = mido.MidiFile(str(midi_file))
            new_mid = mido.MidiFile()
            new_mid.ticks_per_beat = mid.ticks_per_beat
            
            # Create a new track for the target channel
            new_track = mido.MidiTrack()
            
            # Copy tempo and time signature messages
            for track in mid.tracks:
                for msg in track:
                    if msg.type in ['set_tempo', 'time_signature', 'key_signature']:
                        new_track.append(msg)
            
            # Copy messages from the target channel
            for track in mid.tracks:
                for msg in track:
                    if (hasattr(msg, 'channel') and msg.channel == target_channel and 
                        msg.type in ['note_on', 'note_off', 'control_change', 'program_change']):
                        new_track.append(msg)
                    elif msg.type == 'end_of_track':
                        # Only add end_of_track at the very end
                        if len(new_track) > 0 and new_track[-1].type != 'end_of_track':
                            new_track.append(msg)
            
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.mid', delete=False)
            new_mid.tracks = [new_track]
            new_mid.save(temp_file.name)
            temp_file.close()
            
            return Path(temp_file.name)
            
        except Exception as e:
            print(f"Error creating channel MIDI for {midi_file}, channel {target_channel}: {e}")
            return None
    
    def midi_to_audio(self, midi_file, duration=None, start_time=0.0):
        """
        Convert MIDI file to audio using pretty_midi.
        
        Args:
            midi_file (Path): Path to MIDI file
            duration (float): Maximum duration in seconds (optional)
            start_time (float): Start time in seconds to crop from beginning
            
        Returns:
            np.ndarray: Audio data as numpy array
        """
        try:
            pm = pretty_midi.PrettyMIDI(str(midi_file))
            
            # Get duration
            if duration is None:
                duration = pm.get_end_time()
            
            # Synthesize audio
            audio_data = pm.synthesize(fs=self.sample_rate)
            
            # Crop from start_time if specified
            if start_time > 0:
                start_sample = int(start_time * self.sample_rate)
                audio_data = audio_data[start_sample:]
            
            # Ensure we have the right duration
            target_length = int(duration * self.sample_rate)
            if len(audio_data) > target_length:
                audio_data = audio_data[:target_length]
            elif len(audio_data) < target_length:
                # Pad with silence
                padding = np.zeros(target_length - len(audio_data))
                audio_data = np.concatenate([audio_data, padding])
            
            return audio_data
            
        except Exception as e:
            print(f"Error converting MIDI to audio {midi_file}: {e}")
            return None
    
    def audio_to_mp3(self, audio_data, output_path):
        """
        Convert audio data to MP3 format.
        
        Args:
            audio_data (np.ndarray): Audio data
            output_path (Path): Output MP3 file path
        """
        try:
            # Ensure audio data is in the right format
            if len(audio_data.shape) == 1:
                # Mono audio
                audio_data = audio_data.astype(np.float32)
                # Normalize to prevent clipping
                if np.max(np.abs(audio_data)) > 0:
                    audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8
            else:
                # Stereo audio
                audio_data = audio_data.astype(np.float32)
                if np.max(np.abs(audio_data)) > 0:
                    audio_data = audio_data / np.max(np.abs(audio_data)) * 0.8
            
            # Convert to 16-bit PCM
            audio_data_16bit = (audio_data * 32767).astype(np.int16)
            
            # Convert numpy array to AudioSegment
            audio_segment = AudioSegment(
                audio_data_16bit.tobytes(),
                frame_rate=self.sample_rate,
                sample_width=2,  # 16-bit = 2 bytes
                channels=1 if len(audio_data.shape) == 1 else audio_data.shape[1]
            )
            
            # Export as MP3
            audio_segment.export(str(output_path), format="mp3", bitrate="192k")
            
        except Exception as e:
            print(f"Error converting to MP3 {output_path}: {e}")
    
    def process_midi_file(self, midi_file):
        """
        Process a single MIDI file and extract all channels.
        
        Args:
            midi_file (Path): Path to MIDI file
        """
        print(f"Processing {midi_file.name}...")
        
        # Create output folder for this MIDI file
        file_stem = midi_file.stem
        output_folder = self.output_dir / file_stem
        output_folder.mkdir(exist_ok=True)
        
        # Analyze channels and get first note time
        channels, first_note_time = self.analyze_midi_channels(midi_file)
        
        if not channels:
            print(f"No channels found in {midi_file.name}")
            return
        
        print(f"Found {len(channels)} channels: {channels}")
        print(f"First note starts at: {first_note_time:.3f} seconds")
        
        # Process each channel
        for channel in channels:
            print(f"  Processing channel {channel}...")
            
            # Create temporary MIDI file with only this channel
            temp_midi = self.create_channel_midi(midi_file, channel)
            
            if temp_midi is None:
                continue
            
            try:
                # Convert to audio, cropping from first note time
                audio_data = self.midi_to_audio(temp_midi, start_time=first_note_time)
                
                if audio_data is not None:
                    # Save as MP3
                    output_path = output_folder / f"channel_{channel:02d}.mp3"
                    self.audio_to_mp3(audio_data, output_path)
                    print(f"    Saved: {output_path}")
                else:
                    print(f"    Failed to convert channel {channel} to audio")
                    
            finally:
                # Clean up temporary file
                if temp_midi.exists():
                    temp_midi.unlink()
    
    def process_all_files(self):
        """Process all MIDI files in the input directory."""
        midi_files = self.get_midi_files()
        
        if not midi_files:
            print(f"No MIDI files found in {self.input_dir}")
            return
        
        print(f"Found {len(midi_files)} MIDI files")
        
        for i, midi_file in enumerate(midi_files, 1):
            print(f"\n[{i}/{len(midi_files)}] Processing {midi_file.name}")
            try:
                self.process_midi_file(midi_file)
            except Exception as e:
                print(f"Error processing {midi_file.name}: {e}")
                continue
        
        print(f"\nProcessing complete! Check output directory: {self.output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Extract MIDI channels and convert to MP3")
    parser.add_argument("input_dir", nargs="?", default="midi", 
                       help="Input directory containing MIDI files (default: midi)")
    parser.add_argument("output_dir", nargs="?", default="output", 
                       help="Output directory for MP3 files (default: output)")
    parser.add_argument("--sample-rate", type=int, default=44100,
                       help="Sample rate for audio conversion (default: 44100)")
    
    args = parser.parse_args()
    
    # Check if input directory exists
    if not os.path.exists(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist")
        sys.exit(1)
    
    # Create extractor and process files
    extractor = MIDIChannelExtractor(args.input_dir, args.output_dir, args.sample_rate)
    extractor.process_all_files()


if __name__ == "__main__":
    main()
