import cv2
#import youtube_dl
#import numpy as np

# Logger object for youtube_dl output
#class MyLogger(object):
#    def debug(self, msg):
#        pass
#
#    def warning(self, msg):
#        pass
#
#    def error(self, msg):
#        print(msg)
#
# not sure what this is but according to the documentation I need it...        
#def my_hook(d):
#    if d['status'] == 'finished':
#        print('Done downloading, now converting ...')

class GenerateImage:

	def download_link(self, link):
		print("test")	
		
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
			

if __name__ == "__main__":
	var = GenerateImage()
	
	var.generate(stay.mp4)
			