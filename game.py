from facial_recognition import check_webcam, facial_recognition
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
ROPE_COLOR = (139, 69, 19)  # brown rope

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
animation_steps = [4, 6, 3, 4, 6]

no_webcam_img = pygame.image.load(os.path.join(script_dir, 'assets', 'no_webcam.png'))

finish_flag = pygame.image.load(os.path.join(script_dir, 'assets', 'finish_flag.png'))

ground_tile_1 =  pygame.image.load(os.path.join(script_dir, 'assets', 'ground_tile.png'))
ground_rect_1 = ground_tile_1.get_rect()
ground_rect_1.bottomleft = (0, 600)

ground_tile_2 =  pygame.image.load(os.path.join(script_dir, 'assets', 'ground_tile.png'))
ground_rect_2 = ground_tile_2.get_rect()
ground_rect_2.bottomright = (800, 600)

ground_tile_3 =  pygame.image.load(os.path.join(script_dir, 'assets', 'ground_tile.png'))
ground_rect_3 = ground_tile_2.get_rect()
ground_rect_3.bottomright = (3000, 600)

ground_tiles = [ground_rect_1, ground_rect_2, ground_rect_3]

bg_images = []
for i in range(1,6):
    bg_image = pygame.image.load(os.path.join(script_dir, 'assets', "Parallax", f"plx-{i}.png")).convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  
    bg_images.append(bg_image)


bg_speeds = [0.1, 0.11, 0.11, 0.12, 0.13]
bg_positions = [0, 0, 0, 0, 0]

def draw_bg(is_moving, offset_x):
    for idx, bg_image in enumerate(bg_images):
        if is_moving:
            bg_positions[idx] -= bg_speeds[idx]
            if bg_positions[idx] <= -SCREEN_WIDTH:
                bg_positions[idx] += SCREEN_WIDTH
        win.blit(bg_image, (bg_positions[idx] - offset_x * bg_speeds[idx], 0))
        win.blit(bg_image, (bg_positions[idx] + SCREEN_WIDTH - offset_x * bg_speeds[idx], 0))

def display_no_webcam_message():
    win.fill(BLACK)
    win.blit(no_webcam_img, (0, 0))
    pygame.display.flip()

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
        pygame.time.wait(1000)  

print("Webcam confirmed to exist")
cap = cv2.VideoCapture(0)
frame_holder = {"frame": None, "lock": threading.Lock()}
threading.Thread(target=facial_recognition, args=(cap, frame_holder), daemon=True).start()

zimblort = Zimblort(0, 387, sprite_sheet, animation_steps, ground_tiles)

def convert_cv2_to_pygame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    return frame

def resize_frame(frame, width, height):
    return cv2.resize(frame, (width, height))

def draw(win, offset_x, offset_y):
    for ground_tile in ground_tiles:
        win.blit(ground_tile_1, (ground_tile.left - offset_x, ground_tile.top - offset_y))

    win.blit(finish_flag, (ground_tiles[1].right - offset_x, ground_tiles[1].top - offset_y))
    pygame.draw.line(win, ROPE_COLOR, (ground_tiles[0].right - offset_x, ground_tiles[0].top - offset_y), (ground_tiles[1].left - offset_x, ground_tiles[1].top - offset_y), 5)
    pygame.draw.line(win, ROPE_COLOR, (ground_tiles[1].right - offset_x, ground_tiles[1].top - offset_y), (ground_tiles[2].left - offset_x, ground_tiles[2].top - offset_y), 5)

    zimblort.draw(win, (offset_x, offset_y))

def show_start_screen():
    start_screen = True
    font = pygame.font.SysFont(None, 48)
    text = font.render("Press any button to begin", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start_screen = False

        win.fill((12, 24, 36))
        draw_bg(False, 0) 
        draw(win, 0, 0)  

        win.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)

show_start_screen()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    zimblort.update()

    offset_x = zimblort.x - SCREEN_WIDTH // 2
    offset_x = max(0, min(offset_x, ground_tiles[-1].right - SCREEN_WIDTH))
    
    offset_y = zimblort.y - SCREEN_HEIGHT // 2
    offset_y = max(0, min(offset_y, ground_tiles[0].top - SCREEN_HEIGHT))

    win.fill((12, 24, 36))

    is_moving = zimblort.action == 1 
    draw_bg(is_moving, offset_x)
    draw(win, offset_x, offset_y)

    with frame_holder["lock"]:
        frame = frame_holder["frame"]
    if frame is not None:
        resized_frame = resize_frame(frame, 200, 200)
        frame_surface = convert_cv2_to_pygame(resized_frame)
        frame_rect = frame_surface.get_rect(topleft=(25, 25))  
        win.blit(frame_surface, frame_rect)
        pygame.draw.rect(win, (27, 65, 153), frame_rect, 5)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()