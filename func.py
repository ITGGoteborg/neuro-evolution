import pygame as pg
import pygame.gfxdraw
import numpy  as np

from random import randint

def draw_circle(surface, x, y, r, color):
    pg.gfxdraw.aacircle(surface, x ,y ,r, color)
    pg.gfxdraw.filled_circle(surface, x ,y ,r, color)

def circle_collision(x1, y1, r1, x2, y2, r2):
    dist = (x2 - x1) ** 2 + (y2 - y1) ** 2
    return dist < (r1 + r2) ** 2

# AI
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def think(weights, inp):
    a1 = sigmoid(np.dot(inp, weights[0]))
    a2 = sigmoid(np.dot(a1, weights[1]))
    return a2 > 0.5

def mutate(weights):
    mut_size = 0.02
    mut0 = (np.random.rand(3,5) - 0.5) * mut_size
    mut1 = (np.random.rand(5,1) - 0.5) * mut_size
    return [weights[0] + mut0, weights[1] + mut1]

def new_generation(old_weights, fitness):
    probs = [ f ** 2 for f in fitness ]
    tot = sum(probs)
    probs = np.array([ f / float(tot) for f in probs ])
    new_indices = np.random.choice(range(len(old_weights)), len(old_weights), p=probs)
    new_weights = [ old_weights[i] for i in new_indices ]
    mutated = list(map(mutate, new_weights))
    return mutated

