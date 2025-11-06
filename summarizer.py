# summarizer.py
import json
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from config import MISTRAL_MODEL, MAX_CHUNK_SECONDS
from utils import chunk_transcript_by_duration, seconds_to_timestamp

# load model once globally
print("Loading Mistral model... (first time may take ~30s)")
tokenizer = AutoTokenizer.from_pretrained(MISTRAL_MODEL, token= None)
model = AutoModelForCausalLM.from_pretrained(MISTRAL_MODEL, device_map="auto", torch_dtype="auto")
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

BASE_PROMPT = """You are an assistant that turns meeting transcripts into structured Minutes of Meeting (MoM).

You will receive lines like:
[00:02:10] Speaker_1: Welcome everyone, let's discuss project X...

Return a *valid JSON* object with:
{
  "short_summary": "Brief 1-2 sentence overview.",
  "long_summary": "Detailed narrative of discussion and outcomes.",
  "attendees": [],
  "agenda": [],
  "decisions": [],
  "action_items": [],
  "topics": []
}
Each 'action_item' = {"task": "", "owner": "", "due": "", "timestamp": ""}.
Each 'decision' = {"decision": "", "by": "", "timestamp": ""}.
Output strictly valid JSON, no commentary.
"""

def build_transcript_text(segments):
    return "\n".join([
        f"[{seconds_to_timestamp(s['start'])}] {s.get('speaker','Speaker')}: {s['text']}"
        for s in segments
    ])

def call_mistral(prompt, max_new_tokens=700):
    output = generator(prompt, max_new_tokens=max_new_tokens, temperature=0.2, do_sample=False)
    text = output[0]["generated_text"]
    return text[len(prompt):].strip() if text.startswith(prompt) else text.strip()

def parse_json_safe(text):
    import re
    match = re.search(r'(\{.*\})', text, re.S)
    if match:
        try:
            return json.loads(match.group(1))
        except Exception:
            return json.loads(match.group(1).replace("'", '"'))
    raise ValueError("No JSON found in output.")

def generate_minutes(merged_segments):
    chunks = chunk_transcript_by_duration(merged_segments, max_seconds=MAX_CHUNK_SECONDS)
    partials = []
    for ch in chunks:
        txt = build_transcript_text(ch["segments"])
        prompt = BASE_PROMPT + "\n\nTRANSCRIPT:\n" + txt
        out = call_mistral(prompt)
        j = parse_json_safe(out)
        partials.append(j)
    # Simple merge
    combined = {
        "short_summary": " ".join(p.get("short_summary", "") for p in partials),
        "long_summary": " ".join(p.get("long_summary", "") for p in partials),
        "attendees": list({a for p in partials for a in p.get("attendees", [])}),
        "agenda": list({a for p in partials for a in p.get("agenda", [])}),
        "decisions": [d for p in partials for d in p.get("decisions", [])],
        "action_items": [a for p in partials for a in p.get("action_items", [])],
        "topics": [t for p in partials for t in p.get("topics", [])],
    }
    return combined
