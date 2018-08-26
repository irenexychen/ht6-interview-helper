'''

Implement classes/functions for keeping track of stats to present to user
eg. words per minute (WPM)
	filler word counter

'''
from setup import *

class StatsCollector(object):
		
	def __init__(self):
		self.num_filler_words = 0
		self.num_words = 0
		self.pos_word_choices = 0
		self.neg_word_choices = 0
		self.start_timestamp = time.time()
		self.end_timestamp = 0
		self.facial_emotions = {emo : 0 for emo in FACIAL_EMOTIONS}
		self.eye_contact_frames = 0
		self.total_frames = 0

	def inc_total_frames(self):
		self.total_frames += 1
		
	def inc_num_filler_words(self):
		self.num_filler_words += 1
	
	def inc_num_words(self):
		self.num_words += 1
	
	def inc_pos_words(self):
		self.pos_word_choices += 1
	
	def inc_neg_words(self):
		self.neg_word_choices += 1

	def inc_eye_contact_frames(self):
		self.eye_contact_frames += 1

	def inc_emotion(self, emotion):
		assert(emotion in FACIAL_EMOTIONS)
		self.facial_emotions[emotion] += 1
	
	def finish(self):
		assert(self.end_timestamp == 0)
		self.end_timestamp = time.time()
		# self.normalize_emo_stats()
	
	def get_elapsed_time(self):
		assert(self.end_timestamp != 0)
		return self.end_timestamp - self.start_timestamp
	
	def get_wpm(self):
		assert(self.end_timestamp != 0)
		return self.num_words / self.get_elapsed_time()
	
	def normalize_emo_stats(self):
		s = float(sum(self.facial_emotions.values()))
		for k in self.facial_emotions.keys():
			self.facial_emotions[k] /= s

	def calc_eye_contact_rate(self):
		return float(self.eye_contact_frames) / self.total_frames

	def dump_stats(self):
		print('===================')
		print('| Dumping stats |')
		print('===================')
		print('Number of filler words: {0}'.format(self.num_filler_words))
		print('Number of words: {0}'.format(self.num_words))
		print('Number of positive word choices: {0}'.format(self.pos_word_choices))
		print('Number of negative word choices: {0}'.format(self.neg_word_choices))
		print('Start timestamp: {0}'.format(self.start_timestamp))
		print('End timestamp: {0}'.format(self.end_timestamp))
		print('Emotions: {0}'.format([emo + ' : ' + str(self.facial_emotions[emo]) for emo in FACIAL_EMOTIONS]))
		print('Eye contact rate: {0}'.format(self.calc_eye_contact_rate()))
		print('Total number of frames: {0}'.format(self.total_frames))
