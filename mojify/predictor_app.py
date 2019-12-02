import flask
from flask import request, redirect, flash, send_from_directory
from predictor_api import make_prediction
import os
from werkzeug.utils import secure_filename


PHOTO_FOLDER = os.path.join('static', 'photos')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Initialize the app

app = flask.Flask(__name__)
app.config['UPLOAD_FOLDER'] = PHOTO_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route("/", methods=["POST", "GET"])
def show_image():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect('/')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            input = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            input_image, prediction = make_prediction(input_image=input)
            return flask.render_template('predictor.html',
                                         uploaded_photo=input_image,
                                         prediction=prediction)
    return flask.render_template('predictor.html', uploaded_photo='', prediction='')

# Start the server, continuously listen to requests.

if __name__=="__main__":
    # For local development:
    app.run(debug=True)
    # For public web serving:
    #app.run(host='0.0.0.0')
    app.run()
