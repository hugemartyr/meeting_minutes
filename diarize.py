# diarize.py
from config import HUGGINGFACE_TOKEN

def diarize_pyannote(audio_path):
    from pyannote.audio import Pipeline
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=HUGGINGFACE_TOKEN)
    diarization = pipeline(audio_path)
    diarization_segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        diarization_segments.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })
    return diarization_segments

def merge_transcript_and_diarization(transcript_segments, diarization_segments):
    merged = []
    for t in transcript_segments:
        best_speaker, best_overlap = "Unknown", 0
        for d in diarization_segments:
            overlap = max(0, min(t['end'], d['end']) - max(t['start'], d['start']))
            if overlap > best_overlap:
                best_overlap, best_speaker = overlap, d['speaker']
        merged.append({**t, "speaker": best_speaker})
    return merged
