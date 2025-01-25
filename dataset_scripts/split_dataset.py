import os
import random
import shutil
import hashlib

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
            print(f"Found only {len(image_files)} images for '{movie_dir}'. Using all available.")
            selected_files = image_files
        else:
            selected_files = random.sample(image_files, num_files)

        for source_path in selected_files:
            hashed_name = hash_filename(source_path)
            # Prevents overwriting files with the same name
            while True:
                target_path = os.path.join(target_dir, hashed_name + os.path.splitext(source_path)[1])
                if not os.path.exists(target_path):
                    break
                hashed_name = hashlib.sha256(f"{hashed_name}{os.urandom(1)}".encode()).hexdigest() 

            shutil.copy2(source_path, target_path)


def create_split(dataset_dir: str, output_dir: str, split_name: str, movies: list, num_files: int = 15) -> int:

    split_dir = os.path.join(output_dir, split_name)
    os.makedirs(split_dir, exist_ok=True)
    total_files = 0
    for movie in movies:
        copy_and_hash_images(os.path.join(dataset_dir, movie), os.path.join(split_dir, movie), num_files)
        total_files += sum([len(files) for _, _, files in os.walk(os.path.join(split_dir, movie))])
    return total_files


if __name__ == "__main__":
    train_size, val_size, test_size = 0.7, 0.15, 0.15
    assert sum(train_size + val_size + test_size) == 1.0, "Must sum to 1.0"

    dataset_dir = "3d_animation/3d_animation_folders_cleaned"
    output_dir = "3d_animation/3d_folders_split"

    movies = [d for d in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, d))]
    random.shuffle(movies)

    train_end = int(len(movies) * train_size)
    val_end = train_end + int(len(movies) * val_size)

    train_movies = movies[:train_end]
    val_movies = movies[train_end:val_end]
    test_movies = movies[val_end:]

    train_files = create_split(dataset_dir=dataset_dir,
                               output_dir=output_dir,
                               split_name="train",
                               movies=train_movies,
                               num_files=10)
    
    val_files = create_split(dataset_dir=dataset_dir,
                               output_dir=output_dir,
                               split_name="val",
                               movies=val_movies,
                               num_files=10)
    
    test_files = create_split(dataset_dir=dataset_dir,
                               output_dir=output_dir,
                               split_name="test",
                               movies=test_movies,
                               num_files=10)

    print(f"Train split: {train_files} files")
    print(f"Validation split: {val_files} files")
    print(f"Test split: {test_files} files")