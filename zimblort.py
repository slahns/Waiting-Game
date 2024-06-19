from facial_recognition import watching_event
import pygame

class Zimblort:

    def __init__(self, x, y, sprite_sheet, animation_steps, animation_cooldown=50):

        #zimblort object 
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect((self.x, self.y, 32, 32))
        self.color = (250, 120, 60)
        self.velX = 0
        self.velY = 0
        self.speed = 0.3

        #sprite and animation
        self.sprite_sheet = sprite_sheet
        self.animation_steps = animation_steps
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.animation_cooldown = animation_cooldown
        self.action = 0  # idle action
        self.frame = 0
        self.last_update = pygame.time.get_ticks()

    def draw(self, win):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0

        image = self.animation_list[self.action][self.frame]
        win.blit(image, (self.x, self.y))

    def update(self):
        self.velX = 0
        self.velY = 0
        if watching_event.is_set():
            new_action = 1 
        else:
            new_action = 0  

        if new_action != self.action:
            self.action = new_action
            self.frame = 0

        if self.action == 1:
            self.velX = self.speed

        self.x += self.velX
        self.rect = pygame.Rect(int(self.x), int(self.y), 32, 32)

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        step_counter = 0
        for anim in animation_steps:
            temp_img_list = []
            for _ in range(anim):
                temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 3, (0, 0, 0)))
                step_counter += 1
            animation_list.append(temp_img_list)
        return animation_list