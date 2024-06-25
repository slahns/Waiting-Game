import facial_recognition
import pygame
import global_vars
import random

class Zimblort:

    def __init__(self, x, y, sprite_sheet, animation_steps, ground_tiles, animation_cooldown=50):
        self.x = int(x)
        self.y = int(y)
        self.rect = pygame.Rect((self.x, self.y, 64, 65))
        self.color = (250, 120, 60)
        self.velX = 0
        self.velY = 0
        self.speed = 0.3
        self.fall_speed = 2
        self.gravity = 0.05  
        self.spin_speed = random.uniform(-10, 10)  
        self.angle = 0  
        self.sprite_sheet = sprite_sheet
        self.animation_steps = animation_steps
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.animation_cooldown = animation_cooldown
        self.action = 0  
        self.frame = 0
        self.ground_tiles = ground_tiles
        self.last_update = pygame.time.get_ticks()

    def draw(self, win, offset):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.frame += 1
            self.last_update = current_time
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0

        image = self.animation_list[self.action][self.frame]

        if self.action == 3: 
            rotated_image = pygame.transform.rotate(image, self.angle).convert_alpha()
            win.blit(rotated_image, (self.x - offset[0], self.y - offset[1]))
        else:
            win.blit(image, (self.x - offset[0], self.y - offset[1]))

        #pygame.draw.rect(win, (255, 0, 0), self.rect, 2)

    def check_ground_collision(self):
        for ground_tile in self.ground_tiles:
            if self.rect.colliderect(ground_tile):
                global_vars.on_ground = True
                return True
        global_vars.on_ground = False
        return False


    def update(self):
        self.velX = 0

        if self.check_ground_collision():
            #global_vars.falling = False
            #global_vars.fell = False
            #self.velY = 0
            #self.angle = 0
            print("on ground")

        if facial_recognition.watching_event.is_set():
            new_action = 1  # moving
        elif global_vars.fell:
            if self.check_ground_collision():
                new_action = 0  # idle
            else:
                new_action = 3  # fell
        else:
            if global_vars.falling:
                if self.check_ground_collision():
                    new_action = 0  # idle
                else:
                    new_action = 2  # falling
            else:
                new_action = 0  # idle

        if new_action != self.action:
            self.action = new_action
            self.frame = 0

        if self.action == 1:  # moving
            self.velX = self.speed
        elif self.action == 3:  # fell
            self.velY += self.gravity  
            self.angle += self.spin_speed  

        self.x += self.velX
        self.y += self.velY
        self.rect = pygame.Rect(int(self.x), int(self.y), 64, 65)


    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        frame_width = sprite_sheet.image.get_width() // 24 
        step_counter = 0
        for anim in animation_steps:
            temp_img_list = []
            for frame_num in range(anim):
                frame = sprite_sheet.get_image(step_counter + frame_num, frame_width, frame_width, 3, (0, 0, 0))
                temp_img_list.append(frame)
            step_counter += anim
            animation_list.append(temp_img_list)
        return animation_list

