from PIL import Image
import cv2
from math import floor

class GenerateImage:

    def generate(self, filename):
        reader = cv2.VideoCapture(filename)
        success, image = reader.read()
        success = True;
        width = 720
        height = 480
        px_count = 0
        im_count = 1
        #print("1: %s    2: %s" % (image.shape[0], image.shape[1]))
        length = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))
        q_length = floor(length / width) # NOTE: THIS CANNOT BE 0

        print("pls")

        # Check that its not longer than 10 mins
        if length > 14400:
            print("Sorry, this video is too long, try again with a video under 10 minutes in length")
            quit() # TODO: find a more elegant way to do this

        while success:
            # 1. read in image
            success, image = reader.read()
            if im_count % q_length == 0:
                #print('Processing image %d' % px_count)
                pil_im = Image.fromarray(image) # get PIL image
                pil_im.show()
                # 2. get enumerated list of colours
                colours = pil_im.getcolors()
                # 3. get most dominant colour
                most_freq = colours[0]
                for count, colour in colours:
                    if count > most_freq(0):
                        most_freq = (count, colour)
                # 4. write to column of new image
                # TODO: this...
                # iterate
                px_count += 1
            im_count += 1

        # 5. write new image


if __name__ == "__main__":
	var = GenerateImage()
	print("starting")
	var.generate("stay.mp4")
