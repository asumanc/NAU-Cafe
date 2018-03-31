
import face_recognition
import cv2
import numpy as np 
import pandas as pd 
from flask_table import Table, Col
from flask import Markup
from flask import Flask
from flask import render_template, Flask, request
import time 
app = Flask(__name__)
import datetime
import glob

font = cv2.FONT_HERSHEY_DUPLEX


def load_known_images():
    known_names = []
    known_encods = []

    for i in glob.glob("p/*.jpg"):
        name = i[2:-4]
        image = face_recognition.load_image_file(i)
        encoding = face_recognition.face_encodings(image)[0]

        known_names.append(name)
        known_encods.append(encoding)

    return known_names, known_encods


def face_a(frame):

    login_name="Unknown"
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    any_match = False
    print(len(face_encodings))
    for face_encoding in face_encodings:
        for ii in range(len(known_encods)):
            # See if the face is a match for the known face(s)

            match = face_recognition.compare_faces([known_encods[ii]], face_encoding)


            if match[0] == True:
                any_match = True
                login_name=known_names[ii]
                
    print(any_match, login_name)

    return any_match, login_name

known_names, known_encods = load_known_images()


print(known_names, len(known_encods))
@app.route("/")
def index():
    # Grab a single frame of video
   
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()


    any_match, login_name = face_a(frame)

    if any_match == True:
        return render_template("main.html", login_name = login_name)
    else:
        return render_template("index.html", login_name = login_name)


@app.route("/main")
def main():
    return render_template("main.html")


if __name__ == '__main__':

    app.run(host= '0.0.0.0',debug = True)



