from flask import Flask, flash, render_template, request
from werkzeug import secure_filename
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd()+'/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'])

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', endpoint='uploadform')
def uploadform():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'], endpoint='uploadfile')
def uploadfile():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # Get the list of files to upload.
        uploaded_files = request.files.getlist('file')
        print("File : ", file)
        print("Uploaded Files : ", uploaded_files)

        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        counter = 0
        length = len(uploaded_files)
        # Iterate over the list of files.
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                counter += 1
            if (counter == length):
                flash('File(s) successfully uploaded')
        return redirect('/upload')

    return ""


if __name__ == "__main__":
    app.run(debug=True)
