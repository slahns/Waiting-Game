from facial_recognition import check_webcam, facial_recognition, watching_event
from zimblort import Zimblort
import threading
import pygame
import spritesheet
import cv2
import numpy as np
import os

TITLE = "The Waiting Game"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)

pygame.init()
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
script_dir = os.path.dirname(os.path.abspath(__file__))
sprite_sheet_path = os.path.join(script_dir, 'assets', 'doux.png')
sprite_sheet_image = pygame.image.load(sprite_sheet_path).convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
animation_steps = [4, 6, 3, 4]

# Load the "no webcam" image
no_webcam_img = pygame.image.load(os.path.join(script_dir, 'assets', 'no_webcam.png'))

# Function to display a message or image
def display_no_webcam_message():
    win.fill(BLACK)
    win.blit(no_webcam_img, (0, 0))
    pygame.display.flip()

# Loop to check for webcam connection
webcam_connected = False
while not webcam_connected:
    if check_webcam():
        webcam_connected = True
    else:
        display_no_webcam_message()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.time.wait(1000)  # Wait for 1 second before checking again

print("Webcam confirmed to exist")
cap = cv2.VideoCapture(0)
frame_holder = {"frame": None, "lock": threading.Lock()}
threading.Thread(target=facial_recognition, args=(cap, frame_holder), daemon=True).start()

# zimblort initialization
zimblort = Zimblort(100, 100, sprite_sheet, animation_steps)

def convert_cv2_to_pygame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    return frame

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update and draw zimblort
    win.fill((12, 24, 36))  # Draw background
    zimblort.update()
    zimblort.draw(win)

    with frame_holder["lock"]:
        frame = frame_holder["frame"]
    if frame is not None:
        resized_frame = resize_frame(frame, 320, 240)
        frame_surface = convert_cv2_to_pygame(resized_frame)
        win.blit(frame_surface, (0, 0))

    pygame.display.flip()
    clock.tick(120)


pygame.quit()