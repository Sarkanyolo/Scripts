import os

folder_path = r"D:\Film\Mese\Pottommag Tilda"
old_substring = 'Pottommag Tilda -'
new_substring = 'Tilda -'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
        
    if os.path.isfile(file_path):
        if old_substring in filename:
            new_filename = filename.replace(old_substring, new_substring)
            new_file_path = os.path.join(folder_path, new_filename)
            os.rename(file_path, new_file_path)
            print(f'Renamed: {filename} -> {new_filename}')
