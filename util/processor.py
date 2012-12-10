# Utility for processing image files for my lunar lander game

from PIL import Image
import glob, os

for infile in glob.glob("*.png"):

    print("Processing " + infile)

    im = Image.open(infile)

    w, h = im.size

    (root, ext) = os.path.splitext(infile)
    outfile = root + ".dat"

    with open (outfile, 'w') as f:

        # calculate a list of terrain heights

        for x in range(w):
            height = 0
            for y in range(h):
                #print im.getpixel((x,y))
                if im.getpixel((x,y)) == (0,0,0):
                    height = y
            height = h - height
            out = str(height) + '\n'
            f.write(out)
