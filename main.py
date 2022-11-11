import webbrowser
import pandas as pd
import numpy as np
import cv2
import time
from flask import Flask, render_template, request, Response, redirect, flash
from video_emotion_recognition import gen_frames_2, get_max
import os
import uuid

UPLOAD_FOLDER = 'files'
app = Flask(__name__)


@app.route('/save-record', methods=['POST'])
def save_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = str(uuid.uuid4()) + ".mp3"
    full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    file.save(full_file_name)
    return render_template("voice.html")

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/qna')
def qna():
    return render_template("QNA.html")

@app.route('/voice')
def voice():
    return render_template("voice.html")

@app.route('/results')
def results():
    return render_template("results.html")


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames_2(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:2000/')
    app.run(debug=True, port=2000)
