import indicoio
import numpy as np
import cv2

FACIAL_EMOTIONS = ['happy', 'sad', 'angry', 'fear', 'surprise', 'neutral']

def get_facial_emotion_score(fer_dict, emotion):
	assert (emotion in FACIAL_EMOTIONS)
	return fer_dict[emotion]

def get_facial_emotion(img, detect=False, sensitivity=0.8):
	return indicoio.fer(img)