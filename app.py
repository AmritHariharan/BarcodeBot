from sys import stderr

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from os import listdir, path

from werkzeug.utils import secure_filename

STATIC_IMAGES_DIR = 'static/images'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST'])
def process_file():
    # check if the post request has a file
    if 'file' not in request.files:
        flash('No file in request')
        return redirect(request.url)
    file = request.files['file']
    print(file)
    # if user does not select file, browser also submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('start'))


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
