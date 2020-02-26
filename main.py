import pygame as pg
import pygame.gfxdraw
import numpy  as np

from random import randint
from func import *

WIDTH  = 640
HEIGHT = 480
WHITE  = (255, 255, 255)
GREEN  = (50, 200, 50, 50)
RED    = (200, 0, 0)

PLAYERS = 100

floor_y = HEIGHT - 40

player_radius = 50
player_x = 100
player_y = [ 0 ] * PLAYERS
player_y_speed = [ 0 ] * PLAYERS
player_alive = [ True ] * PLAYERS
player_fitness = [ 0 ] * PLAYERS

obstacle_x = []
obstacle_radius = []
for i in range(1, 4):
    obstacle_x.append(WIDTH * i + randint(-25, 25))
    obstacle_radius.append(randint(40, 70))

weights = [ [ (np.random.rand(3,5) - 0.5) * 0.1, (np.random.rand(5,1) - 0.5 ) * 0.1 ] for x in range(PLAYERS) ]

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

running = True
while running:
    clock.tick(60) # 60 fps

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player_alive = [ False ] * 100

    # Update
    for o in range(3):
        obstacle_x[o] -= 10
        if obstacle_x[o] < -100:
            obstacle_x[o] = WIDTH * 3 + randint(-25, 25)
            obstacle_radius[o] = randint(40,70)

    if not any(player_alive):
        # Skapa ny generation
        weights = new_generation(weights, player_fitness)
        player_y = [ 0 ] * PLAYERS
        player_y_speed = [ 0 ] * PLAYERS
        player_alive = [ True ] * PLAYERS
        player_fitness = [ 0 ] * PLAYERS
        print("New generation")


    for p in range(PLAYERS):
        player_y_speed[p] += 1
        player_y[p] += player_y_speed[p]

        if player_y[p] > floor_y - player_radius:
            player_y[p] = floor_y - player_radius
            player_y_speed[p] = 0

        closest_radius = 0
        for r in range(len(obstacle_radius)):
            if obstacle_radius[r] < obstacle_radius[closest_radius]:
                closest_radius = r
        closest_radius = obstacle_radius[closest_radius]
        if think(weights[p], np.array([10, min(obstacle_x), closest_radius])) and player_y[p] == floor_y - player_radius:
            player_y_speed[p] = -20

        if player_alive[p]:
            player_fitness[p] += 1

        if circle_collision(player_x, player_y[p], player_radius, min(obstacle_x), floor_y - closest_radius, closest_radius):
            player_alive[p] = False


    # Draw
    screen.fill((0, 0, 0))
    pg.draw.rect(screen, WHITE, (0, floor_y, WIDTH, 2))

    for o in range(3):
        draw_circle(screen, obstacle_x[o], floor_y - obstacle_radius[o], obstacle_radius[o], RED)
        
    for p in range(PLAYERS):
        if player_alive[p]:
            draw_circle(screen, player_x, player_y[p], player_radius, GREEN)

    pg.display.flip()

