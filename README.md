# BarcodeBot

This was inspired by my original barcode project which can be found [here](https://github.com/AmritHariharan/FilmBarcode2)). The idea is for this to work was a twitter bot, where people tweet youtube links at it, it downloads and processes the video, and tweets the generated barcode back at them.

## Requirements

```
$ pip3 install opencv-python pytube validators tweepy
```

## Examples

### [Castle on the Hill (Ed Sheeran)](https://www.youtube.com/watch?v=K0ibBPhiaG0)

![Castle on the Hill (Ed Sheeran)](images/castle.png)

## Todo:
- [x] Get barcode generation working
- [x] Add youtube-dl functionality
- [x] Integrate twitter
- [ ] Put in a Docker container(?)
- [ ] Get it hosted on AWS/Google Cloud/Azure(???)

## Tools Used

- Downloading videos: [pytube](https://github.com/nficano/pytube)
- Working with videos: [OpenCV](http://opencv-python-tutroals.readthedocs.io/en/latest/)
- Twitter integration: [Tweepy](http://www.tweepy.org/)
- URL validation: [validator](https://github.com/kvesteri/validators)
