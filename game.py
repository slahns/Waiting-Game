import threading
from facial_recognition import check_webcam, facial_recognition, watching_event
import pygame

TITLE = "The Waiting Game"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

if check_webcam():
    print("Webcam confirmed to exist")
    threading.Thread(target=facial_recognition, daemon=True).start()
else:
    print("Error: Could not open webcam")

class Zimblort:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect((self.x, self.y, 32, 32))
        self.color = (250, 120, 60)
        self.velX = 0
        self.velY = 0
        self.speed = 0.3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        self.velX = 0
        self.velY = 0
        if watching_event.is_set():
            self.velX = self.speed

        self.x += self.velX

        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)

# zimblort initialization
zimblort = Zimblort(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill((12, 24, 36))  
    zimblort.draw(win)

    zimblort.update()
    pygame.display.flip()

    clock.tick(120)

pygame.quit()