import sys
from facial_recognition import facial_recognition, stop_event
from zimblort import Zimblort
import global_vars
import threading
import pygame
import spritesheet
import cv2
import numpy as np
import os
import random

TITLE = "The Waiting Game"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
ROPE_COLOR = (231, 162, 124) 


pygame.init()
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)

win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS # if PyInstaller is packaging the program
else:
    base_path = os.path.dirname(os.path.abspath(__file__)) # if program is running normally

sprite_sheet_path = os.path.join(base_path, 'assets', 'doux.png')
sprite_sheet_image = pygame.image.load(sprite_sheet_path).convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
animation_steps = [4, 6, 3, 4, 6]

vcrmono = os.path.join(base_path, 'assets', 'VCR_OSD_MONO_1.001.ttf')
victory_theme = os.path.join(base_path, 'assets', 'TipTopTomCat Your Heart Your Soul V2.mp3')
victory_sfx = pygame.mixer.Sound(victory_theme)

victory_img = pygame.image.load(os.path.join(base_path, 'assets', 'you_won.png'))
icon_img = pygame.image.load(os.path.join(base_path, 'assets', 'zimblort_icon.png'))

pygame.display.set_icon(icon_img) 

ground_tile_1 = pygame.image.load(os.path.join(base_path, 'assets', 'ground_tile.png'))
ground_rect_1 = ground_tile_1.get_rect()
ground_rect_1.bottomleft = (0, 600)

ground_tile_2 = pygame.image.load(os.path.join(base_path, 'assets', 'ground_tile.png'))
ground_rect_2 = ground_tile_2.get_rect()
ground_rect_2.bottomright = (800, 600)

ground_tile_3 = pygame.image.load(os.path.join(base_path, 'assets', 'ground_tile.png'))
ground_rect_3 = ground_tile_2.get_rect()
ground_rect_3.bottomright = (48000, 600)

ground_tiles = [ground_rect_1, ground_rect_2, ground_rect_3]

bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(os.path.join(base_path, 'assets', "Parallax", f"plx-{i}.png")).convert_alpha()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_images.append(bg_image)

bg_speeds = [0.01, 0.011, 0.011, 0.012, 0.013]
bg_positions = [0, 0, 0, 0, 0]

def draw_bg(is_moving, offset_x):
    for index, bg_image in enumerate(bg_images):
        if is_moving: # if background should be moving
            bg_positions[index] -= bg_speeds[index] # move bg left
            if bg_positions[index] <= -SCREEN_WIDTH: # supposed to reset bg before player can see the end of it off screen, but doesnt work :(
                bg_positions[index] = 0

        x_position = bg_positions[index] - offset_x * bg_speeds[index]
        win.blit(bg_image, (x_position, 0))
        win.blit(bg_image, (x_position + SCREEN_WIDTH, 0))


def display_victory_message():
    win.fill(BLACK)
    win.blit(victory_img, (0, 0))
    pygame.display.flip()


cap = cv2.VideoCapture(0)
frame_holder = {"frame": None, "lock": threading.Lock()}
global facial_recognition_thread
facial_recognition_thread = threading.Thread(target=facial_recognition, args=(cap, frame_holder), daemon=True)
facial_recognition_thread.start()

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

    pygame.draw.line(win, ROPE_COLOR, (ground_tiles[0].right - offset_x, ground_tiles[0].top - offset_y),
                     (ground_tiles[1].left - offset_x, ground_tiles[1].top - offset_y), 5)
    pygame.draw.line(win, ROPE_COLOR, (ground_tiles[1].right - offset_x, ground_tiles[1].top - offset_y),
                     (ground_tiles[2].left - offset_x, ground_tiles[2].top - offset_y), 5)

    zimblort.draw(win, (offset_x, offset_y))

def reset_game():
    global facial_recognition_thread, cap
    global_vars.falling = False
    global_vars.fell = False
    global_vars.on_ground = True
    global_vars.game_over = False
    zimblort.x = 0
    zimblort.y = 387
    zimblort.velX = 0  
    zimblort.velY = 0  
    zimblort.angle = 0  
    zimblort.spin_speed = random.uniform(-10, 10) 
    zimblort.action = 0

    stop_event.set()  # signal the current facial recognition thread to stop
    facial_recognition_thread.join()  # wait for the thread to finish
    stop_event.clear()  # clear the stop event for the new thread

    cap.release()  
    cap = cv2.VideoCapture(0)  
    facial_recognition_thread = threading.Thread(target=facial_recognition, args=(cap, frame_holder), daemon=True)
    facial_recognition_thread.start()

    global_vars.win = False


def show_start_screen():
    start_screen = True
    font = pygame.font.Font(vcrmono, 48)
    text = font.render("Press any button to begin", True, (87, 118, 178))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    while start_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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

    if global_vars.game_over:
        current_time = pygame.time.get_ticks()
        if current_time - global_vars.game_over_time >= 3500:
            reset_game()
            show_start_screen()
    
    if global_vars.win:
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

if global_vars.win:
        victory_sfx.play()
        end_loop = True
        display_victory_message()
        while end_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    end_loop = False

pygame.quit()