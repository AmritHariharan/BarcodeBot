# Image/video processing stuff
from PIL import Image
import cv2
import numpy as np
from math import floor

# YouTube
from pytube import YouTube
from validators import url

from sys import stdout


class Generator:

    # Get the barcode from a video
    def generate_barcode(self, filename, output_filename):
        print('Generating a barcode')

        # Setup
        reader = cv2.VideoCapture(filename)
        success, image = reader.read()
        success = True
        height = len(image)
        width = len(image[0])
        im_count = 1
        out = image

        frame_count = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_count = frame_count / 2  # TODO: Find a better fix than this...
        q_length = floor(frame_count / width)  # NOTE: THIS CANNOT BE 0

        self.check_video_dimensions(frame_count, width)

        counter = 0

        while success:
            # 1. read in image
            success, image = reader.read()
            if im_count == q_length:
                im_count = 0
                counter += 1
                print('\rProgress: %d/%d' % (counter, width), end='\r')
                stdout.flush()
                self.write_column(counter, width, height, image, out)

            # break if you reach the end of the image array
            if counter == width:
                print('Finished processing image.')
                break
            im_count += 1

        # debug print statements
        print('length: {}'.format(frame_count))
        print('q_length: {}'.format(q_length))
        print('im_count: {}'.format(im_count))
        print('counter: {}'.format(counter))
        print('width: {}'.format(width))

        # 5. write new image
        final = Image.fromarray(out, 'RGB')
        final.save(output_filename)

    def write_column(self, column, width, height, image, final_image):
        for row in range(height):
            # 1. get row of image
            pil_im = Image.fromarray(image[row].reshape(1, width, 3))

            # 2. get enumerated list of colours
            im_colours = pil_im.getcolors(width)

            # 3. get most dominant colour in row
            most_freq = im_colours[0]
            for count, colour in im_colours:
                if count > most_freq[0]:
                    most_freq = (count, colour)

            # 4. write to of new image
            final_image[row][column - 1][0] = most_freq[1][0]
            final_image[row][column - 1][1] = most_freq[1][1]
            final_image[row][column - 1][2] = most_freq[1][2]

    def check_video_dimensions(self, frame_count, width):
        # Check that its not longer than 10 mins
        if frame_count > 54000:
            print("Sorry, this video is too long, try again with a video under 30 minutes in length")
            quit()  # TODO: find a more elegant way to do this
        # Check that its not too short
        if frame_count < width:
            print('Sorry, this video is too short (or possibly too high res)')
            quit()


if __name__ == '__main__':
    generator = Generator()
    generator.generate_barcode('firestone.mp4', 'firestone.png')
