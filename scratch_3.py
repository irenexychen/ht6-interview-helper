import cv2

import indicoio

indicoio.config.api_key = "fc13c0c79bfa4d02be04e534f6b178bd"

cam = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    '/usr/local/Cellar/opencv/3.4.2/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv/3.4.2/share/OpenCV/haarcascades/haarcascade_eye.xml')

cv2.namedWindow("test")

pictureCount = 0
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


    #
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, "Percent looking forward: "+str(text), (x, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        ew1 = 1
        ew2=1
        eh1=1
        eh2=1
        count = 0
        for (ex, ey, ew, eh) in eyes:
            if count == 0:
                ew1=ew
                eh1 = eh
            elif count == 1:
                ew2 = ew
                eh2 = eh
            else: break
            count = count+1

        if (2*abs(ew1-ew2)/(ew1+ew2) > 0.2)|(2*abs(eh1-eh2)/(eh1+eh2) > 0.2):
            print("qwertyuiop")
            forwardCount = forwardCount +1

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    #
    cv2.imshow("test", frame)

    emotions = indicoio.fer(frame)
    print(emotions)


    cv2.waitKey(100)
    pictureCount = pictureCount +1
    text = ((pictureCount-forwardCount)/pictureCount)
    print(text)



cam.release()

cv2.destroyAllWindows()