from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import cv2

video_camera = None
global_frame = None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', the_title='ElevAIte')

@app.route('/demo_status', methods=['POST'])
def demo_status():
    global video_camera 
    if video_camera == None:
        video_camera = VideoCamera()
 
    json = request.get_json()
 
    status = json['status']
 
    if status == "true":
        video_camera.start_record()
        return jsonify(result="started")
    else:
        video_camera.stop_record()
        return jsonify(result="stopped")

def video_stream():
    global video_camera 
  
    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
 
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, threaded=True)
