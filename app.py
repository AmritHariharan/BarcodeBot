from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from os import listdir
from os.path import splitext, join
from generator import Generator

STATIC_IMAGES_DIR = 'static/images'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'mp3'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)


@app.route('/')
@app.route('/start')
def start():
    return render_template('base.html', images=listdir(STATIC_IMAGES_DIR))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_filename(filename):
    return splitext(filename)[0] + '.png'


@app.route('/', methods=['POST'])
def process_file():
    # check if the post request has a file
    if 'file' not in request.files:
        flash('No file in request')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        generator = Generator()
        Response(generator.generate_barcode(filename), mimetype='text/event-stream')
    return redirect(url_for('start'))


if __name__ == '__main__':
    app.run(debug=True)
