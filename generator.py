from PIL import Image
import cv2
import numpy as np
from math import floor

class GenerateImage:

    def generate(self, filename):
        reader = cv2.VideoCapture(filename)
        success, image = reader.read()
        success = True;
        width = 640
        height = 360
        px_count = 0
        im_count = 1
        #print("1: %s    2: %s" % (image.shape[0], image.shape[1]))
        length = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))
        q_length = floor(length / width) # NOTE: THIS CANNOT BE 0

        # Check that its not longer than 10 mins
        if length > 14400:
            print("Sorry, this video is too long, try again with a video under 10 minutes in length")
            quit() # TODO: find a more elegant way to do this

        colours = []

        while success:
            # 1. read in image
            success, image = reader.read()
            if im_count % q_length == 0:
                pil_im = Image.fromarray(image) # get PIL image
                
                # 2. get enumerated list of colours
                im_colours = pil_im.getcolors(width * height)
                
                # 3. get most dominant colour
                most_freq = im_colours[0]
                for count, colour in im_colours:
                    if count > most_freq[0]:
                        most_freq = (count, colour)
                
                # 4. write to column of new image
                colours.append(most_freq)
                # iterate
                px_count += 1
            im_count += 1
        im_count -= 1

        # 5. write new image
        im_arr = np.array(colours)
        im_arr = np.resize(im_arr, (480,len(im_arr))) 
        final = Image.fromarray(im_arr, mode='RGB')
        final.save('output.png')
        final.show()

if __name__ == "__main__":
	var = GenerateImage()
	#var.generate("stay.mp4")
	var.generate("zodiac.mp4")
