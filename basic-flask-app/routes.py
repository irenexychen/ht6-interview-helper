from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import cv2

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', the_title='ElevAIte')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/camera')
def camera():
	return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('get-ready.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')











if __name__ == '__main__':
    app.run(debug=True)

    
