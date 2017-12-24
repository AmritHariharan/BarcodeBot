# BarcodeBot

This was inspired by my original barcode project which can be found [here](https://github.com/AmritHariharan/FilmBarcode2)). The idea is for this to work was a twitter bot, where people tweet youtube links at it, it downloads and processes the video, and tweets the generated barcode back at them.

## Todo:
- [x] Get barcode generation working
- [ ] Add youtube-dl functionality
- [ ] Integrate twitter
- [ ] Put in a Docker container(?)
- [ ] Get it hosted on AWS

## Tools Used

- Downloading videos: [youtube-dl](https://github.com/rg3/youtube-dl)
- Working with videos: [OpenCV](http://opencv-python-tutroals.readthedocs.io/en/latest/)
- Twitter integration: 
	- [Tweepy](http://www.tweepy.org/)
	- [This tweepy tutorial](https://scotch.io/tutorials/build-a-tweet-bot-with-python)
