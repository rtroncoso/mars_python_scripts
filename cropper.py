# -*- coding: utf-8 -*-
from PIL import Image

def resize_and_crop(img, size, fill_white = True):
    """
    Resize and crop an image to fit the specified size.
    args:
        img: Image object
        size: `(width, height)` tuple.
    raises:
        Exception: if can not open the file in img of there is problems
            to save the image.
    """
    def fill_white_spaces(img):
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)

        return img

    # Compute variables
    src_width, src_height = img.size
    dst_width, dst_height = size

    # Get current and desired ratio for the images
    src_ratio = float(src_width) / float(src_height)
    dst_ratio = float(dst_width) / float(dst_height)

    #The image is scaled/cropped vertically or horizontally depending on the ratio
    if dst_ratio < src_ratio:
        crop_height = src_width # src_height
        crop_width = int(crop_height * dst_ratio) # crop_height * dst_ratio
        x_offset = 0 # int(float(src_width - crop_width) // 2)
        y_offset = int(crop_height // 2) - int(src_height // 2) # 0

    elif dst_ratio > src_ratio:
        crop_width = src_height # src_width
        crop_height = int(crop_width * dst_ratio) # crop_width * dst_ratio
        x_offset = int(crop_width // 2) - int(src_width // 2) # 0
        y_offset = 0 # int(float(src_height - crop_height) // 3)

    offset = (x_offset, y_offset)
    print(offset, crop_width, crop_height, src_width, src_height)

    img = img.convert("RGBA")
    new = Image.new(img.mode, (crop_width, crop_height), "white")
    new.paste(img, offset)
    new = new.resize((dst_width, dst_height), Image.ANTIALIAS)
    if fill_white: new = fill_white_spaces(new)
    
    return new