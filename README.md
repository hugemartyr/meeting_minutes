# Meeting Minutes Generator

An automated system that converts meeting audio/video recordings into structured Minutes of Meeting (MoM) using AI-powered speech recognition, speaker diarization, and text summarization.

## Features

- **Audio/Video Processing**: Supports various formats (MP4, MKV, MOV, WAV)
- **Speech Recognition**: Uses WhisperX for accurate transcription
- **Speaker Diarization**: Identifies different speakers using pyannote.audio
- **AI Summarization**: Generates structured meeting minutes using Mistral-7B
- **Web Interface**: Simple Flask-based upload interface

## Generated Meeting Minutes Include

- Short summary (1-2 sentences)
- Detailed narrative summary
- List of attendees
- Meeting agenda
- Key decisions with timestamps
- Action items with owners and due dates
- Discussion topics

## Prerequisites

- Python 3.x
- FFmpeg (for audio/video processing)
- CUDA-compatible GPU (optional, for faster processing)

## Installation

1. Clone the repository
2. Install the required packages:

```bash
pip install -r [requirements.txt](http://_vscodecontentref_/1)
```
