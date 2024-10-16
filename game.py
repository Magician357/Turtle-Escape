import pygame
from random import randint
from maze import generate_maze_growing_tree, choosing_algorithm # type: ignore

width, height = 800, 800
fps = 60

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

background_color=(255,255,255)

maze = generate_maze_growing_tree(10,10,choosing_algorithm)

while running:
    # clear previous frame
    screen.fill(background_color)
    
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    

    pygame.display.flip()

    clock.tick(fps)  # limit fps
