# setup.py

import indicoio
import numpy as np
import cv2
import time
import Queue
import threading

INDICO_API_KEY = 'e9e61ec5e27e2f14c33cfaba8ab00585'

def setup():
	indicoio.config.api_key = INDICO_API_KEY

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

FACIAL_EMOTIONS = ['Happy', 'Sad', 'Angry', 'Fear', 'Surprise', 'Neutral']

VIDEO_CAPTURE_TIME_LIMIT = 50     		#seconds
CV2_FPS = 30
STANDARD_BOUND_BOX_SIZE = 56
STANDARD_EYE_CIRCLE_SIZE = 8
PUPIL_MOVEMENT_TOLERANCE_X = 0.5
PUPIL_MOVEMENT_TOLERANCE_Y = 0.4
STANDARD_EYE_BOX_DIFF_TOLERANCE_X = 10
STANDARD_EYE_BOX_DIFF_TOLERANCE_Y = STANDARD_EYE_BOX_DIFF_TOLERANCE_X
STANDARD_EYE_DIFF_TOLERANCE = 10

HAAR_CASCADE_EYE = 'haarcascade_eye.xml'
HAAR_CASCADE_FRONTAL_FACE = 'haarcascade_frontalface_default.xml'

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MUTEX = threading.Lock()
NUM_EMO_THREADS = 5