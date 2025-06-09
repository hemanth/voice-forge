"""
Voice Forge CLI - Main entry point and argument parsing
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path

from .cli import VoiceForgeCLI


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="voice-forge",
        description="Voice Forge - Generate and play speech from text using Chatterbox TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  voice-forge "Hello, world!"
  voice-forge "Hello, world!" --save output.wav
  voice-forge "Hello, world!" --voice reference.wav
  voice-forge "Hello, world!" --exaggeration 0.7 --cfg-weight 0.3
  voice-forge --file input.txt --save output.wav
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "text", 
        nargs="?", 
        help="Text to convert to speech"
    )
    input_group.add_argument(
        "--file", "-f",
        type=str,
        help="Read text from file"
    )
    
    # Voice options
    parser.add_argument(
        "--voice", "-v",
        type=str,
        help="Path to reference audio file for voice cloning"
    )
    
    # Model parameters
    parser.add_argument(
        "--exaggeration", "-e",
        type=float,
        default=0.5,
        help="Exaggeration/intensity control (default: 0.5)"
    )
    
    parser.add_argument(
        "--cfg-weight", "-c",
        type=float,
        default=0.5,
        help="CFG weight for generation control (default: 0.5)"
    )
    
    # Output options
    parser.add_argument(
        "--save", "-s",
        type=str,
        help="Save generated audio to file (default: play only)"
    )
    
    parser.add_argument(
        "--no-play",
        action="store_true",
        help="Don't play audio, only save to file"
    )
    
    # Audio playback options
    parser.add_argument(
        "--audio-method",
        choices=["auto", "pygame", "playsound", "system"],
        default="auto",
        help="Audio playback method (default: auto)"
    )
    
    # Device options
    parser.add_argument(
        "--device",
        choices=["auto", "cpu", "cuda"],
        default="auto",
        help="Device to run model on (default: auto)"
    )
    
    parser.add_argument(
        "--verbose", "-V",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"Voice Forge {_get_version()}"
    )
    
    return parser


def _get_version():
    """Get package version."""
    try:
        from . import __version__
        return __version__
    except ImportError:
        return "unknown"


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Get text input
    if args.text:
        text = args.text
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
        except Exception as e:
            print(f"❌ Error reading file {args.file}: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
    
    if not text:
        print("❌ No text provided or file is empty")
        sys.exit(1)
    
    # Validate voice reference file
    if args.voice and not os.path.exists(args.voice):
        print(f"❌ Voice reference file not found: {args.voice}")
        sys.exit(1)
    
    # Initialize CLI
    cli = VoiceForgeCLI()
    
    # Set device
    if args.device != "auto":
        cli.device = args.device
    
    # Load model
    try:
        cli.load_model_if_needed()
    except Exception as e:
        print(f"❌ Failed to initialize Voice Forge: {e}")
        sys.exit(1)
    
    # Generate speech
    try:
        wav_data = cli.generate_speech(
            text, 
            audio_prompt_path=args.voice,
            exaggeration=args.exaggeration,
            cfg_weight=args.cfg_weight
        )
    except Exception as e:
        print(f"❌ Speech generation failed: {e}")
        sys.exit(1)
    
    # Handle output
    temp_file = None
    audio_path = args.save
    
    if not audio_path:
        # Create temporary file for playback
        temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        audio_path = temp_file.name
        temp_file.close()
    
    # Save audio
    try:
        cli.save_audio(wav_data, audio_path)
    except Exception as e:
        if temp_file:
            os.unlink(temp_file.name)
        sys.exit(1)
    
    # Play audio if requested
    if not args.no_play:
        try:
            cli.play_audio(audio_path, method=args.audio_method)
        except Exception as e:
            print(f"⚠️  Playback failed: {e}")
            if args.save:
                print(f"Audio saved to: {args.save}")
    
    # Clean up temporary file
    if temp_file:
        try:
            os.unlink(temp_file.name)
        except:
            pass
    
    print("✅ Done!")


if __name__ == "__main__":
    main() 