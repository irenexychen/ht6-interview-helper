import cv2

import indicoio

indicoio.config.api_key = "fc13c0c79bfa4d02be04e534f6b178bd"

cam = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    '/usr/local/Cellar/opencv/3.4.2/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv/3.4.2/share/OpenCV/haarcascades/haarcascade_eye.xml')

cv2.namedWindow("test")

pictureCount = 1
forwardCount = 0
text=0
while True:
    ret, frame = cam.read()

    if not ret:
        break
    k = cv2.waitKey(1)
    if k % 256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    emotions = indicoio.fer(frame)
    cv2.putText(frame, "Angry:"+str(emotions["Angry"]), (1, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, "Sad:" + str(emotions["Sad"]), (1, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 127, 127), 2)
    cv2.putText(frame, "Neutral:" + str(emotions["Neutral"]), (1, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(frame, "Surprise:" + str(emotions["Surprise"]), (1, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (127, 127, 255), 2)
    cv2.putText(frame, "Fear:" + str(emotions["Fear"]), (1, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(frame, "Happy:" + str(emotions["Happy"]), (1, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (127, 0, 127), 2)


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)



    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    try:
        x, y, w, h = faces[0]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, "Percent looking forward: "+str(text), (x, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        try:
            ex1, ey1, ew1, eh1 = eyes[0]
            ex2, ey2, ew2, eh2 = eyes[1]

            diff1 = 2 * abs(ew1 - ew2) / (ew1 + ew2)
            diff2 = 2 * abs(eh1 - eh2) / (eh1 + eh2)
            if (diff1<0.7)&(diff2<0.7):
                pictureCount = pictureCount + 1
                cv2.rectangle(roi_color, (ex1, ey1), (ex1 + ew1, ey1 + eh1), (0, 255, 0), 2)
                cv2.rectangle(roi_color, (ex2, ey2), (ex2 + ew2, ey2 + eh2), (0, 255, 0), 2)
                if (diff1 > 0.15)  | (diff2 > 0.15):
                    print("qwertyuiop")
                    forwardCount = forwardCount + 1
        except IndexError:
            pass

    except IndexError:
        pass

    cv2.imshow("test", frame)

    emotions = indicoio.fer(frame)
    print(emotions)


    cv2.waitKey(75)

    text = ((pictureCount-forwardCount)/pictureCount)
    print(text)



cam.release()

cv2.destroyAllWindows()