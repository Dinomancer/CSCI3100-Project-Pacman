#from Button import Button
import pygame
import pygame.key
class Setting:
    # define position and the keyboard relationship and default volume settings
    def __init__(self):
        self.left = pygame.K_a
        self.right = pygame.K_d
        self.up = pygame.K_w
        self.down = pygame.K_s
        self.vol = 50

    def keyBinding(self, key, binding):
        if key == "left":
            self.left = binding
        elif key == "right":
            self.right = binding
        elif key == "up":
            self.up = binding
        elif key == "down":
            self.down = binding
# allow volume change within a constraint
    def volumeChange(self, volume):
        if (0 <= volume and volume <= 100):
            self.vol = volume


