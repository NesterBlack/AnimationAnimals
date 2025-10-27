#!/usr/bin/env -S uv run --script
# /// script
# dependencies = ["pygame", "shapely"]
# ///

import pygame
from animation import Animal


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("Arial", 40)
clock = pygame.time.Clock()

animal = Animal(screen, "robocode", 0.5, (82, 179, 227), debug=False)
running = True
if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        animal.move_animal(pygame.mouse.get_pos(), 10)
        animal.draw_animal(screen)

        pygame.display.flip()
        clock.tick(60)
