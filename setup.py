#!/usr/bin/env python3
"""
Setup script for Voice Forge
"""

from setuptools import setup, find_packages

setup(
    name="voice-forge",
    use_scm_version=False,
    version="1.0.0",
    author="Hemanth HM",
    author_email="hemanth.hm@gmail.com",
    description="A command-line tool for text-to-speech generation using Chatterbox TTS",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://h3manth.com",
    packages=find_packages(include=["voice_forge*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: System Shells",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=[
        "chatterbox-tts",
        "torch>=1.9.0",
        "torchaudio>=0.9.0",
        "pygame>=2.0.0",
        "playsound>=1.2.2",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8", 
            "mypy",
            "build",
            "twine",
        ],
    },
    entry_points={
        "console_scripts": [
            "voice-forge=voice_forge.main:main",
        ],
    },
    keywords="tts text-to-speech voice speech chatterbox cli",
    project_urls={
        "Homepage": "https://h3manth.com",
        "Repository": "https://github.com/hemanth/voice-forge",
        "Bug Reports": "https://github.com/hemanth/voice-forge/issues",
        "Source": "https://github.com/hemanth/voice-forge",
        "Documentation": "https://github.com/hemanth/voice-forge#readme",
    },
) 