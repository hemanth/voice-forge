"""
Voice Forge CLI - Core TTS functionality
"""

import os
import sys
import time
import tempfile
import platform
from pathlib import Path
from typing import Optional, Tuple

# Import chatterbox TTS
try:
    import chatterbox
    CHATTERBOX_AVAILABLE = True
except ImportError as e:
    print(f"Error importing chatterbox: {e}")
    print("Please install chatterbox-tts: pip install chatterbox-tts")
    CHATTERBOX_AVAILABLE = False

# Import audio libraries
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False

import torch
import torchaudio as ta


class VoiceForgeCLI:
    """Voice Forge CLI - Text-to-Speech Generation Tool"""
    
    def __init__(self):
        self.model = None
        self.device = "cuda" if self._is_cuda_available() else "cpu"
        
    def _is_cuda_available(self) -> bool:
        """Check if CUDA is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def load_model_if_needed(self) -> None:
        """Load the TTS model if not already loaded."""
        if self.model is not None:
            return
            
        print(f"Loading Chatterbox TTS model on {self.device}...")
        try:
            # Set default tensor type to CPU to avoid CUDA issues
            if self.device == "cpu":
                torch.set_default_dtype(torch.float32)
                torch.set_default_device('cpu')
                
                # Set map_location for torch.load to handle CUDA->CPU model loading
                original_load = torch.load
                def patched_load(*args, **kwargs):
                    if 'map_location' not in kwargs:
                        kwargs['map_location'] = torch.device('cpu')
                    return original_load(*args, **kwargs)
                torch.load = patched_load
            
            self.model = chatterbox.tts.ChatterboxTTS.from_pretrained(device=self.device)
            
            # Restore original torch.load
            if self.device == "cpu":
                torch.load = original_load
                
            print("✅ Model loaded successfully!")
        except Exception as e:
            # Restore original torch.load in case of error
            if self.device == "cpu" and 'original_load' in locals():
                torch.load = original_load
            print(f"❌ Failed to load model: {e}")
            raise
    
    def generate_speech(self, text: str, audio_prompt_path: Optional[str] = None, 
                       exaggeration: float = 0.5, cfg_weight: float = 0.5) -> tuple:
        """Generate speech from text using Chatterbox TTS."""
        if not self.model:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        print(f"Generating speech for: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        
        try:
            if audio_prompt_path:
                print(f"Using voice reference: {audio_prompt_path}")
                wav = self.model.generate(
                    text, 
                    audio_prompt_path=audio_prompt_path,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight
                )
            else:
                wav = self.model.generate(
                    text,
                    exaggeration=exaggeration,
                    cfg_weight=cfg_weight
                )
            return wav, self.model.sr
        except Exception as e:
            print(f"❌ Failed to generate speech: {e}")
            raise
    
    def save_audio(self, wav_data: Tuple, output_path: str) -> None:
        """Save generated audio to file."""
        if not wav_data:
            print("❌ No audio data to save")
            return
            
        wav, sr = wav_data
        try:
            ta.save(output_path, wav, sr)
            print(f"💾 Audio saved to: {output_path}")
        except Exception as e:
            print(f"❌ Error saving audio: {e}")
    
    def play_audio(self, audio_path: str, method: str = "auto") -> None:
        """Play audio file using available audio libraries."""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"🔊 Playing audio...")
        
        if method == "auto":
            # Try pygame first, then playsound, then system command
            if PYGAME_AVAILABLE:
                method = "pygame"
            elif PLAYSOUND_AVAILABLE:
                method = "playsound"
            else:
                method = "system"
        
        try:
            if method == "pygame":
                self._play_with_pygame(audio_path)
            elif method == "playsound":
                self._play_with_playsound(audio_path)
            elif method == "system":
                self._play_with_system(audio_path)
            else:
                raise ValueError(f"Unknown audio method: {method}")
        except Exception as e:
            print(f"❌ Failed to play audio: {e}")
            # Try fallback methods
            if method != "system":
                print("🔄 Trying system audio player...")
                self._play_with_system(audio_path)
    
    def _play_with_pygame(self, audio_path: str) -> None:
        """Play audio using pygame."""
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        pygame.mixer.quit()
    
    def _play_with_playsound(self, audio_path: str) -> None:
        """Play audio using playsound."""
        playsound(audio_path, block=True)
    
    def _play_with_system(self, audio_path: str) -> None:
        """Play audio using system audio player."""
        if sys.platform.startswith('darwin'):  # MacOS
            os.system(f'afplay "{audio_path}"')
        elif sys.platform.startswith('linux'):  # Linux
            # Try different audio players
            players = ['paplay', 'aplay', 'mplayer', 'mpv', 'vlc']
            for player in players:
                if os.system(f'which {player} > /dev/null 2>&1') == 0:
                    os.system(f'{player} "{audio_path}" > /dev/null 2>&1')
                    return
            raise RuntimeError("No audio player found on Linux system")
        elif sys.platform.startswith('win'):  # Windows
            os.system(f'start "" "{audio_path}"')
        else:
            raise RuntimeError(f"Unsupported platform: {sys.platform}")


# Maintain backward compatibility
ChatterboxCLI = VoiceForgeCLI 