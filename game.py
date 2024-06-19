from facial_recognition import check_webcam, facial_recognition

if check_webcam():
    print("Webcam confirmed to exist")
    facial_recognition()
else:
    print("Error: Could not open webcam")