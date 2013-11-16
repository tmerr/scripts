"""
Recursively search directories for a file type then copy them to the
destination in a flat structure.
"""

import os
import shutil
import string
import random

def rip(source, dest, extensions):
    if dest.startswith(source):
        raise Exception("Destination cannot be inside source directory.")

    if not os.path.exists(dest):
        os.makedirs(dest)

    for root, subFolders, files in os.walk(source):
        for f in files:
            fname, ext = os.path.splitext(f)
            if ext in extensions:
                fpath = os.path.join(root, fname)
                copypath = os.path.join(dest, fname)
                while os.path.isfile(copypath):
                    copypath += random.choice(string.letters)
                shutil.copyfile(fpath + ext, copypath + ext)
                print('copied {0} to {1}'.format(fpath+ext, copypath+ext))

if __name__ == '__main__':
    extensions = ('.jpeg', '.jpg', '.png', '.tif')
    source = raw_input("Source directory to search for images: ")
    dest = raw_input("Destination directory to place them: ") 
    rip(source, dest, extensions)
