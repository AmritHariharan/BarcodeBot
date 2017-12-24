# Image/video processing stuff
from PIL import Image
import cv2
import numpy as np
from math import floor

# YouTube
from pytube import YouTube
from validators import url

# Twitter stuff
import requests
import tweepy
from io import BytesIO

from secrets import *


# Variables
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) # Twitter requires all requests to use OAuth for authentication
auth.set_access_token(access_token, access_secret) 
api = tweepy.API(auth)


# Get the barcode from a video
def generate_barcode(filename, outputfilename):

    print('Generating a barcode')

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
    if length > 54000:
        print("Sorry, this video is too long, try again with a video under 30 minutes in length")
        quit() # TODO: find a more elegant way to do this

    # Check that its not too short
    if length < width:
        print('Sorry, this video is too short (or possible too high res)')
        quit()

    counter = 0

    while success:
        # 1. read in image
        success, image = reader.read()
        numpy_im = np.array(image)
        if im_count == q_length:
            im_count = 0
            counter += 1
            for j in range(height):
                pil_im = Image.fromarray(image[j].reshape(1,width,3)) # get row of image 
                
                # 2. get enumerated list of colours
                im_colours = pil_im.getcolors(width)
                
                # 3. get most dominant colour in row
                most_freq = im_colours[0]
                for count, colour in im_colours:
                    if count > most_freq[0]:
                        most_freq = (count, colour)
                
                # 4. write to of new image
                out[j][counter-1][0] = most_freq[1][0]
                out[j][counter-1][1] = most_freq[1][1]
                out[j][counter-1][2] = most_freq[1][2]

        # break if you reach the end of the image array
        if (counter == width):
            print('at width')
            break
        im_count += 1

    print('length: {}'.format(length))
    print('q_length: {}'.format(q_length))
    print('im_count: {}'.format(im_count))
    print('counter: {}'.format(counter))
    print('width: {}'.format(width))
    # 5. write new image
    final = Image.fromarray(out, 'RGB')
    final.save(outputfilename)
    #final.show()


def tweet_image(link, username, status_id):
    # 1. Download it
    yt = YouTube(link)
    yt.streams.filter(only_video=True, file_extension='mp4').first().download()

    # 2. Generate the barcode
    outfile = yt.title + '.png'
    infile = yt.title + '.mp4'
    generate_barcode(infile, outfile)

    # 3. Tweet the image
    api.update_with_media(outfile, status='@{} here\'s \'{}\' as a #videobarcode'.format(username, yt.title), in_reply_to_status_id=status_id)
    print('@%s here\'s \'%s\' as a #videobarcode' % (username, yt.title))


def tweet_msg(msg, status_id):
    api.update_status(status=msg, in_reply_to_status_id=status_id)


class BotStreamer(tweepy.StreamListener):

    def on_status(self, status):

        # get user/tweet info
        username = status.user.screen_name
        status_id = status.id

        print('got a status from {}'.format(username))

        # get url from tweet text
        link = status.entities['urls'][0]['expanded_url']
        print(link)

        if url(link):
            tweet_image(link, username, status_id)
            #if 'youtube' in link:
            #    # is a link, tweet back the barcode
            #    tweet_image(link, username, status_id)
            #else:
            #    # not a youtube link
            #    tweet_msg('@{} sorry, this only work with full youtube links'.format(username), status_id)
        else:
            # not a link
            tweet_msg('@{} sorry, \'{}\'  not a valid url'.format(username, link), status_id)


def test():
    generate_barcode('zodiac.mp4', 'zodiac2.png')
    generate_barcode('perfect.mp4', 'perfect.png')


#test()

myStreamListener = BotStreamer()

# Construct the Stream instance
stream = tweepy.Stream(auth, myStreamListener)
print('running...')
stream.filter(track=['@videobarcode'])
