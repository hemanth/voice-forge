"""
Voice Forge - Text-to-Speech Generation Tool

A command-line interface for the Chatterbox TTS model that allows you to:
- Generate speech from text
- Clone voices using reference audio
- Control speech generation parameters
- Save output to files or play directly
"""

__version__ = "1.0.0"
__author__ = "Hemanth HM"
__email__ = "hemanth.hm@gmail.com"

from .cli import ChatterboxCLI
from .main import main

__all__ = ["ChatterboxCLI", "main", "__version__"] 