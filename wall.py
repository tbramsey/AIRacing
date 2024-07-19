import pygame

class Wall:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)