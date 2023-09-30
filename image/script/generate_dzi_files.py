# ensure to use my fork https://github.com/wattapik/MagickSlicer

import os
import subprocess
import shutil

def convert_to_jpg(input_file, output_dir):
    try:
        file_name_without_extension = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join("original", "jpg", f"{file_name_without_extension}.jpg")

        convert_command = ["convert", input_file, "-quality", "100", output_file]

        subprocess.run(convert_command)

        process_image(output_file, output_dir)
    except Exception as e:
        print(f"Error converting {input_file} to JPG: {e}")

def process_image(input_file, output_dir):
    try:
        file_name_without_extension = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, file_name_without_extension, f"{file_name_without_extension}")

        command = ["./script/magick-slicer.sh", input_file, output_file]

        subprocess.run(command)
        print(f"Processed {input_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

input_dir = "original"
output_dir = "dzi"

os.makedirs(output_dir, exist_ok=True)
os.makedirs(os.path.join(input_dir, "jpg"), exist_ok=True)

image_files = []
for root, _, files in os.walk(input_dir):
    for filename in files:
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            image_files.append(os.path.join(root, filename))

for input_file in image_files:
    convert_to_jpg(input_file, output_dir)

shutil.rmtree(os.path.join(input_dir, "jpg"))
print("Sliced all photos.")
