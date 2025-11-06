# app.py
from flask import Flask, request, jsonify, render_template_string
import os, uuid
from utils import extract_audio_from_video
from asr_transcribe import transcribe
from diarize import diarize_pyannote, merge_transcript_and_diarization
from summarizer import generate_minutes

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

HTML = """
<!doctype html>
<title>Mistral MoM Generator</title>
<h1>Upload meeting audio/video</h1>
<form method=post enctype=multipart/form-data action="/upload">
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("file")
    if not f:
        return "No file uploaded", 400
    fname = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4().hex}_{f.filename}")
    f.save(fname)

    if fname.lower().endswith((".mp4", ".mkv", ".mov")):
        audio_path = fname.rsplit(".", 1)[0] + ".wav"
        extract_audio_from_video(fname, audio_path)
    else:
        audio_path = fname

    transcript = transcribe(audio_path)

    try:
        diar = diarize_pyannote(audio_path)
        merged = merge_transcript_and_diarization(transcript, diar)
    except Exception as e:
        print("Diarization skipped:", e)
        merged = [{**t, "speaker": f"Speaker_{(i%4)+1}"} for i, t in enumerate(transcript)]

    minutes = generate_minutes(merged)
    return jsonify(minutes)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
