from facial_recognition import check_webcam, facial_recognition, watching_event
from zimblort import Zimblort
import threading
import pygame
import spritesheet

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
    threading.Thread(target=facial_recognition, daemon=True).start()
else:
    print("Error: Could not open webcam")

# zimblort initialization
zimblort = Zimblort(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update and draw Zimblort
    win.fill((12, 24, 36))  # Draw background
    zimblort.update()
    zimblort.draw(win)

    pygame.display.flip()
    clock.tick(120)


pygame.quit()