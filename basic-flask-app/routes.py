from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import cv2


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', the_title='ElevAIte')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
 
if __name__ == '__main__':
    app.run()
