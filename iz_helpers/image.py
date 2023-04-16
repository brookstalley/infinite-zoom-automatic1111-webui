import requests
from PIL import Image
import numpy as np


def shrink_and_paste_on_blank(current_image, mask_width):
    """
    Decreases size of current_image by mask_width pixels from each side,
    then adds a mask_width width transparent frame, 
    so that the image the function returns is the same size as the input. 
    :param current_image: input image to transform
    :param mask_width: width in pixels to shrink from each side
    """

    height = current_image.height
    width = current_image.width

    # shrink down by mask_width
    prev_image = current_image.resize(
        (height-2*mask_width, width-2*mask_width))
    prev_image = prev_image.convert("RGBA")
    prev_image = np.array(prev_image)

    # create blank non-transparent image
    blank_image = np.array(current_image.convert("RGBA"))*0
    blank_image[:, :, 3] = 1

    # paste shrinked onto blank
    blank_image[mask_width:height-mask_width,
                mask_width:width-mask_width, :] = prev_image
    prev_image = Image.fromarray(blank_image)

    return prev_image

def pan_and_paste_on_blank(current_image, pan_width):
    """
    Crops the image to remove pan_width on either left or right,
    then adds a mask_width width transparent frame, 
    so that the image the function returns is the same size as the input. 
    :param current_image: input image to transform
    :param pan_width: width in pixels to cut from left (if negative) or right (if positive)
    """

    height = current_image.height
    width = current_image.width

    # crop pan_width pixels. if pan_width is negative, crop from the left. if pan_width is positive, crop from the right
    if pan_width < 0:
        prev_image = current_image.crop((0, 0, width+pan_width, height))
    else:
        prev_image = current_image.crop((pan_width, 0, width, height))

    prev_image = prev_image.convert("RGBA")
    prev_image = np.array(prev_image)

    # create blank non-transparent image
    blank_image = np.array(current_image.convert("RGBA"))*0
    blank_image[:, :, 3] = 1

    # paste panned onto blank. if pan_width is negative, past on right side. If pan_width is positive, paste on left side
    if pan_width < 0:
        blank_image[-pan_width:0, width:height, :] = prev_image
    else:
        blank_image[0:0, (width-1)-pan_width : (height-1), :] = prev_image

    prev_image = Image.fromarray(blank_image)

    return prev_image
