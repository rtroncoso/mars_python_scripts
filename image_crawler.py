#!/usr/bin/python

import os, os.path, sys
from shutil import copyfile
from PIL import Image
from collections import defaultdict

__pretend__ = False
allowed_extensions = ['.jpg', '.jpeg', '.png']
amount_adobe = 0

def process_file(input_file, out_path, name):
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    output_file = "%s/%s" % (out_path, name)
    print("Copying file: %s to %s" % (input_file, output_file))
    if not __pretend__ : copyfile(input_file, output_file)

def all_images_counter(directory, files):
    for name in files:
        file_name, file_extension = os.path.splitext(name)

        if ( file_extension in allowed_extensions and 
                  file_name[:2] != '._' ) :
            print("[ALLIMG]: Filename: %s, Extension: %s" % (file_name, file_extension))
            out_path = "all_images"

            if not os.path.isdir(out_path):
                os.makedirs(out_path)

            input_file = "%s/%s" % (directory, name)
            process_file(input_file, out_path, name)

def repeated_images(directory, files):
    for name in files:
        file_name, file_extension = os.path.splitext(name)

        if ( file_extension in allowed_extensions and 
                  file_name[:2] == '._' ) :
            print("[REPEATED]: Filename: %s, Extension: %s" % (file_name, file_extension))
            out_path = "repeated_images"

            if not os.path.isdir(out_path):
                os.makedirs(out_path)

            input_file = "%s/%s" % (directory, name)
            process_file(input_file, out_path, name)

def adobe_files(directory, files):
    for name in files:
        file_name, file_extension = os.path.splitext(name)

        if ( file_extension in ['.psd', '.eps'] and 
                  file_name[:2] != '._' ) :
            amount_adobe += 1
            print("[ADOBE]: Filename: %s, Extension: %s, Number: %d" % 
                (file_name, file_extension, amount_adobe))

def main():
    if(len(sys.argv) != 2):
        print("Usage: %s <input directory>" % (sys.argv[0]))
        exit(1)

    src_dir = sys.argv[1]

    for root, dirs, files in os.walk(src_dir):
        print("Found directory: %s" % root)
        all_images_counter(root, files)
        repeated_images(root, files)
        adobe_files(root, files)

    printf("Amount of Adobe files: %d", amount_adobe)

if __name__ == "__main__":
    main()