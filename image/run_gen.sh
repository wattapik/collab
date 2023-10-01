#!/bin/bash
Xvfb :99 -screen 0 1280x1024x24 &
export DISPLAY=:99

script/bin/python3.11 script/generate_dzi_files.py
script/bin/python3.11 script/generate_images_txt.py
script/bin/python3.11 script/generate_filtered_photos.py
script/bin/python3.11 script/generate_annotations.py

sudo chmod -R 775 .
sudo chown -R opc .
