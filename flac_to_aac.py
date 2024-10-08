import os
import re
import subprocess

qaac = r"C:\Progs\qaac\qaac64.exe"

def convert_to_mp3(qaac_path, input_file, output_file):
    command = [
        qaac_path,
        input_file,
        '--tvbr', '127',
        '-o', output_file
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
            m4a_path = os.path.join(root, new_base_name + '.m4a')
            
            try:
                convert_to_mp3(qaac, file_path, m4a_path)
                os.remove(file_path)
                print(f"Successfully converted {file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {file_path}: {e}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

        elif ext.lower() == '.m4a':
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
