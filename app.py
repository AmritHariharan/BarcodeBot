from sys import stderr

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from os import listdir

from validators import url

STATIC_IMAGES_DIR = 'static/images'

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
@app.route('/start')
def start():
    return render_template('start.html', images=listdir(STATIC_IMAGES_DIR))


@app.route('/generate', methods=['POST'])
def generate_barcode():
    video_url = request.form.get('url')
    print('URL: \'{0}\''.format(video_url), file=stderr)
    # if not url(video_url):
    #     return redirect(url_for('start') + '#errorModal')
    return redirect(url_for('start'))


if __name__ == '__main__':
    app.run()
