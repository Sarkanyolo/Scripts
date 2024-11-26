import os
import subprocess

# Folder with your AAC files
folder_path = r"C:\Users\gyuri\Downloads"

# Loop through all AAC files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".aac"):
        # Set paths for the input and output files
        input_path = os.path.join(folder_path, filename)
        output_path = os.path.join(folder_path, os.path.splitext(filename)[0] + ".opus")
        
        # Run ffmpeg command
        command = [
            "ffmpeg", "-i", input_path, 
            "-c:a", "libopus",           # Use Opus codec
            "-b:a", "32k",               # Set the Opus bitrate
            "-vbr", "on",                # Enable variable bitrate for Opus
            output_path
        ]
        
        subprocess.run(command)
        print(f"Converted '{filename}' to Opus format at '{output_path}'")
