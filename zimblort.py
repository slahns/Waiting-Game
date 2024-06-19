from facial_recognition import watching_event
import pygame

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