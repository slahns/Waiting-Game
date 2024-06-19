import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
webcam_exists = False

# check if the webcam exists
if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

webcam_exists = True

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

face_detected = False
eyes_detected = False

eyes_not_detected_start_time = None
eyes_not_detected_duration = 2

face_not_detected_start_time = None
face_not_detected_duration = 2

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        face_detected = True
        face_not_detected_start_time = None  # reset the timer if face is detected
    else:
        if face_not_detected_start_time is None:
            face_not_detected_start_time = time.time()  # start the timer
        face_detected = False

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (225, 0, 0), 5)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]  # reference to og frame so we can find eyes on the face on roi_gray
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)

        if len(eyes) > 0:
            eyes_detected = True
            eyes_not_detected_start_time = None  # reset the timer if eyes are detected
        else:
            if eyes_not_detected_start_time is None:
                eyes_not_detected_start_time = time.time()  # start the timer
            eyes_detected = False

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (225, 0, 0), 5)

    if face_detected:
        print("Face detected")
        if eyes_detected:
            print("Eyes detected")
        else:
            print("Eyes not detected")
            if eyes_not_detected_start_time:
                elapsed_time_eyes = time.time() - eyes_not_detected_start_time
                if elapsed_time_eyes >= eyes_not_detected_duration:
                    print(f"Eyes have not been detected for {eyes_not_detected_duration} seconds")
    else:
        print("No face detected")
        if face_not_detected_start_time:
            elapsed_time_face = time.time() - face_not_detected_start_time
            if elapsed_time_face >= face_not_detected_duration:
                print(f"Face has not been detected for {face_not_detected_duration} seconds")

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
