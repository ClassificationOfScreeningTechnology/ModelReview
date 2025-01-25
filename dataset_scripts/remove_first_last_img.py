import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def delete_first_and_last_images(root_dir):

    image_extensions = ('.jpg', '.jpeg', '.png', '.gif')

    for subdir, _, files in os.walk(root_dir):
        image_files = []
        for file in files:
            if file.lower().endswith(image_extensions):
                # Get the number
                match = re.search(r'_(\d+)\.', file)  
                if match:
                    # Get first grouped number
                    image_files.append((int(match.group(1)), file))
        if len(image_files) >= 2:
            image_files.sort()  

            first_image = os.path.join(subdir, image_files[0][1])
            last_image = os.path.join(subdir, image_files[-1][1])
            try:
                os.remove(first_image)
                os.remove(last_image)
                print(f"Deleted {first_image} and {last_image}")
            except FileNotFoundError:
                print(f"Warning: One or both files not found in {subdir}")


root_directory = "live_action/live_action_folders"
delete_first_and_last_images(root_directory)
