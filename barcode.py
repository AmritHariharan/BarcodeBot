from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
@app.route('/start')
def homepage():
    return render_template('start.html')


@app.route('/healthcheck')
def healthcheck():
    return 'Running'


@app.route('/generate')
def generate_barcode():
    return 'This is a barcode.'


if __name__ == '__main__':
    app.run()
