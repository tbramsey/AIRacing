import pygame
import math

class Car:
    def __init__(self, x, y, img, height, width, walls, color):
        self.x = x - width / 2
        self.y = y - height / 2
        self.height = height
        self.width = width
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.blit(img, (0, 0))
        self.angle = 0
        self.speed = 0
        self.sensor_length = 100
        self.sensors = []
        self.sensor_distances = [1.0] * 18
        self.walls = walls

    def draw(self, window):
        self.rect.topleft = (int(self.x), int(self.y))
        rotated = pygame.transform.rotate(self.surface, self.angle)
        surface_rect = self.surface.get_rect(topleft=self.rect.topleft)
        new_rect = rotated.get_rect(center=surface_rect.center)
        window.blit(rotated, new_rect.topleft)

        for index, angle in enumerate(range(0, 180, 10)):
            sensor_angle = math.radians(self.angle + angle)
            for size in range(0, 400, 10):
                sensor_end_x = self.x + self.width / 2 + size * math.cos(sensor_angle)
                sensor_end_y = self.y + self.height / 2 - size * math.sin(sensor_angle)
                pygame.draw.line(window, (255, 0, 0), (self.x + self.width / 2, self.y + self.height / 2), (sensor_end_x, sensor_end_y), 2)
                if self.check_sensors(sensor_end_x, sensor_end_y):
                    self.sensor_distances[index] = size/400
                    break

    def check_sensors(self, sensor_end_x, sensor_end_y):
        sensor_rect = pygame.Rect(sensor_end_x, sensor_end_y, 1, 1)  # Adjust this size as needed
        for wall in self.walls:
            if sensor_rect.colliderect(wall.rect):
                return True
        return False
