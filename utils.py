# # utils.py
# import moviepy.editor as mp
# from moviepy.editor import VideoFileClip
# from pydub import AudioSegment
# import math

# def extract_audio_from_video(video_path, out_audio_path):
#     clip = VideoFileClip(video_path)
#     clip.audio.write_audiofile(out_audio_path, logger=None)
#     clip.close()
#     return out_audio_path

# def convert_to_wav(input_path, out_path, sample_rate=16000):
#     audio = AudioSegment.from_file(input_path)
#     audio = audio.set_frame_rate(sample_rate).set_channels(1)
#     audio.export(out_path, format="wav")
#     return out_path

# def seconds_to_timestamp(s):
#     m, s = divmod(int(s), 60)
#     h, m = divmod(m, 60)
#     return f"{h:02d}:{m:02d}:{s:02d}"

# def chunk_transcript_by_duration(segments, max_seconds=600):
#     chunks, cur, duration = [], {"segments": []}, 0
#     for seg in segments:
#         seg_len = seg['end'] - seg['start']
#         if not cur.get("start"): cur["start"] = seg['start']
#         if duration + seg_len > max_seconds and cur["segments"]:
#             cur["end"] = cur["segments"][-1]['end']
#             chunks.append(cur)
#             cur, duration = {"segments": [seg], "start": seg['start']}, seg_len
#         else:
#             cur["segments"].append(seg)
#             duration += seg_len
#     if cur["segments"]:
#         cur["end"] = cur["segments"][-1]['end']
#         chunks.append(cur)
#     return chunks


# utils.py

# --- NEW IMPORTS ---
from pydub import AudioSegment
import math
import subprocess
import os
# --- END NEW IMPORTS ---


def extract_audio_from_video(video_path, out_audio_path):
    """
    Extracts audio from a video file using the FFmpeg command-line utility,
    then converts it to the final WAV format using pydub.
    
    NOTE: FFmpeg must be installed and accessible via the system PATH.
    """
    # 1. Define a temporary path for the extracted audio (e.g., MP3)
    temp_mp3_path = os.path.splitext(out_audio_path)[0] + "_temp.mp3"
    
    # 2. Define the FFmpeg command to extract audio to MP3
    command = [
        'ffmpeg',
        '-y',               # Overwrite output file without asking
        '-i', video_path,   # Input file
        '-vn',              # No video stream (discard video)
        '-acodec', 'libmp3lame', # Use the libmp3lame codec
        '-q:a', '0',        # Highest quality VBR (Variable Bit Rate)
        temp_mp3_path       # Temporary MP3 output path
    ]

    try:
        # Run the FFmpeg command
        print("Starting FFmpeg audio extraction...")
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"FFmpeg extraction complete. Converting to final WAV format...")
        
        # 3. Convert the temporary MP3 to the final WAV using pydub
        # NOTE: The target sample_rate (16000) and channels (1) are applied here
        audio = AudioSegment.from_mp3(temp_mp3_path)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(out_audio_path, format="wav")
        
        # 4. Clean up the intermediate file
        os.remove(temp_mp3_path)
        
        return out_audio_path
        
    except subprocess.CalledProcessError as e:
        # Catch errors if FFmpeg runs but fails (e.g., bad video file)
        error_output = e.stderr.decode('utf8', errors='ignore')
        raise RuntimeError(f"FFmpeg failed to extract audio. Error: {error_output}")
    except FileNotFoundError:
        # Catch errors if the 'ffmpeg' command itself cannot be found
        raise FileNotFoundError("The 'ffmpeg' command was not found. Ensure FFmpeg is installed and added to your system's PATH.")


def convert_to_wav(input_path, out_path, sample_rate=16000):
    """
    Converts any audio file to a 16kHz mono WAV file using pydub.
    (This function is retained for general use, but its logic is now partially integrated into extract_audio_from_video).
    """
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_frame_rate(sample_rate).set_channels(1)
    audio.export(out_path, format="wav")
    return out_path

def seconds_to_timestamp(s):
    m, s = divmod(int(s), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def chunk_transcript_by_duration(segments, max_seconds=600):
    chunks, cur, duration = [], {"segments": []}, 0
    for seg in segments:
        seg_len = seg['end'] - seg['start']
        if not cur.get("start"): cur["start"] = seg['start']
        if duration + seg_len > max_seconds and cur["segments"]:
            cur["end"] = cur["segments"][-1]['end']
            chunks.append(cur)
            cur, duration = {"segments": [seg], "start": seg['start']}, seg_len
        else:
            cur["segments"].append(seg)
            duration += seg_len
    if cur["segments"]:
        cur["end"] = cur["segments"][-1]['end']
        chunks.append(cur)
    return chunks
