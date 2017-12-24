from PIL import Image
import cv2
import numpy as np
from math import floor

class GenerateImage:

    def generate(self, filename):
        reader = cv2.VideoCapture(filename)
        success, image = reader.read()
        success = True;
        width = len(image[0])
        height = len(image) 
        im_count = 1
        out = image

        length = int(reader.get(cv2.CAP_PROP_FRAME_COUNT))
        q_length = floor(length / width) # NOTE: THIS CANNOT BE 0

        # Check that its not longer than 10 mins
        if length > 14400:
            print("Sorry, this video is too long, try again with a video under 10 minutes in length")
            quit() # TODO: find a more elegant way to do this

        im_arr = np.zeros((height, width, 3))
        counter = 0

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
                for i in range(height):
                    out[i][counter][0] = most_freq[1][0]
                    out[i][counter][1] = most_freq[1][1]
                    out[i][counter][2] = most_freq[1][2]

                # iterate
                counter += 1
            if (counter == width-1):
                break
            im_count += 1
        im_count -= 1

        # 5. write new image
        final = Image.fromarray(out, 'RGB')
        final.save('output2.png')
        final.show()

if __name__ == "__main__":
	var = GenerateImage()
	#var.generate("stay.mp4")
	var.generate("zodiac.mp4")
