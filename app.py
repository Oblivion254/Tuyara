from flask import *  
import feature_extraction
from keras.models import load_model
import cv2
import numpy as np
import os
# from camera import VideoCamera

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

app = Flask(__name__)  

@app.route('/')  
def index():  
    return render_template("index.html") 
 
@app.route('/text')  
def text():  
    return render_template("text.html") 

@app.route('/audio')  
def audio():  
    return render_template("record.html")

@app.route('/image')   
def image():  
    return render_template("image.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('image.html', message='No file part')
    file = request.files['file']
    if file.filename == '':
        return render_template('image.html', message='No image selected')
    if file:
        try:
            nparr = np.fromstring(file.read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            emotion = feature_extraction.detect_emotionIMG(img)
            return render_template('result.html', emotion=emotion)
        except Exception as e:
            print(e)
            return render_template('image.html', message='Error processing image')
    return render_template('image.html')
 
@app.route('/video')  
def video():  
    return render_template("video.html") 

@app.route('/video/video_feed')
def video_feed():
    return Response(feature_extraction.detect_emotion(), mimetype='multipart/x-mixed-replace; boundary=frame')
 
@app.route('/about') 
def about():  
    return render_template("aboutus.html") 

@app.route('/feedback') 
def feedback():  
    return render_template("leave_feedback.html") 


@app.route('/emotion', methods = ['POST'])   
def emotion():  
    if request.method == 'POST':  
        if request.form['form-name'] == "image":
            if request.files['image']:
                return render_template("image.html")

        elif request.form['form-name'] == "text":
            if request.form['text']:
                text = request.form['text']  
                result = feature_extraction.text_cleaning(text)

                return render_template("text.html", name = result) 
            else:
                return render_template("text.html") 

        elif request.form['form-name'] == "audio":
            if request.files['audio']:
                audiof = request.files['audio'] 
                audiof.save(audiof.filename) 
                result = feature_extraction.audio_prediction(audiof.filename)

                # Remove file after processing
                if os.path.exists(audiof.filename):
                    os.remove(audiof.filename)

                return render_template("record.html", name = result) 
            else:
                return render_template("record.html") 

        elif request.form['form-name'] == "video":
            if request.files['video']:
                videof = request.files['video'] 
                videof.save(videof.filename) 
                result = feature_extraction.video_prediction(videof.filename)


                # Remove file after processing
                if os.path.exists(videof.filename):
                    os.remove(videof.filename)

                return render_template("video.html", name = result) 
            else:
                return render_template("video.html") 

        elif request.form['form-name'] == "feedback":
            if request.form['feedback']:
                text = request.form['feedback']  
                response = feature_extraction.feedback(text)

                return render_template("leave_feedback.html", name = response) 
            else:
                return render_template("leave_feedback.html") 
  
if __name__ == '__main__':  
    app.run(debug = True, host="0.0.0.0",port=5000)  