import pygame
import sys
import math
import random
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()
win = pygame.display.set_mode((1280, 720))

# pygame.font.init()
# my_font = pygame.font.SysFont('Comic Sans MS', 30)


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def len(self):
        return math.sqrt(self.x**2+self.y**2)

    def __add__(self, o):
        return Vec2(self.x+o.x, self.y+o.y)

    def __sub__(self, o):
        return Vec2(self.x-o.x, self.y-o.y)

    def __truediv__(self, o):
        return Vec2(self.x/o, self.y/o)

    def __mul__(self, o):
        return Vec2(self.x*o, self.y*o)

    def to_tuple(self):
        return (self.x, self.y)
    __rmul__ = __mul__


# parameters
center = Vec2(1280/2, 720/2)
radius = 30
G = 100000

objs = []


class Ball:
    def __init__(self, p, r, v0, color):
        self.p = p
        self.oldp = p-v0
        self.r = r
        self.color = color
        self.acc = Vec2(0, 0)
        self.stop = False

    def render(self):
        pygame.draw.circle(win, self.color, (self.p.x, self.p.y), self.r)

    # verlet integration
    def updatePos(self, dt):
        v = self.p-self.oldp
        self.oldp = self.p
        self.p += v+self.acc*dt*dt
        self.acc = Vec2(0, 0)


def applyGravity(obj):
    to_obj = center-obj.p
    r = to_obj.len()
    if r <= radius:
        obj.stop = True
        return
    obj.acc += G*to_obj/(r**3)


def update(dt):
    for obj in objs:
        applyGravity(obj)
        obj.updatePos(dt)


def deleteUseless():
    i = 0
    while i < len(objs):
        if objs[i].stop:
            del objs[i]
            continue
        (x, y) = (objs[i].p.x, objs[i].p.y)
        if x < 0 or x > 1280:
            del objs[i]
        elif y < 0 or y > 720:
            del objs[i]
        else:
            i += 1


def render():
    win.fill((0, 0, 0))
    for obj in objs:
        obj.render()
    pygame.draw.circle(win, (0, 0, 255), center.to_tuple(), radius)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i in range(10):
                v = Vec2(2*(random.random()-0.5), 2*(random.random()-0.5))
                color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                objs.append(Ball(Vec2(pos[0], pos[1]), 5, v, color))
                # objs.append(Ball(Vec2(pos[0],pos[1]),5,-1*v,color))
    for i in range(2):
        update(0.05/2)
    render()
    deleteUseless()
    pygame.display.flip()
    fpsClock.tick(120)
