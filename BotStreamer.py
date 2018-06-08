import tweepy
from validators import url
from Generator import Generator
from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)  # Twitter needs all requests to use OAuth for authentication
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


class BotStreamer(tweepy.StreamListener):

    def on_status(self, status):

        # get user/tweet info
        username = status.user.screen_name
        status_id = status.id

        print('got a status from {}'.format(username))

        # get url from tweet text
        link = status.entities['urls'][0]['expanded_url']
        print(link)

        barcode_generator = Generator()
        if url(link):
            barcode_generator.tweet_image(link, username, status_id)
        else:
            barcode_generator.tweet_msg('@{} sorry, \'{}\'  not a valid url'.format(username, link), status_id)
