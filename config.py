# config.py
import os
from dotenv import load_dotenv
load_dotenv()

# ASR (Speech-to-text)
ASR_PROVIDER = os.getenv("ASR_PROVIDER", "whisperx")

# Hugging Face model paths
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", None)

# chunking duration for transcripts
MAX_CHUNK_SECONDS = int(os.getenv("MAX_CHUNK_SECONDS", "600"))
