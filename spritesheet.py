import pygame

class SpriteSheet:
    def __init__(self, image):
        self.image = image

    def get_image(self, frame, width, height, scale, color_key):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.image, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color_key)
        return image