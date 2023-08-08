from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = r'C:\Users\Ashling Mccarthy\Programming\gait analysis\FEETPICS😊❤'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '':
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
            return f'File saved successfully! Path: {os.path.join(app.config["UPLOAD_FOLDER"], photo.filename)}'
    return 'No file selected or an error occurred.'

if __name__ == '__main__':
    app.run(debug=True)
