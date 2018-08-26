from setup import *

class EmotionsThread(threading.Thread):
    def __init__(self, thread_ID, stats, work_queue):
      threading.Thread.__init__(self)
      self.thread_ID = thread_ID
      self.stats = stats
      self.work_queue = work_queue
      self.exitflag = False
      print "Starting emotion thread ID : " + str(self.thread_ID)

    def run(self):
        while not self.exitflag:
            # print('Thread ' + str(self.thread_ID) + ' chillling, exit flag is ' + str(self.exitflag))
            EMO_MUTEX.acquire()
            if not self.work_queue.empty():
                face_img = self.work_queue.get()
                EMO_MUTEX.release()
                self.process_emotions(face_img)
            else:
                EMO_MUTEX.release()
            time.sleep(1)
        print('Emotion thread {0} exiting...'.format(self.thread_ID))
               
    def process_emotions(self, face_img):
        fer_dict = indicoio.fer(face_img)
        max_emotion = max(FACIAL_EMOTIONS, key=lambda x : fer_dict[x])
        self.stats.inc_emotion(max_emotion)
        # print('Emotion thread {0} : '.format(self.thread_ID) + max_emotion)
        # print('Size of workqueue: {0}'.format(self.work_queue.qsize()))

    def set_exit_flag(self):
        self.exitflag = True