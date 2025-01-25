import os
import shutil

def copy_files_matching_dir_name(source_dir, tgt_dir):
    for subdir, _, files in os.walk(source_dir):
        subdir_name = os.path.basename(subdir)
        target_dir = os.path.join(tgt_dir, subdir_name)

        if os.path.exists(target_dir):
            for file in files:
                source_file = os.path.join(subdir, file)
                destination_file = os.path.join(target_dir, file)
                shutil.copy2(source_file, destination_file)
                print(f'Copied {source_file} to {destination_file}')

if __name__ == "__main__":
    source_dir = 'migrate/Films'
    tgt_dir = 'migrate/stop_motion_folders'
    copy_files_matching_dir_name(source_dir, tgt_dir)