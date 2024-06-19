from facial_recognition import check_webcam, facial_recognition, watching_event
from zimblort import Zimblort
import threading
import pygame
import spritesheet
import cv2
import numpy as np

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
sprites = pygame.sprite.Group()
sprite_sheet_image = pygame.image.load('assets/doux.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
animation_steps = [4, 6, 3, 4]

if check_webcam():
    print("Webcam confirmed to exist")
    cap = cv2.VideoCapture(0)
    frame_holder = {"frame": None, "lock": threading.Lock()}
    threading.Thread(target=facial_recognition, args=(cap, frame_holder), daemon=True).start()
else:
    print("Error: Could not open webcam")

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