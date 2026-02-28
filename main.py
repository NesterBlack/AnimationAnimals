import pygame
from animation import *


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("Arial", 40)
clock = pygame.time.Clock()

pos = pygame.Vector2(0,0)
direction = pygame.Vector2(0,0)

animal = Bird()
running = True
if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        animal.move_animal(pygame.mouse.get_pos(), 0.1)

        attributes = animal.get_points_for_draw()
        pygame.draw.polygon(screen, (82, 179, 227), attributes[0], 0)

        print(attributes[2])
        pygame.draw.polygon(screen, (82, 100, 227), attributes[2], )

        for point in attributes[1]:
            pygame.draw.circle(screen, (255,255,255), point, 10)
            pygame.draw.circle(screen, (0, 0, 0), point, 4)

        debug = animal.debug()
        # for line in debug[0]:
        #     pygame.draw.line(screen, (255, 255, 255), line[0], line[1], 1)
        # for points in debug[1]:
        #     print(points)
        #     pygame.draw.circle(screen, (255, 0, 0), points, 5)
        # for par in debug[2]:
        #     pygame.draw.circle(screen, (0, 255, 0), par[0], par[1], 3)

        pygame.display.flip()
        # clock.tick(60)
