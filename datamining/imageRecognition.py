__author__ = 'Kevin'
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from numpy import *
import imageop


def img2binary(img, newimgid):
    img = Image.open(img)
    assert isinstance(img, Image.Image)
    img = img.convert("L")  # transfer the image into gray-scale
    img = img.filter(ImageFilter.MedianFilter(3))  # use median filter to de-noise
    enhencer = ImageEnhance.Contrast(img)  # to enhance the contrast of the image
    length = img.size[0]
    width = img.size[1]  # find the length and the width of the image
    counter = 0
    num_of_valid_pix = []  # this data structure is to store the number of valid pixels for each column.
    pixdata = img.load()  # load the image data into the @pixdata
    # retrival all the pixels in the image
    for x in range(0, length):
        for y in range(0, width):
            if pixdata[x, y] < 130:
                counter += 1
                pixdata[x, y] = 0  # reset the pixdata to binary form, 1 represents for valid pixel
            else:
                pixdata[x, y] = 255  # reset the pixdata to binary form, 0 represents for invalid pixel
        num_of_valid_pix.append(counter)
        counter = 0  # this counter is used to count the number of the pixel for each row
    letter_col_id = []
    i = 0
    # the following part is to separate the letters out
    # from the given CAPTCHA.
    while i in range(len(num_of_valid_pix)):
        letter_id = []  # @letter_id stores the cols for each letter
        # letter feature: there must be blank cols that contains no valid pixels
        # in the column
        while num_of_valid_pix[i] != 0:
            letter_id.append(i)
            if i < 119:
                i += 1
        if letter_id:
            letter_col_id.append(letter_id)
        i += 1
        # check the num of lines for each letter
    numofLetters = len(letter_col_id)
    # this part is dealing with the saparated
    for j in range(numofLetters):
        colsForLetter = len(letter_col_id[j])
        if colsForLetter in range(3, 25):
            file = open("trainingdigit/demo%d.txt" % newimgid, 'w')
            # listbuffer = []
            newimg = Image.new("L", (len(letter_col_id[j]), width))
            # newimg = newimg.load()
            for y in range(width):
                # rowbuffer = []
                i = 0
                for x in letter_col_id[j]:
                    # rowbuffer.append(pixdata[x, y])
                    # newimg[i, y] = pixdata[x, y]
                    if pixdata[x, y] == 255:
                        file.write("0")  # 0 for there's a invalid digit
                    elif pixdata[x, y] == 0:
                        file.write("1")  # 1 for there's a valid digit
                    newimg.putpixel([i, y], pixdata[x, y])
                    i += 1
                # listbuffer.append(rowbuffer)
                file.write("\n")
            file.close()
            newimg.save("trainingdigit/letter_%d.png" % newimgid, "PNG")
            newimgid += 1
    return newimgid
