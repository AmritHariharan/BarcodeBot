import cv2
#import numpy as np

class GenerateImage:

	def generate(self, filename):
		reader = cv2.VideoCapture(filename)
		success, image = reader.read()
		count = 0
		success = True;
		while success:
			success, image = reader.read()
			print('Read a new frame: ', success)
			cv2.imwrite("frame%d.png" % count, image)
			count += 1
			average_color = [img[:, :, i].mean() for i in range(img.shape[-1])] # does this work???
			