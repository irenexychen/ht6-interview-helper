'''

Implement classes/functions for keeping track of stats to present to user
eg. words per minute (WPM)
    choice of words

'''
from setup import *
import json

class StatsCollector(object):
        
    def __init__(self):
        self.start_timestamp = time.time()
        self.end_timestamp = 0
        self.wpm_list = []
        self.facial_emotions = {emo : 0 for emo in FACIAL_EMOTIONS}
        self.pword_count = {word : 0 for word in POWERFUL_WORDS} 
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
    
    def normalize_emo_stats(self):
        s = float(sum(self.facial_emotions.values()))
        for k in self.facial_emotions.keys():
            self.facial_emotions[k] /= s

    def calc_eye_contact_rate(self):
        return float(self.eye_contact_frames) / self.total_frames

    def print_stats(self):
        print('===================')
        print('| Dumping stats |')
        print('===================')
        print('Start timestamp: {0}'.format(self.start_timestamp))
        print('End timestamp: {0}'.format(self.end_timestamp))
        print('Emotions: {0}'.format([emo + ' : ' + str(self.facial_emotions[emo]) for emo in FACIAL_EMOTIONS]))
        if self.total_frames:
            print('Eye contact rate: {0}'.format(self.calc_eye_contact_rate()))
        else:
            print('Eye contact rate: {0}'.format('0.0'))
        print('Total number of frames: {0}'.format(self.total_frames))

    def get_top_strong_words(self, count=3):
        top_words = sorted(POWERFUL_WORDS, key=lambda x : self.pword_count[x], reverse=True)[:count]
        return [(w, self.pword_count[w]) for w in top_words]

    def to_json(self, file_name):
        d = dict()
        d['top_strong_words'] = self.get_top_strong_words()
        d['facial_emotion_distribution'] = str(self.facial_emotions)
        if self.total_frames:
            d['eye_contact_freq'] = self.calc_eye_contact_rate()
        else:
            d['eye_contact_freq'] = 0.0
        d['wpm'] = self.wpm_list
        with open(file_name, 'w+') as f:
            json.dump(d, f)
