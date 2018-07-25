from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from os import listdir
from os.path import splitext, join
from generator import generate_barcode
from celery import Celery

STATIC_IMAGES_DIR = 'static/images/examples'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'mp3'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Celery config
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

Bootstrap(app)


@app.route('/')
@app.route('/start')
def start():
    return render_template('base.html', images=listdir(STATIC_IMAGES_DIR))


@celery.task(bind=True)
def generate_image_task(self, filename):
    return generate_barcode(filename, self)


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
        filename = secure_filename(file.filename)
        file.save(join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        task = generate_image_task.delay(filename)
        return jsonify({}), 202, {'Location': url_for('taskstatus',task_id=task.id)}
    return redirect(url_for('start'))


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = generate_image_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        # job did not start yet
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
