#import os
import cv2
from sklearn.cluster import KMeans
from math import ceil
#from colorthief import ColorThief
#import numpy as np

#os.system("cd ..")

class GenerateImage:

	def generate(self, filename):
		reader = cv2.VideoCapture(filename)
		success, image = reader.read()
		success = True;
		#n_colors = 1
		width = 720
		height = 480
		px_count = 0
		im_count = 1
		#print("1: %s    2: %s" % (image.shape[0], image.shape[1]))
		w = image.shape[1]
		q_length = ceil(w / width) # NOTE: THIS CANNOT BE 0
		print("q length: %s" % q_length)


		while success:
			success, image = reader.read()
			print('Read a new frame: ', success)
			if im_count % q_length == 0:
				print('Writing an image')
				cv2.imwrite("%s-frame%d.png" % (filename, im_count), image)
			im_count += 1

			# Average colour
			#average_color = [img[:, :, i].mean() for i in range(img.shape[-1])] # does this work???


if __name__ == "__main__":
	var = GenerateImage()
	var.generate("stay.mp4")
