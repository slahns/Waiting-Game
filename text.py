import pygame
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
vcrmono = os.path.join(script_dir, 'assets', 'VCR_OSD_MONO_1.001.ttf')
font = pygame.font.Font(vcrmono, 48)
file = os.path.join(script_dir, 'dialogue.txt')

