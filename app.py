from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from os import listdir
from os.path import splitext, join
from generator import generate_barcode

STATIC_IMAGES_DIR = 'static/images/examples'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'mp3'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Bootstrap(app)


@app.route('/')
@app.route('/start')
def start():
    return render_template('base.html', images=listdir(STATIC_IMAGES_DIR))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has a file
    if 'file' not in request.files:
        flash('No file in request')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
    if file and allowed_file(file.filename):
        video_file = join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(video_file)
        print(video_file)
        generate_barcode(video_file)
    return redirect(url_for('start'))


if __name__ == '__main__':
    app.run(debug=True)
