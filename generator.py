#import os
import cv2
from sklearn.cluster import KMeans
from math import floor
#from colorthief import ColorThief
#import numpy as np

#os.system("cd ..")

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

		# Check that its not longer than 10 mins
		if length > 14400:
			print("Sorry, this video is too long, try again with a video under 10 minutes in length")
			quit() # TODO: find a more elegant way to do this

		while success:
			success, image = reader.read()
			#print('Read a new frame: ', success)
			if im_count % q_length == 0:
				print('Processing image %d' % px_count)
				cv2.imwrite("%s-frame%d.png" % (filename, px_count), image)
				px_count += 1
			im_count += 1


if __name__ == "__main__":
	var = GenerateImage()
	var.generate("stay.mp4")
