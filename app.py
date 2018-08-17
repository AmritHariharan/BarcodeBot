from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from os import listdir
from os.path import join
from generator import generate_barcode, convert_filename
from rq import Queue
from rq.job import Job
from worker import conn

STATIC_IMAGES_DIR = 'static/images/examples'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'mp3'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

q = Queue(connection=conn)

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
        # Job data will be kept for 6 hours
        job = q.enqueue_call(
            generate_barcode,
            args=(video_file,),
            result_ttl=21600
        )
        return redirect(url_for('start', filename=convert_filename(video_file), job_id=job.get_id()))
    return redirect(url_for('start', error='Sorry, something went wrong while uploading'))


@app.route('/status/<job_id>', methods=['GET'])
def status(job_id):
    job = Job.fetch(job_id, connection=conn)
    if job.is_queued:
        return 'QUEUED', 201
    elif job.is_started:
        return job.meta.progress, 202
    elif job.is_finished:
        return job.result, 200
    elif job.is_failed:
        return job.result, 500
    else:
        return 'ERROR', 500


if __name__ == '__main__':
    app.run(debug=True)
