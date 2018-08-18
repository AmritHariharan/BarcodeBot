from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from redis import StrictRedis
from werkzeug.utils import secure_filename
from os import listdir
from os.path import join
from rq import Queue
from rq.job import Job

from generator import convert_filename, process_video
from settings import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

q = Queue(connection=StrictRedis(host=REDIS_HOST, port=REDIS_PORT))

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
        video_filename = join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        # file.save(video_file)
        print(video_filename)
        # Job data will be kept for 1 hour
        job = q.enqueue_call(
            process_video,
            args=(file,),
            result_ttl=3600
        )
        return redirect(url_for('start', filename=convert_filename(video_filename), job_id=job.get_id()))
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
    app.run(host='0.0.0.0', port=8080, debug=True)
