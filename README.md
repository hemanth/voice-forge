# Voice Forge

A powerful command-line interface for [Chatterbox TTS](https://github.com/resemble-ai/chatterbox) - Resemble AI's state-of-the-art open-source Text-to-Speech model.

## Features

- 🎯 **Simple CLI interface** - Generate speech from text with a single command
- 🔊 **Automatic audio playback** - Hear your generated speech immediately
- 💾 **Audio file export** - Save generated speech to WAV files
- 🎭 **Voice cloning** - Use reference audio files for voice conversion
- ⚙️ **Customizable parameters** - Control exaggeration and CFG weight
- 📄 **File input support** - Read text from files
- 🖥️ **Cross-platform** - Works on macOS, Linux, and Windows
- 🎮 **Multiple audio backends** - Supports pygame, playsound, and system audio players

## Installation

### Prerequisites

- Python 3.8 or higher
- CUDA (optional, for GPU acceleration)

### Install Dependencies

```bash
# Install core dependencies
pip install chatterbox-tts torch torchaudio

# Install optional audio playback libraries
pip install pygame playsound

# Or install all dependencies at once
pip install -r requirements.txt
```

### Install Voice Forge

```bash
# Install from PyPI (once published)
pip install voice-forge

# Or install from source
pip install -e .

# Or run directly from the package
python -m voice_forge --help
```

## Usage

### Basic Usage

```bash
# Generate and play speech from text
voice-forge "Hello, world! This is Voice Forge with Chatterbox TTS."

# Save audio to file
voice-forge "Hello, world!" --save output.wav

# Read text from file
voice-forge --file input.txt --save output.wav
```

### Voice Cloning

```bash
# Use a reference voice
voice-forge "Hello, world!" --voice reference.wav

# Combine voice cloning with file output
voice-forge "Hello, world!" --voice reference.wav --save cloned_output.wav
```

### Advanced Parameters

```bash
# Adjust exaggeration and CFG weight
voice-forge "Hello, world!" --exaggeration 0.7 --cfg-weight 0.3

# Use CPU instead of GPU
voice-forge "Hello, world!" --device cpu

# Save without playing
voice-forge "Hello, world!" --save output.wav --no-play
```

### Audio Playback Options

```bash
# Use specific audio backend
voice-forge "Hello, world!" --audio-method pygame
voice-forge "Hello, world!" --audio-method playsound
voice-forge "Hello, world!" --audio-method system
```

## Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `text` | - | Text to convert to speech | - |
| `--file` | `-f` | Read text from file | - |
| `--voice` | `-v` | Path to reference audio file for voice cloning | - |
| `--exaggeration` | `-e` | Exaggeration/intensity control (0.0-1.0) | 0.5 |
| `--cfg-weight` | `-c` | CFG weight for generation control (0.0-1.0) | 0.5 |
| `--save` | `-s` | Save generated audio to file | - |
| `--no-play` | - | Don't play audio, only save to file | False |
| `--audio-method` | - | Audio playback method (auto/pygame/playsound/system) | auto |
| `--device` | - | Device to run model on (auto/cpu/cuda) | auto |
| `--verbose` | `-V` | Enable verbose output | False |

## Examples

### Basic Text-to-Speech
```bash
voice-forge "Welcome to Voice Forge with Chatterbox TTS!"
```

### Gaming Voice Lines
```bash
voice-forge "Ezreal and Jinx teamed up with Ahri, Yasuo, and Teemo to take down the enemy's Nexus in an epic late-game pentakill."
```

### Expressive Speech
```bash
voice-forge "This is amazing!" --exaggeration 0.8 --cfg-weight 0.2
```

### Voice Conversion
```bash
voice-forge "Hello, this is my cloned voice!" --voice my_voice_sample.wav
```

### Batch Processing
```bash
# Create a text file with your content
echo "This is a longer text that I want to convert to speech." > input.txt
voice-forge --file input.txt --save batch_output.wav
```

## Tips for Best Results

### General Use (TTS and Voice Agents)
- The default settings (`exaggeration=0.5`, `cfg-weight=0.5`) work well for most prompts
- If the reference speaker has a fast speaking style, try lowering `cfg-weight` to around `0.3`

### Expressive or Dramatic Speech
- Use lower `cfg-weight` values (e.g., `~0.3`) and increase `exaggeration` to around `0.7` or higher
- Higher `exaggeration` tends to speed up speech; reducing `cfg-weight` helps compensate with slower, more deliberate pacing

### Voice Cloning
- Use high-quality reference audio (clear speech, minimal background noise)
- Reference audio should be at least 3-10 seconds long
- WAV format is preferred for reference files

## Troubleshooting

### Installation Issues

If you encounter import errors:
```bash
# Make sure all dependencies are installed
pip install chatterbox-tts torch torchaudio pygame playsound

# On macOS, you might need:
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### Audio Playback Issues

If audio doesn't play:
```bash
# Try different audio methods
voice-forge "test" --audio-method system
voice-forge "test" --audio-method pygame
voice-forge "test" --audio-method playsound

# Or just save to file and play manually
voice-forge "test" --save test.wav --no-play
```

### CUDA Issues

If you have CUDA issues:
```bash
# Force CPU mode
voice-forge "test" --device cpu
```

## License

This project is based on [Chatterbox TTS](https://github.com/resemble-ai/chatterbox) by Resemble AI, which is licensed under the MIT License.

## Acknowledgments

- [Resemble AI](https://resemble.ai/) for creating Chatterbox TTS
- [Chatterbox TTS Repository](https://github.com/resemble-ai/chatterbox)
- The original Chatterbox research and development team

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is for educational and research purposes. Please use responsibly and follow all applicable laws and ethics guidelines when generating synthetic speech. 
