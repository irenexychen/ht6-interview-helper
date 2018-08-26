# setup.py
from key_words import *
import indicoio
import numpy as np
import cv2
import time
import Queue
import threading

##############
DEBUG = False
##############


INDICO_API_KEY = 'e9e61ec5e27e2f14c33cfaba8ab00585'

def setup():
	indicoio.config.api_key = INDICO_API_KEY

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

VIDEO_CAPTURE_TIME_LIMIT = 180     		#seconds
CV2_FPS = 10
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

EMO_MUTEX = threading.Lock()
GCLOUD_MUTEX = threading.Lock()
NUM_EMO_THREADS = 5

# Only use one thread to avoid conflicting results
NUM_GCLOUD_THREADS = 1
GCLOUD_TIMEOUT = 65.0	# seconds
language_code = 'en-US'  # a BCP-47 language tag





