import pygame
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
vcrmono = os.path.join(script_dir, 'assets', 'VCR_OSD_MONO_1.001.ttf')
font = pygame.font.Font(vcrmono, 48)
#text = font.render("Press any button to begin", True, (255, 255, 255))
file = os.path.join(script_dir, 'dialogue.txt')

