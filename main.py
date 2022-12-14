import webbrowser
import pandas as pd
import numpy as np
import cv2
import time
from flask import Flask, render_template, request, Response, redirect, flash
from video_emotion_recognition import gen_frames_2, get_max
import os
import uuid
from pred import Pred_regressor, Pred_classifier
from speech_emotion_recognition import speech_emotion_recognition
from speech_to_text import get_large_audio_transcription
from text_emotion_recognition import predict
# from record_speech import record_speech

UPLOAD_FOLDER = 'files'
app = Flask(__name__)


@app.route('/voice_temp', methods=['GET', 'POST'])
def save_record():
    return render_template("voice.html")


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/submit-data', methods=['GET', 'POST'])
def sub():
    global happiness_index, emotion, label
    form_data = request.form
    arr = [form_data['lifes'], form_data['mhealth'], form_data['hs'], form_data['ltd'], form_data['wh'],
           form_data['sh'], form_data['scp'], form_data['pf'], form_data['ss'], form_data['fam'], form_data['vc'],
           form_data['ass'], form_data['hhi'], form_data['hhq']]
    # arr = [form_data['lifes']]
    arr = [int(elem) for elem in arr]
    print(arr)
    res = Pred_regressor(arr)
    print(res[0])
    happiness_index = round(abs(res[0]), 2)
    emotion = get_max()
    label = Pred_classifier(arr)
    return render_template('record.html', happiness_index=happiness_index, emotion=emotion, label=label)


@app.route('/qna')
def qna():
    return render_template("QNA.html")


@app.route('/voice')
def voice():
    return render_template("record.html", happiness_index=happiness_index, emotion=emotion, label=label)


@app.route('/run_voice', methods=['GET', 'POST'])
def run_voice():
    # ans = record_speech()
    Speech_Emotion = f"Speech Emotion: {speech_emotion_recognition()}"
    Text = f"Text: {get_large_audio_transcription()}"
    Text_Emotion = f"Text Emotion: {predict()}"
    return render_template("results.html", Speech_Emotion=Speech_Emotion, Text=Text, Text_Emotion=Text_Emotion,
                           happiness_index=happiness_index, emotion=emotion, label=label[0])


@app.route('/results')
def results():
    return render_template("results.html")


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames_2(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:2000/')
    app.run(debug=True, port=2000)
