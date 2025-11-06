# asr_transcribe.py
from utils import convert_to_wav
from config import ASR_PROVIDER

def transcribe_local_whisperx(audio_path, model="base"):
    import whisperx
    device = "cuda" if whisperx.utils.is_cuda_available() else "cpu"
    model_w = whisperx.load_model(model, device=device)
    result = model_w.transcribe(audio_path)
    segments = [
        {"start": s["start"], "end": s["end"], "text": s["text"].strip()}
        for s in result["segments"]
    ]
    return segments

def transcribe(audio_path):
    if not audio_path.lower().endswith(".wav"):
        wav = audio_path.rsplit(".", 1)[0] + ".wav"
        convert_to_wav(audio_path, wav)
        audio_path = wav
    return transcribe_local_whisperx(audio_path, model="small")
