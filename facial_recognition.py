# facial recognition code derived from Tech with Tim's video "OpenCV Python Tutorial #8 - Face and Eye Detection" https://www.youtube.com/watch?v=mPCZLOVTEc4
import sys
import os
import numpy as np
import cv2
import time
import threading
import global_vars
import pygame

watching_event = threading.Event()
stop_event = threading.Event()

def check_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False
    cap.release()
    return True

def get_cascade_path(filename):
    if getattr(sys, 'frozen', False): # if script is being packaged by PyInstaller
        path = os.path.join(sys._MEIPASS, filename)  # sys._MEIPASS attribute is set to the path of this temporary folder
    else:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename) # if script is not being packaged, files are expected to be in the same directory as the script
    
    return path

def facial_recognition(cap, frame_holder):
    face_cascade_path = get_cascade_path("cv2/data/haarcascades/haarcascade_frontalface_default.xml")

    face_cascade = cv2.CascadeClassifier(face_cascade_path)

    if face_cascade.empty():
        print("Error loading face cascade")

    face_detected = False
    elapsed_time_face = 0.0 # how long the player's face has not been visible
    face_not_detected_start_time = None # state of player's face being visible or not
    face_not_detected_duration = 2 # how long the player can look away before Zimblort falls

    while not stop_event.is_set():
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

        if face_detected and not global_vars.game_over:
            global_vars.falling = False
            watching_event.set() # player is watching and face is visible
        else:
            if face_not_detected_start_time: # player's face has begun to not be visible
                if not global_vars.on_ground:
                    elapsed_time_face = time.time() - face_not_detected_start_time
                if elapsed_time_face >= face_not_detected_duration:
                    watching_event.clear()
                    global_vars.falling = True
                    if elapsed_time_face >= 5:
                        watching_event.clear()
                        global_vars.fell = True
                        global_vars.game_over_time = pygame.time.get_ticks()  
                        global_vars.game_over = True
                        break
            else:
                global_vars.falling = False

        with frame_holder["lock"]:
            frame_holder["frame"] = frame.copy()

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
