import os
import random
import string

def generate_random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def rename_files_in_subdirectories(films_dir):
    for subdir, _, files in os.walk(films_dir):
        for file in files:
            new_name = f"{generate_random_name()}{os.path.splitext(file)[1]}"
            os.rename(
                os.path.join(subdir, file),
                os.path.join(subdir, new_name)
            )
            print(f'Renamed {file} to {new_name}')

if __name__ == "__main__":
    rename_files_in_subdirectories('Films')