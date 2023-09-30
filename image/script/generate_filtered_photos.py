from PIL import Image, ImageOps, ImageEnhance
import os
import shutil

with open('image.txt', 'r') as file:
    lines = file.readlines()

for line, folder_name in zip(lines, os.listdir('dzi')):
    folder_name, x, y, red, green, blue = line.strip().split()

    original_folder_path = os.path.join('dzi', folder_name, folder_name + '_files')

    edited_folder_path = os.path.join('dzi_edited', folder_name, folder_name + '_files')
    os.makedirs(edited_folder_path, exist_ok=True)

    original_dzi_file_path = os.path.join('dzi', folder_name, f'{folder_name}.dzi')
    edited_dzi_file_path = os.path.join('dzi_edited', folder_name, f'{folder_name}.dzi')
    shutil.copy(original_dzi_file_path, edited_dzi_file_path)

    for folder in os.listdir(original_folder_path):
        for filename in os.listdir(os.path.join(original_folder_path, folder)):
            original_image_path = os.path.join(original_folder_path, folder, filename)
            grayscale_image = ImageOps.grayscale(Image.open(original_image_path))

            colormap = ImageOps.colorize(grayscale_image, black=(0, 0, 0), white=(int(red), int(green), int(blue)))

            enhancer = ImageEnhance.Brightness(colormap)
            bright_colormap = enhancer.enhance(1.5)

            edited_image_path = os.path.join(edited_folder_path, folder, filename)

            os.makedirs(os.path.join(edited_folder_path, folder), exist_ok=True)
            bright_colormap.save(edited_image_path, quality=100)
    print("Processing " + folder_name)

print("Image processing completed.")
