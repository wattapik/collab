#!/bin/bash
source script/bin/activate

# Xvfb :99 -screen 0 1280x1024x24 &
# export DISPLAY=:99

python3 script/generate_dzi_files.py
python3 script/generate_images_txt.py
python3 script/generate_filtered_photos.py
python3 script/generate_annotations.py

sudo chmod -R 775 .
sudo chown -R opc .
