import os
import re
import subprocess

ffmpeg_path = r"C:\ProgramData\chocolatey\lib\ffmpeg-full\tools\ffmpeg\bin\ffmpeg.exe"

def convert_to_mp3(ffmpeg_path, input_file, output_file):
    command = [
        ffmpeg_path,
        '-i', input_file,
        '-codec:a', 'libmp3lame',
        '-qscale:a', '0',
        output_file
    ]
    subprocess.run(command, check=True)

def remove_brackets(filename):
    return re.sub(pattern, '', filename).strip()

pattern = re.compile(r'\s*[\[\(].*?[\]\)]\s*')
base_dir = os.getcwd()

for root, dirs, files in os.walk(base_dir):
    for file in files:
        file_path = os.path.join(root, file)
        base_name, ext = os.path.splitext(file)
        
        if ext.lower() == '.flac':
            new_base_name = remove_brackets(base_name)
            mp3_path = os.path.join(root, new_base_name + '.mp3')
            
            try:
                convert_to_mp3(ffmpeg_path, file_path, mp3_path)
                os.remove(file_path)
                print(f"Successfully converted {file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {file_path}: {e}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

        elif ext.lower() == '.mp3':
            new_base_name = remove_brackets(base_name)
            new_file_path = os.path.join(root, new_base_name + ext)
            if new_file_path != file_path:
                try:
                    os.rename(file_path, new_file_path)
                    print(f"Renamed {file_path} to {new_file_path}")
                except OSError as e:
                    print(f"Error renaming {file_path}: {e}")

        elif ext.lower() in ['.txt', '.jpg', '.jpeg']:
            try:
                os.remove(file_path)
                print(f"Deleted {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

print("Done!")
