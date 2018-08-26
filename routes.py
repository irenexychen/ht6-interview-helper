from __future__ import print_function
from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import src.main as lib_processing
import logging
from logging.handlers import RotatingFileHandler
import sys


video_camera = None
global_frame = None

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', the_title='ElevAIte')

@app.route('/demo_status', methods=['POST'])
def demo_status():
    # global video_camera 
    # if video_camera == None:
    #     video_camera = VideoCamera()
 
    json = request.get_json()
 
    status = json['status']
 
    print('kms!', file=sys.stderr)
    sys.stderr.flush()

    if status == "true":
        # app.logger.warning('A warning occurred (%d apples)', 42)
        # app.logger.error('An error occurred')   
        
        # video_camera.start_record()
        print("testing INFO", file=sys.stderr)
        sys.stderr.flush()
        sys.stdout.flush()
        lib_processing.main(emo=False,gcloud=False)
        return jsonify(result="started")
    else:
        print("rip in pieces", file=sys.stderr)
        sys.stderr.flush()
        # video_camera.stop_record()
        return jsonify(result="stopped")

# def video_stream():
    # global video_camera 
  
    # if video_camera == None:
    #     video_camera = VideoCamera()
        
    # while True:
    #     frame = video_camera.get_frame()
    #     yield (b'--frame\r\n'
    #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @app.route('/video_viewer')
# def video_viewer():
#     # return Response(video_stream(),
#     #                 mimetype='multipart/x-mixed-replace; boundary=frame')

 
if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=True)
