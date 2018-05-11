# BarcodeBot

This was inspired by my original barcode project which can be found [here](https://github.com/AmritHariharan/FilmBarcode2)). The idea is for this to work was a twitter bot, where people tweet youtube links at it, it downloads and processes the video, and tweets the generated barcode back at them.

## Requirements

``` bash
# Set up virtualenv (optional)
$ python -m virtualenv VENV_NAME

# Activate virtualenv
$ source VENV_NAME/bin/activate

# Install packages
$ pip3 install opencv-python pytube validators tweepy
```

## Examples

### [Firestone (Kygo)](https://www.youtube.com/watch?v=9Sc-ir2UwGU)

![Firestone (Kygo)](images/firestone.png)

### [Castle on the Hill (Ed Sheeran)](https://www.youtube.com/watch?v=K0ibBPhiaG0)

![Castle on the Hill (Ed Sheeran)](images/castle.png)

## Todo:
- [x] Get barcode generation working
- [x] Add youtube-dl functionality
- [x] Integrate twitter
- [x] Fix downloading, pytube doesn't seem to like my options
- [ ] Fix  naming scheme, seems to be breaking the program if the filename has a `.` in it
- [ ] Put in a Docker container #webscale (?)
- [ ] Get it hosted on AWS/Google Cloud/Azure(???)

## Tools Used

- Downloading videos: [pytube](https://github.com/nficano/pytube)
- Working with videos: [OpenCV](http://opencv-python-tutroals.readthedocs.io/en/latest/)
- Twitter integration: [Tweepy](http://www.tweepy.org/)
- URL validation: [validator](https://github.com/kvesteri/validators)
