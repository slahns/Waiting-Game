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
sprite_sheet_image = pygame.image.load('Waiting-Game/assets/doux.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

animation_list = []
animation_steps = [4, 6, 3, 4]
action = 1
last_update = pygame.time.get_ticks()
animation_cooldown = 50 #ms
frame = 0
step_counter = 0

for anim in animation_steps:
    temp_img_list = []
    for _ in range(anim):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 3, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)



if check_webcam():
    print("Webcam confirmed to exist")
    threading.Thread(target=facial_recognition, daemon=True).start()
else:
    print("Error: Could not open webcam")

# zimblort initialization
zimblort = Zimblort(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

run = True
while run:

    # bg
    win.fill((12, 24, 36))  

    zimblort.draw(win)
    zimblort.update()

    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    screen.blit(animation_list[action][frame], (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if watching_event:
            action = 0
        else:
            action = 1

    pygame.display.flip()
    clock.tick(120)

pygame.quit()