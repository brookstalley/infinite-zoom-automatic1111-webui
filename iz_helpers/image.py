from PIL import Image

def shrink_and_paste_on_blank(current_image, mask_width, mask_height):
    """
    Decreases size of current_image by mask_width pixels from each side,
    then adds a mask_width width transparent frame,
    so that the image the function returns is the same size as the input.
    :param current_image: input image to transform
    :param mask_width: width in pixels to shrink from each side
    :param mask_height: height in pixels to shrink from each side
    """

    # calculate new dimensions
    width, height = current_image.size
    new_width = width - 2 * mask_width
    new_height = height - 2 * mask_height

    # resize and paste onto blank image
    prev_image = current_image.resize((new_width, new_height))
    blank_image = Image.new("RGBA", (width, height), (0, 0, 0, 1))
    blank_image.paste(prev_image, (mask_width, mask_height))

    return blank_image  

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
    
    left = pan_width
    right = width - 1

    # to support panning left in the future
    if pan_width < 0:
        left = 0
        right = width + pan_width

    top = 0
    bottom = height - 1
    
    prev_image = current_image.crop((left, top, right, bottom))

    prev_image = prev_image.convert("RGBA")
    prev_image = np.array(prev_image)

    # create blank non-transparent image
    blank_image = np.array(current_image.convert("RGBA"))*0
    blank_image[:, :, 3] = 1

    # paste panned onto blank. if pan_width is negative, past on right side. If pan_width is positive, paste on left side
    if pan_width < 0:
        blank_image[-pan_width:0, width:height, :] = prev_image
    else:
        blank_image[0:height-1, 0 : (width-1)-pan_width, :] = prev_image

    return blank_image

