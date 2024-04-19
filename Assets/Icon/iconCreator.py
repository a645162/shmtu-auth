#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://github.com/prOttonicFusion/iconCreator
# Script for creating a set of icon from a single NxN pixel image
# Usage: python iconCreator.py image-file.png
#

import os
# import sys
from PIL import Image
from pathlib import Path

# Output directories
directories = ["base", "linux", "mac"]

# Input file from CLI argument
# if (len(sys.argv) != 2):
#     print("Usage: {} <input-image-file>".format(sys.argv[0]))
#     exit()

# infile = sys.argv[1]
infile = Path("macOS/Logo.png")


def addMargin(image, topMargin, leftMargin, bottomMargin, rightMargin):
    """Pad image with margin of defined size"""
    newWidth = image.size[0] + rightMargin + leftMargin
    newHeight = image.size[1] + topMargin + bottomMargin
    newImage = Image.new(image.mode, (newWidth, newHeight), (255, 255, 255, 0))
    newImage.paste(image, (leftMargin, topMargin))
    return newImage


for dir in directories:
    # Create output directory structure if not exists
    pathToDir = Path("icons") / Path(dir)
    if not os.path.exists(pathToDir):
        os.makedirs(pathToDir)

    if dir == 'base':
        # General icons
        imgSizes = [16, 24, 32, 48, 64]
    else:
        # Mac & Linux icons
        imgSizes = [128, 256, 512, 1024]

    for size in imgSizes:
        outfile = pathToDir / Path(str(size) + ".png")
        try:
            with Image.open(infile) as img:
                # Scale & convert image

                if 'mac' in dir:
                    # Add ~5% margin to Mac icons
                    m = int(img.size[0] * 0.05)
                    img = addMargin(img, m, m, m, m)

                img.thumbnail((size, size))
                img.save(outfile)
        except IOError:
            print("Unable to process", infile)
            exit()

        print("Created: ", outfile)

# Windows ICO file
outfile = Path("icons") / Path("Icon.ico")
try:
    # Scale & convert image
    with Image.open(infile) as img:
        img.save(outfile)
except IOError:
    print("Unable to process", infile)
    exit()
print("Created: ", outfile)

print("Done!")
