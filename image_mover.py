#!/usr/bin/python

import os, os.path, sys
from shutil import copyfile
from PIL import Image
from collections import defaultdict

__pretend__ = False
extensions = ['.jpg', '.jpeg', '.png']

def process_file(input_file, out_path, name, image_type):
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    output_file = "%s/%s.png" % (out_path, image_type)
    print("Copying file: %s to %s" % (input_file, output_file))
    if not __pretend__ : copyfile(input_file, output_file)

def process_directory(directory, files, out_dir):
    valid_zreps = defaultdict(int)

    for name in files:
        file_name, file_extension = os.path.splitext(name)
        splitted_name = file_name.split("_")
        material_zrep = splitted_name[-1]

        if ( file_extension in extensions and 
                  material_zrep.isdigit() and 
                  file_name[:2] != '._' ) :
            valid_zreps[material_zrep] += 1

            out_path = "%s/%s" % (out_dir, material_zrep)
            input_file = "%s/%s" % (directory, name)
            process_file (
                input_file, 
                out_path, 
                name, 
                'package' if valid_zreps[material_zrep] == 1 else 'box'
            )
            previous_file = name


def main():
    if(len(sys.argv) != 3):
        print("Usage: %s <input directory> <output directory>" % (sys.argv[0]))
        exit(1)

    src_dir = sys.argv[1]
    out_dir = sys.argv[2]

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    for root, dirs, files in os.walk(src_dir):
        print("Found directory: %s" % root)
        process_directory(root, files, out_dir)

if __name__ == "__main__":
    main()