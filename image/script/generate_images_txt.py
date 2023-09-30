from PIL import Image
import os

if os.path.exists("image.txt"):
    os.remove("image.txt")

su_image = Image.open("sureal25x25.png").convert("RGBA")
su_pixels = su_image.load()

subfolder_names = sorted(os.listdir("dzi"))

with open("image.txt", "w") as output_file:
    for y in range(su_image.height):
        for x in range(su_image.width):
            r, g, b, a = su_pixels[x, y]

            if a == 255:
                if subfolder_names:
                    folder_name = subfolder_names.pop(0)
                    output_file.write(f"{folder_name} {x} {y} {r} {g} {b}\n")
                else:
                    print("Finished generating images txt")
                    exit()
