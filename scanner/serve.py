import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from intent import scan

UPLOAD_FOLDER = 'tmp/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

application = Flask(__name__)
application.secret_key = "Yes123"
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return {
                "ERROR": "No file part in request params",
                "data": str(request.files)
            }
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {
                "ERROR": "No filename part in request params",
                "data": str(request.files)
            }

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(
                application.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return scan(file_path)

        return {"ERROR": "Can't parse request"}

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
