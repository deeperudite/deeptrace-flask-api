from flask_restful import Resource, Api, reqparse
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = os.getcwd()+'/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'csv'])

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
CORS(app)
parser = reqparse.RequestParser()

class DeepTracer(Resource):

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def post(self):
        parser.add_argument('split',type=str)
        parser.add_argument('model',type=str)
        args = parser.parse_args()
        split = args['split']
        model = args['model']
        file = request.files['file']
        if file and self.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = data.head().to_json(orient='index')
            fs = "Uploaded"
        else:
            fs = "Not Uploaded"
        return {'split':split, 'model': model, 'file': fs, 'data': data}

api.add_resource(DeepTracer, '/')

if __name__ == '__main__':
    app.run()
