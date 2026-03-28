import pygame
import random
from animation import *


pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("Arial", 40)
clock = pygame.time.Clock()

class Apple:
    def __init__(self, screen):
        self.screen = screen
        self.pos = (0,0)

    def spawn_apple(self):
        self.pos = (random.randint(0,SCREEN_WIDTH),random.randint(0,SCREEN_HEIGHT))

    def draw(self):
        rect = pygame.Rect(self.pos[0], self.pos[1], 15,15)
        pygame.draw.rect(self.screen, (255,0,0), rect)

    def get_rect(self):
        rect = pygame.Rect(self.pos[0], self.pos[1], 15, 15)
        return rect

pos = pygame.Vector2(0,0)
direction = pygame.Vector2(0,0)

apple = Apple(screen)
apple.spawn_apple()
animal = SnakeIO(rotated_speed=7)
animal.add_ball(100)
speed = 5
running = True
if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        test = animal.move_animal(pygame.mouse.get_pos(), speed)

        attributes = animal.get_points_for_draw()
        for pos in attributes[1]:
            ccc = 0
            pygame.draw.circle(screen, (45-random.randint(-ccc,ccc), 109-random.randint(-ccc,ccc), 140-random.randint(-ccc,ccc)), pos, attributes[0]+2)
            pygame.draw.circle(screen, (82-random.randint(-ccc,ccc), 179-random.randint(-ccc,ccc), 227-random.randint(-ccc,ccc)), pos, attributes[0])

        # print(attributes[2])
        # pygame.draw.polygon(screen, (82, 100, 227), attributes[2], )

        for point in attributes[2]:
            pygame.draw.circle(screen, (255,255,255), point, 4)
            pygame.draw.circle(screen, (0, 0, 0), point, 2)

        apple.draw()

        apple_rect = apple.get_rect()
        tuple_rect = animal.get_head_rect()
        rect = pygame.Rect(tuple_rect[0], tuple_rect[1], tuple_rect[2], tuple_rect[3])

        if rect.colliderect(apple_rect):
            apple.spawn_apple()
            animal.add_ball(10)

        debug = animal.debug()
        # for line in debug[0]:
        #     pygame.draw.line(screen, (255, 255, 255), line[0], line[1], 1)
        #     print(points)
        #     pygame.draw.circle(screen, (255, 0, 0), points, 5)
        # for par in debug[2]:
        #     pygame.draw.circle(screen, (0, 255, 0), par[0], par[1], 3)


        # pygame.draw.rect(screen, (255, 255, 255), rect)

        pygame.display.flip()
        clock.tick(60)
