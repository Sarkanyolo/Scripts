import os
import subprocess
import time
from datetime import datetime

def convert_to_avi(mp4_path: str, start_time: str = "", end_time: str = "") -> None:

    # Video and audio parameters
    video_codec = "mpeg4"
    video_tag = "XVID"
    video_bitrate = "1400k"
    frame_settings = "600x480"
    audio_codec = "libmp3lame"
    audio_bitrate = "160k"
    audio_rate = "48000"
    audio_channels = "2"


    mp4_path = mp4_path.strip().strip('"')

    if not os.path.exists(mp4_path):
        raise FileNotFoundError(f"File not found: {mp4_path}")

    if mp4_path.lower().endswith(".avi"):
        raise ValueError("Input file is already an AVI format")

    duration = None
    layout = "%H:%M:%S"

    if start_time and end_time:
        start = datetime.strptime(start_time, layout)
        end = datetime.strptime(end_time, layout)
        duration = str(end - start)

    # Prepare the output AVI path
    avi_output = os.path.splitext(mp4_path)[0] + ".avi"


    # First pass
    cmd_pass1 = [
        "ffmpeg", "-i", mp4_path, "-vcodec", video_codec, "-vtag", video_tag, 
        "-b:v", video_bitrate, "-bf", "2", "-g", "300", "-s", frame_settings, 
        "-pass", "1", "-an", "-threads", "0", "-f", "rawvideo", "-y", "NUL"
    ]

    # Second pass with optional start/end times
    args_pass2 = [
        "-i", mp4_path, "-vcodec", video_codec, "-vtag", video_tag, "-b:v", video_bitrate, 
        "-bf", "2", "-g", "300", "-s", frame_settings, "-acodec", audio_codec, 
        "-ab", audio_bitrate, "-ar", audio_rate, "-ac", audio_channels, 
        "-pass", "2", "-threads", "0", "-f", "avi", avi_output
    ]

    if end_time:
        args_pass2 = ["-t", duration] + args_pass2
    
    if start_time:
        args_pass2 = ["-ss", start_time] + args_pass2

    cmd_pass2 = ["ffmpeg"] + args_pass2

    # Run the first pass
    result = subprocess.run(cmd_pass1, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed 1st pass: {result.stderr.decode()}")

    # Run the second pass
    result = subprocess.run(cmd_pass2, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed 2nd pass: {result.stderr.decode()}")

    # Clean up
    os.remove("ffmpeg2pass-0.log")
    os.remove(mp4_path)

if __name__ == "__main__":
    mp4_path = input("Enter the path to the MP4 file: ").strip()
    start_time = input("Enter the timestamp where content begins (optional, e.g., 00:02:23): ").strip()
    end_time = input("Enter the timestamp where content ends (optional, e.g., 00:27:12): ").strip()

    try:
        convert_to_avi(mp4_path, start_time, end_time)
        print("Conversion completed successfully!")
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
