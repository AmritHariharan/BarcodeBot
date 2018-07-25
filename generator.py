# Image/video processing stuff
from PIL import Image
import cv2
import numpy as np
from math import floor

# YouTube
from pytube import YouTube
from validators import url

from sys import stdout


# Get the barcode from a video
def generate_barcode(filename, outputfilename):
    print('Generating a barcode')

    reader = cv2.VideoCapture(filename)
    success, image = reader.read()
    success = True
    height = len(image)
    width = len(image[0])
    im_count = 1
    out = image

    length = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))
    length = length / 2  # TODO: Find a better fix than this...
    q_length = floor(length / width)  # NOTE: THIS CANNOT BE 0

    # Check that its not longer than 10 mins
    if length > 54000:
        print("Sorry, this video is too long, try again with a video under 30 minutes in length")
        quit()  # TODO: find a more elegant way to do this

    # Check that its not too short
    if length < width:
        print('Sorry, this video is too short (or possible too high res)')
        quit()

    counter = 0

    while success:
        # 1. read in image
        success, image = reader.read()
        if im_count == q_length:
            im_count = 0
            counter += 1
            print('\rProgress: %d/%d' % (counter, width), end='\r')
            stdout.flush()
            for j in range(height):
                pil_im = Image.fromarray(image[j].reshape(1, width, 3))  # get row of image

                # 2. get enumerated list of colours
                im_colours = pil_im.getcolors(width)

                # 3. get most dominant colour in row
                most_freq = im_colours[0]
                for count, colour in im_colours:
                    if count > most_freq[0]:
                        most_freq = (count, colour)

                # 4. write to of new image
                out[j][counter - 1][0] = most_freq[1][0]
                out[j][counter - 1][1] = most_freq[1][1]
                out[j][counter - 1][2] = most_freq[1][2]

        # break if you reach the end of the image array
        if counter == width:
            print('at width')
            break
        im_count += 1

    # debug print statements
    print('length: {}'.format(length))
    print('q_length: {}'.format(q_length))
    print('im_count: {}'.format(im_count))
    print('counter: {}'.format(counter))
    print('width: {}'.format(width))

    # 5. write new image
    final = Image.fromarray(out, 'RGB')
    final.save(outputfilename)


def test():
    generate_barcode('firestone.mp4', 'firestone.png')
    generate_barcode('stay.mp4', 'stay.png')
