from car import Car
from wall import Wall
import pygame, math
import random
pygame.init()


class GameInformation:
    def __init__(self, laps):
        self.laps = laps

class Checkpoint:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height) 
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

class Game:
    """
    To use this class simply initialize and instance and call the .loop() method
    inside of a pygame event loop (i.e while loop). Inside of your event loop
    you can call the .draw() and .move_paddle() methods according to your use case.
    Use the information returned from .loop() to determine when to end the game by calling
    .reset().
    """
    SCORE_FONT = pygame.font.SysFont("comicsans", 50)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GREEN = (0, 255, 0)
    
    clock = pygame.time.Clock()
    

    def __init__(self, window, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0

        #track 1
        """
        self.walls = [
            Wall(0, 0, 20, 740, self.RED),
            Wall(0, 0, 1400, 20, self.RED),
            Wall(1380, 20, 20, 730, self.RED),
            Wall(0, 730, 1400, 20, self.RED),
            Wall(200, 200, 20, 350, self.RED),
            Wall(200, 200, 1000, 20, self.RED),
            Wall(1180, 200, 20, 350, self.RED),
            Wall(200, 530, 1000, 20, self.RED),
        ]
        self.checkpoints = [
            Checkpoint(20, 220, 180, 10, self.GREEN),
            Checkpoint(400, 20, 10, 180, self.GREEN),
            Checkpoint(700, 20, 10, 180, self.GREEN),
            Checkpoint(1000, 20, 10, 180, self.GREEN),
            Checkpoint(1200, 220, 180, 10, self.GREEN),
            Checkpoint(1200, 370, 180, 10, self.GREEN),
            Checkpoint(1200, 520, 180, 10, self.GREEN),
            Checkpoint(1000, 550, 10, 180, self.GREEN),
            Checkpoint(700, 550, 10, 180, self.GREEN),
            Checkpoint(400, 550, 10, 180, self.GREEN),
            Checkpoint(20, 520, 180, 10, self.GREEN),
            Checkpoint(20, 370, 180, 10, self.GREEN),
        ]
        
        #track 2
        """
        self.walls = [
            Wall(0, 0, 20, 740, self.RED),
            Wall(0, 0, 1400, 20, self.RED),
            Wall(1380, 20, 20, 730, self.RED),
            Wall(0, 730, 1400, 20, self.RED),
            Wall(200, 200, 20, 400, self.RED),
            Wall(400, 0, 20, 400, self.RED),
            Wall(600, 200, 20, 400, self.RED),
            Wall(800, 0, 20, 400, self.RED),
            Wall(1000, 200, 20, 400, self.RED),
            Wall(1000, 200, 200, 20, self.RED),
            Wall(1200, 400, 200, 20, self.RED),
            Wall(200, 600, 820, 20, self.RED),
        ]
        self.checkpoints = [
            Checkpoint(20, 200, 180, 10, self.GREEN),
            Checkpoint(205, 20, 10, 180, self.GREEN),
            Checkpoint(220, 200, 180, 10, self.GREEN),
            Checkpoint(220, 390, 180, 10, self.GREEN),
            Checkpoint(405, 400, 10, 200, self.GREEN),
            Checkpoint(420, 390, 180, 10, self.GREEN),
            Checkpoint(420, 200, 180, 10, self.GREEN),
            Checkpoint(605, 20, 10, 180, self.GREEN), 
            Checkpoint(620, 200, 180, 10, self.GREEN),
            Checkpoint(620, 390, 180, 10, self.GREEN),
            Checkpoint(805, 400, 10, 200, self.GREEN),
            Checkpoint(820, 390, 180, 10, self.GREEN),
            Checkpoint(820, 200, 180, 10, self.GREEN), 
            Checkpoint(1005, 20, 10, 180, self.GREEN),
            Checkpoint(1200, 205, 180, 10, self.GREEN), 
            Checkpoint(1020, 405, 180, 10, self.GREEN), 
            #Checkpoint(1200, 605, 180, 10, self.GREEN), 
            Checkpoint(1000, 620, 10, 110, self.GREEN), 
            Checkpoint(695, 620, 10, 110, self.GREEN), 
            Checkpoint(200, 620, 10, 110, self.GREEN), 
            Checkpoint(20, 605, 180, 10, self.GREEN), 
            Checkpoint(20, 400, 180, 10, self.GREEN), 
        ]
        
        img = pygame.image.load("1.png")
        img = pygame.transform.scale(img, (20, 43))
        self.car = Car(100, 300, img, 43, 20, self.walls, self.WHITE)

        self.laps = 0
        self.window = window
        
    
    def draw_score(self):
        score_text = self.SCORE_FONT.render(f"{self.laps}", 1, self.BLACK)
        self.window.blit(score_text, ((self.window_width // 8) - score_text.get_width() // 2, 20))

    def draw_time(self, time):
        time_text = self.SCORE_FONT.render(f"{time:.2f}", 1, self.BLACK)  # Format time to 2 decimal places
        self.window.blit(time_text, ((self.window_width // 8) * 7 - time_text.get_width() // 2, 20))


    def move_car(self, up=False, down=False, right=False, left=False):
        # Constants for acceleration and deceleration
        acceleration = 0.2
        max_speed = 5
        friction = 0.98  # Higher value for more momentum
        
        # Adjust car speed based on input
        if up:
            self.car.speed += acceleration
        if down:
            self.car.speed -= acceleration

        # Cap the speed to max_speed
        if self.car.speed > max_speed:
            self.car.speed = max_speed
        if self.car.speed < -max_speed:
            self.car.speed = -max_speed

        # Apply friction to simulate momentum
        self.car.speed *= friction

        # Adjust car angle based on speed and input
        if left:
            self.car.angle += self.car.speed / 2
        if right:
            self.car.angle -= self.car.speed / 2

        # Update car position based on speed and angle
        self.car.x -= self.car.speed * math.sin(math.radians(self.car.angle))
        self.car.y -= self.car.speed * math.cos(math.radians(-self.car.angle))

        # Clear the screen and redraw everything
        self.window.fill(self.WHITE)
        self.draw_score()
        self.draw_time(self.elapsed_time)
        self.car.draw(self.window)

        for wall in self.walls:
            wall.draw(self.window)

        for checkpoint in self.checkpoints:
            checkpoint.draw(self.window)

        pygame.display.flip()
        self.clock.tick(60)

        return True


    def loop(self):
        """
        Executes a single game loop.

        :returns: GameInformation instance stating score 
                  and hits of each paddle.
        """

        #self._handle_collision()
        self.current_time = pygame.time.get_ticks()
        self.elapsed_time = (self.current_time - self.start_time) / 1000
        game_info = GameInformation(
            self.laps)

        return game_info

    def reset(self):
        """Resets the entire game."""
        self.laps = 0

    def check_collisions(self):
        car_rect = self.car.surface.get_rect(topleft=(self.car.x, self.car.y))
        for wall in self.walls:
            if car_rect.colliderect(wall.rect):
                #self.reset()
                return True
        return False

    def check_checkpoints(self):
        car_rect = self.car.surface.get_rect(topleft=(self.car.x, self.car.y))
        for index, checkpoint in enumerate(self.checkpoints):
            if self.laps % 21 == index:
                if car_rect.colliderect(checkpoint.rect):
                    self.laps += 1
            
