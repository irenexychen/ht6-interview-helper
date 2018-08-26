from setup import *
from stats_collector import StatsCollector
from emo_thread import EmotionsThread
from gcloud_thread import GCloudThread
# eyetracking - see if person is making eye contact 

class InterviewAI(object):

    def __init__(self, stats, video_path=None, 
                 is_demo=False, 
                 run_eye_tracker=True,
                 run_emo_threads=True, 
                 run_gcloud_threads=True):
        self.stats = stats
        self.start_time = time.time()
        self.video_path = video_path
        self.is_demo = is_demo
        self.work_queue = Queue.Queue()
        self.run_eye_tracker = run_eye_tracker
        self.emo_threads = []
        self.run_emo_threads = run_emo_threads
        self.gcloud_threads = []
        self.run_gcloud_threads = run_gcloud_threads

    def setup(self):
        self.cap = cv2.VideoCapture(self.video_path) if self.video_path else cv2.VideoCapture(0)

        try:
            self.cap.set(3, 640)
            self.cap.set(4, 480)
        except:
            print('Warning : Unable to set webcame resolution to 640x480')

        self.img_height = self.cap.get(3)
        self.img_width =  self.cap.get(4)

        self.cap.set(cv2.CAP_PROP_FPS, CV2_FPS)

        if self.run_emo_threads:
            self.launch_emo_threads()

        if self.run_gcloud_threads:
            self.launch_gcloud_threads()


    def begin(self):
        self.setup()
        print('Launching interviewer...')
        while (time.time() - self.start_time < VIDEO_CAPTURE_TIME_LIMIT):
            ret, img = self.cap.read()
            if ret == True:
                if self.run_eye_tracker:
                    self.process_eye_contact(img)

                if self.run_emo_threads:
                    img, cropped_face = self.crop_face(img)
                    # Indico API is slow, so use threads to parallelize
                    if cropped_face is not None:
                        EMO_MUTEX.acquire()
                        self.work_queue.put(cropped_face)
                        EMO_MUTEX.release()

                # if cropped_face is not None:
                #     img = self.process_emotions(img, cropped_face)

                if self.is_demo:
                    cv2.imshow('Face', img)

            self.stats.inc_total_frames()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                 break

        self.cap.release()
        cv2.destroyAllWindows()

        # wait for threads to finish processing
        if self.run_emo_threads:
            while not self.work_queue.empty():
                pass

            print ('Set emotion thread exit flags to TRUE...')

            for t in self.emo_threads:
                t.set_exit_flag()
                t.join()

        if self.run_gcloud_threads:
            print ('Set Google Cloud thread exit flags to TRUE...')
            for t in self.gcloud_threads:
                t.set_exit_flag()
                t.join()

        print ("Interviewer module exiting...")
        self.stats.finish()

    ######################################################
    # Functions for processing eye contact
    ######################################################

    def process_eye_contact(self, img):
        eyes = cv2.CascadeClassifier(HAAR_CASCADE_EYE)
        detected_eyes = eyes.detectMultiScale(img, 1.3, 5)
        eye_contact = True
        eye_box_dims = []

        for (x, y, w, h) in detected_eyes:
            eye_box_dims.append((w, h))
            if self.is_demo:
                cv2.rectangle(img, (x,y), (x + w, y + h), BLUE ,1)
            eye_img = img[y : y + h, x : x + w]
            circles = self.detect_pupils(eye_img, (w + h) / 2)
            if circles is not None:

                # get circle shortest distance away from centre of bounding box, which is (hopefully) the eyeball
                pupil = min(circles[0], key=lambda c : (c[0] - w / 2) * (c[0] - w / 2) + abs(c[1] - h / 2) *(c[1] - h / 2))

                if self.is_demo:
                    cv2.circle(img, (x + int(pupil[0]), y + int(pupil[1])), int(pupil[2]), RED, 3, cv2.LINE_AA)
                
                # check if eye is looking away, based on the position of the eyeball in the eye's bounding box
                if not self.is_looking_forward(w, h, pupil[0], pupil[1]):
                    if DEBUG:
                        print ('Looking away')
                    eye_contact = False

        # can't find eyes...
        if len(eye_box_dims) < 2:
            if DEBUG:
                print ('Cannot detect eyeballs')
            eye_contact = False

        # if looking away, bounding box size for two eyes will be very different sizes
        elif not self.is_facing_forward(eye_box_dims):
            eye_contact = False

        if self.is_demo:
            if eye_contact:
                cv2.putText(img, 'YES', (int(self.img_width * 0.2), int(self.img_height * 0.2)), cv2.FONT_HERSHEY_SIMPLEX, 4, GREEN, cv2.LINE_AA)
            else:
                cv2.putText(img, ' NO', (int(self.img_width * 0.2), int(self.img_height * 0.2)), cv2.FONT_HERSHEY_SIMPLEX, 4, RED, cv2.LINE_AA)

        if eye_contact:
            self.stats.inc_eye_contact_frames()


    def pre_process(self, img):
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.medianBlur(img, 5)
        windowClose = np.ones((5,5), np.uint8)
        windowOpen  = np.ones((3,3), np.uint8)
        windowErode = np.ones((3,3), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, windowClose)
        img = cv2.morphologyEx(img, cv2.MORPH_ERODE, windowErode)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, windowOpen)
        return img

    def detect_pupils(self, img, s):
        if len(img.shape) == 3:
            img = self.pre_process(img[:,:,0])
        new_circ_size = (STANDARD_EYE_CIRCLE_SIZE * s) / STANDARD_BOUND_BOX_SIZE
        return cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, int(img.shape[1]/3),
                                200,100,new_circ_size, new_circ_size)

    def is_looking_forward(self, w, h, x_pupil, y_pupil):
        revised_tolerance_x = PUPIL_MOVEMENT_TOLERANCE_X *          \
                                STANDARD_BOUND_BOX_SIZE / ((w+h)/2)
        revised_tolerance_y = PUPIL_MOVEMENT_TOLERANCE_Y *          \
                                STANDARD_BOUND_BOX_SIZE / ((w+h)/2)
        x_diff = abs(w - x_pupil)
        y_diff = abs(h - y_pupil)
        return (x_diff < w * revised_tolerance_x) or (y_diff < h * revised_tolerance_y)

    def is_facing_forward(self, eye_box_dims):
        if len(eye_box_dims) >= 2:
            revised_eye_diff_tolerance = \
                STANDARD_EYE_DIFF_TOLERANCE * \
                STANDARD_BOUND_BOX_SIZE / ((eye_box_dims[0][0] + eye_box_dims[1][0]) / 2)
            if abs(eye_box_dims[0][0] - eye_box_dims[1][0]) > revised_eye_diff_tolerance \
            or abs(eye_box_dims[0][1] - eye_box_dims[1][1]) > revised_eye_diff_tolerance:
                if DEBUG:
                    print('Head turning away')
                eye_contact = False
        return True

    ######################################################
    # Functions for processing emotions
    ######################################################

    def launch_emo_threads(self):
        for i in range (NUM_EMO_THREADS):
            new_thread = EmotionsThread(i, self.stats, self.work_queue)
            new_thread.start()
            self.emo_threads.append(new_thread)

    def crop_face(self, img):
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(HAAR_CASCADE_FRONTAL_FACE)

        faces = face_cascade.detectMultiScale(img, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        if len(faces) > 0:
            max_face = max(faces, key=lambda x : x[2] + x[3])
            x, y, w, h = max_face
            return img, img[y : y + h, x : x + w]
        else:
            return img, None

    def process_emotions(self, img, face_img):
        fer_dict = indicoio.fer(face_img)
        max_emotion = max(FACIAL_EMOTIONS, key=lambda x : fer_dict[x])
        self.stats.inc_emotion(max_emotion)
        cv2.putText(img, max_emotion, (int(self.img_width * 0.2), int(self.img_height * 0.2)), cv2.FONT_HERSHEY_SIMPLEX, 4, RED, cv2.LINE_AA)
        return img

    ######################################################
    # Functions for Google Cloud speech-to-text
    ######################################################

    def launch_gcloud_threads(self):
        for i in range (NUM_GCLOUD_THREADS):
            new_thread = GCloudThread(i, self.stats)
            new_thread.start()
            self.gcloud_threads.append(new_thread)

    def get_stats(self):
        return self.stats
