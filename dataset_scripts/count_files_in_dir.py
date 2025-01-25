import os
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

def count_files_in_folders(base_path, output_file):
    folder_counts = []

    for dir in os.listdir(base_path):
        dir_path = os.path.join(base_path, dir)
        if os.path.isdir(dir_path): 
            file_count = sum(1 for file in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, file)))
            print(f"Dir name: {dir_path}, file_count: {file_count   }")  
            folder_counts.append(
                {
                    "movie_title" : dir,
                    "image_count" : file_count
                }
            )

    # Get folders with less than 10 files
    filtered_folders = [entry for entry in folder_counts if entry["image_count"] < 10]
    length = len(filtered_folders)
    middle_movie = filtered_folders[length//2]
    
    with open(output_file, 'w') as json_file:
        json.dump(filtered_folders, json_file, indent=4)

    print(f"Filtered folders have been written to {output_file}")
    print(f"Num of movies: {length}, Name of the middle movie {middle_movie}")


base_folder = "2d_animation/2d_animation_folders"
output_json = "2d_animation/2d_filtered_folders.json"

count_files_in_folders(base_folder, output_json)
