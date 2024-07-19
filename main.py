# https://neat-python.readthedocs.io/en/latest/xor_example.html
from racing import Game
import pygame
import neat
import os
import time
import pickle
import multiprocessing

class RacingGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        #self.window = pygame.display.set_mode((width, height))
        self.car = self.game.car

    def test_drive(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            game_info = self.game.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            keys = pygame.key.get_pressed()
            up = keys[pygame.K_UP]
            down = keys[pygame.K_DOWN]
            left = keys[pygame.K_LEFT]
            right = keys[pygame.K_RIGHT]

            self.game.move_car(up=up, down=down, right=right, left=left)
            if self.game.check_collisions():
                run = False
            self.game.check_checkpoints()
            pygame.display.update()

    def train_ai(self, genome, config):
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()


                sensor_distances = [dist for dist in self.car.sensor_distances]
                
                #print("Sensor distances:", sensor_distances)
                output = net.activate(sensor_distances)
                #print("Output:", output)
                decision = output.index(max(output))
                #print("Decision:", decision)

                #if decision == 0:
                #    pass
                #elif decision == 1:
                #    self.game.move_car(up=True, down=False, right=False, left=False)
                #elif decision == 2:
                #    self.game.move_car(up=False, down=True, right=False, left=False)
                #elif decision == 3:
                #    self.game.move_car(up=False, down=False, right=True, left=False)
                #elif decision == 4:
                #    self.game.move_car(up=False, down=False, right=False, left=True)

                if decision == 0:
                    self.game.move_car(up=True, down=False, right=False, left=False)
                elif decision == 1:
                    self.game.move_car(up=True, down=False, right=True, left=False)
                elif decision == 2:
                    self.game.move_car(up=True, down=False, right=False, left=True)

                
                self.game.loop()
                #self.game.draw_score()
                #self.game.draw_time(elapsed_time)
                #pygame.display.update()
                
                
                self.game.check_checkpoints()
                if self.game.check_collisions()  or self.game.elapsed_time > 20:
                    print("Laps:", self.game.laps, "Collision:", self.game.check_collisions(), "Time:", self.game.elapsed_time)
                    self.calculate_fitness(genome)
                    self.game.laps = 0
                    run = False
            
    def test_ai(self, genome, config):
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()

                sensor_distances = [dist for dist in self.car.sensor_distances]
                output = net.activate(sensor_distances)
                decision = output.index(max(output))

                if decision == 0:
                    self.game.move_car(up=True, down=False, right=False, left=False)
                elif decision == 1:
                    self.game.move_car(up=True, down=False, right=True, left=False)
                elif decision == 2:
                    self.game.move_car(up=True, down=False, right=False, left=True)
                elif decision == 3:
                    self.game.move_car(up=False, down=True, right=False, left=False)

                
                self.game.loop()
                
                self.game.check_checkpoints()
                if self.game.check_collisions():
                    self.game.laps = 0
                    run = False

    def calculate_fitness(self, genome):
        genome.fitness += self.game.laps

     
"""
def eval_genomes(genomes, config):
    width, height = 1400, 750
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Racing")

    for i, (genome_id, genome) in enumerate(genomes):
        print(round(i/len(genomes) * 100), end=" ")
        genome.fitness = 0
        racing = RacingGame(win, width, height)
        force_quit = racing.train_ai(genome, config)
        if force_quit:
            quit()
"""

def eval_genomes(genomes, config):
    width, height = 1400, 750
    window = pygame.display.set_mode((width, height))
    #window = pygame.Surface((width, height))

    for i, (genome_id, genome) in enumerate(genomes):
        #print("genome: ", genome)
        genome.fitness = 0
        game = RacingGame(window, width, height)
        game.train_ai(genome, config)
            
def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-54')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 1)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    width, height = 1400, 750
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Racing")
    racing = RacingGame(win, width, height)
    racing.test_ai(winner, config)
    #racing.test_drive()


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

    #run_neat(config)
    test_best_network(config)
    
