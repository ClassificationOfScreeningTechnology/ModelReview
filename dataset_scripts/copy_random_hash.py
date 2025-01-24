import os
import shutil
import hashlib
import random

def hash_filename(filename):
    with open(filename, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()[:10]
    return file_hash

def copy_and_hash_images(source_dir, target_dir, num_files=15):
    os.makedirs(target_dir, exist_ok=True)

    for movie_dir in os.listdir(source_dir):
        source_movie_dir = os.path.join(source_dir, movie_dir)
        if not os.path.isdir(source_movie_dir):
            continue

        image_files = [os.path.join(source_movie_dir, f) for f in os.listdir(source_movie_dir) 
                        if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

        if len(image_files) < num_files:
            print(f"Warning: Found only {len(image_files)} image files for '{movie_dir}'. Using all available.")
            selected_files = image_files
        else:
            selected_files = random.sample(image_files, num_files)

        for source_path in selected_files:
            file_hash = hash_filename(source_path)  
            while True:
                target_path = os.path.join(target_dir, file_hash + os.path.splitext(source_path)[1])
                if not os.path.exists(target_path):
                    break
                file_hash = hashlib.sha256(f"{file_hash}{os.urandom(1)}".encode()).hexdigest()

            shutil.copy2(source_path, target_path)

if __name__ == "__main__":
    source_directory = "2d_animation/2d_animation_folders"
    target_directory = "2d_animation/2d_rand_hashed_folders"
    copy_and_hash_images(source_directory, target_directory)
