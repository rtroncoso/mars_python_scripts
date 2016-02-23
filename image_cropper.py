#!/usr/bin/python

import os, os.path, sys
from PIL import Image
from cropper import resize_and_crop

__pretend__ = False
extensions = ['.jpg', '.jpeg', '.png']
allowed_names = ['package', 'box']
sizes = {
    'package': {
        'hdpi': (512, 'png'),
        'mdpi': (256, 'png'),
        'ldpi': (128, 'png'),
        'thumbnail': (100, 'png'),
    },

    'box': {
        'hdpi': (512, 'png'),
        'mdpi': (256, 'png'),
        'ldpi': (128, 'png'),
        'thumbnail': (100, 'png'),
    }
}

def generate_file_names(file_name, directory):
    # Yield up original hardcoded image
    yield 'package-original.png', 'original', 'png'
    
    # Process image sizes
    for package_type, package_formats in sizes.items():
        for format, options in package_formats.items():
            size = options[0]
            extension = options[1]
            new_file_name = "%s-%s-%sx%s.%s" % (package_type, format, size, size, extension)
            yield new_file_name, size, extension

def process_directory(directory, files, out_dir):
    for name in files:
        file_name, file_extension = os.path.splitext(name)
        material_zrep = os.path.basename(directory)

        if ( file_extension in extensions and 
                file_name in allowed_names and
                material_zrep.isdigit() ):
            for out_name, out_size, out_extension in generate_file_names(name, material_zrep):
                out_path = "%s/%s" % (out_dir, material_zrep)
                input_file = "%s/%s" % (directory, name);
                process_file(input_file, out_path, out_name, out_size)

def process_file(input_file, out_path, out_name, out_size):
    if not os.path.isdir(out_path):
        os.makedirs(out_path)

    im = Image.open(input_file)
    out_file = "%s/%s" % (out_path, out_name)

    if out_size != "original":
        im = resize_and_crop(im, (out_size, out_size))

    print("\tProcessing input file: %s to output %s" % (input_file, out_file))
    if not __pretend__ : im.save(out_file, optimize=True)

def main():
    if(len(sys.argv) != 3):
        print("Usage: %s <input directory> <output directory>" %
            (sys.argv[0]))
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
