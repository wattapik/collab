# ensure to use my fork https://github.com/wattapik/MagickSlicer

import os
import subprocess
import shutil

def convert_to_jpg(input_file, output_dir):
    try:
        # Construct the output file path for the converted JPG
        file_name_without_extension = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join("original", "jpg", f"{file_name_without_extension}.jpg")

        # Command to convert the image to JPG using ImageMagick's 'convert' command
        convert_command = ["convert", input_file, "-quality", "100", output_file]

        # Run the conversion command
        subprocess.run(convert_command)
        print(f"Converted {input_file} to JPG")

        # Once converted, process the JPG image
        process_image(output_file, output_dir)
    except Exception as e:
        print(f"Error converting {input_file} to JPG: {e}")

def process_image(input_file, output_dir):
    try:
        # Construct the output file path
        file_name_without_extension = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, file_name_without_extension, f"{file_name_without_extension}")

        # Command to invoke the "magick-slicer.sh" script
        command = ["./magick-slicer.sh", input_file, output_file]

        print(command)
        print(output_file)
        print(os.getcwd())
        # Run the command
        subprocess.run(command)
        print(f"Processed {input_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def main():
    # Define the input and output directories
    input_dir = "original"
    output_dir = "dzi"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(input_dir, "jpg"), exist_ok=True)  # Create "original/jpg" folder

    # Gather a list of image files in the input directory
    image_files = []
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                image_files.append(os.path.join(root, filename))

    # Convert and process image files synchronously
    for input_file in image_files:
        convert_to_jpg(input_file, output_dir)

    # Delete the "original/jpg" folder once all conversions and processing are finished
    # shutil.rmtree(os.path.join(input_dir, "jpg"))

if __name__ == "__main__":
    main()
