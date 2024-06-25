import numpy as np
import cv2
import time
import threading
import global_vars

watching_event = threading.Event()

def check_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False
    cap.release()
    return True

def facial_recognition(cap, frame_holder):

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    face_detected = False
    eyes_detected = False

    elapsed_time_eyes = 0.0
    elapsed_time_face = 0.0

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
            roi_color = frame[y:y+h, x:x+w] 
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)

            if len(eyes) > 0: # not everyone has two eyes, so checking if any eyes are present
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
            global_vars.falling = False
            
            if eyes_detected:
                print("Eyes detected")
                global_vars.falling = False
                watching_event.set()
            else:
                print("Eyes not detected")
                if eyes_not_detected_start_time:
                    if global_vars.on_ground == False:
                        elapsed_time_eyes = time.time() - eyes_not_detected_start_time
                    if elapsed_time_eyes >= eyes_not_detected_duration:
                        print(f"Eyes have not been detected for {elapsed_time_eyes} seconds")
                        watching_event.clear()
                        global_vars.falling = True
                        if elapsed_time_eyes >= 5:
                            print(f"Zimblort fell: Eyes have not been detected for {elapsed_time_eyes} seconds")
                            watching_event.clear()
                            global_vars.fell = True
                else:
                    global_vars.falling = False
        else:
            print("No face detected")
            if face_not_detected_start_time:
                if global_vars.on_ground == False:
                    elapsed_time_face = time.time() - face_not_detected_start_time
                if elapsed_time_face >= face_not_detected_duration:
                    print(f"Face has not been detected for {elapsed_time_face} seconds")
                    watching_event.clear()
                    global_vars.falling = True
                    if elapsed_time_face >= 5:
                        print(f"Zimblort fell: Eyes have not been detected for {elapsed_time_face} seconds")
                        watching_event.clear()
                        global_vars.fell = True
            else:
                global_vars.falling = False

        #cv2.imshow('frame', frame)

        with frame_holder["lock"]:
            frame_holder["frame"] = frame.copy()

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    
