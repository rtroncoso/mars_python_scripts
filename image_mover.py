#!/usr/bin/python

import os, os.path, sys
from shutil import copyfile
from PIL import Image
from collections import defaultdict

__pretend__ = False
allowed_extensions = ['.jpg', '.jpeg', '.png']

def process_file(input_file, out_path, name, image_type):
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    output_file = "%s/%s.png" % (out_path, image_type)
    print("Copying file: %s to %s" % (input_file, output_file))
    if not __pretend__ : copyfile(input_file, output_file)

def process_directory(directory, files, out_dir):
    valid_zreps = defaultdict(int)
    dashes_counter = defaultdict(int)

    for name in files:
        file_name, file_extension = os.path.splitext(name)
        splitted_name = file_name.split("_")
        material_zrep = splitted_name[-1]

        if ( file_extension in allowed_extensions and 
                  material_zrep.isdigit() and 
                  len(material_zrep) == 6 and
                  valid_zreps[material_zrep] < 2 and
                  file_name[:2] != '._' ) :
            valid_zreps[material_zrep] += 1

            print("ZRep Number: %s, times: %d, previous dashes: %d, current dashes: %d" %
                (material_zrep, valid_zreps[material_zrep], 
                dashes_counter[material_zrep], len(splitted_name)))

            if ( len(splitted_name) < dashes_counter[material_zrep] or
                 dashes_counter[material_zrep] == 0 ):
                image_type = 'package'
            elif ( len(splitted_name) < dashes_counter[material_zrep] and
                   valid_zreps[material_zrep] == 2 ):
                image_type = 'package'
                copyfile("%s/%s/package.png" % (out_dir, material_zrep), 
                         "%s/%s/box.png" % (out_dir, material_zrep))
            else:
                image_type = 'box'

            out_path = "%s/%s" % (out_dir, material_zrep)
            input_file = "%s/%s" % (directory, name)
            process_file(input_file, out_path, name, image_type)
            dashes_counter[material_zrep] = len(splitted_name)

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