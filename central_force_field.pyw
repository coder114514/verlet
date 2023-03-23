import pygame
import sys
import math
import random
import time
from pygame.locals import *

W = 1280
H = 720

pygame.init()
fpsClock = pygame.time.Clock()
win = pygame.display.set_mode((W, H))

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)


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
    __rmul__ = __mul__

    def dot(self, o):
        return self.x*o.x+self.y*o.y

# velocity verlet
# p'=p+v*dt+0.5*a*dt*dt
# v'=v+0.5*(a+a')*dt


class Ball:
    def __init__(self, r, m, p0, v0, color):
        self.r = r
        self.m = m
        self.p = p0
        self.v = v0
        self.a = self.olda = Vec2(0, 0)
        self.color = color

    def render(self):
        pygame.draw.circle(win, self.color, (self.p.x, self.p.y), self.r)

    def updatePos(self, dt):
        self.p += self.v*dt+0.5*self.a*dt*dt
        self.olda = self.a
        self.a = Vec2(0, 0)

    def updateVelocity(self, dt):
        self.v += 0.5*(self.olda+self.a)*dt


def applyCentral():
    center = Vec2(W / 2, H / 2)
    for obj in objs:
        obj.a += G * (center - obj.p) / obj.m


def solveCollision():
    for i in range(len(objs)):
        for j in range(i+1, len(objs)):
            obj1 = objs[i]
            obj2 = objs[j]
            delta = obj1.p-obj2.p
            r = delta.len()
            mind = obj1.r+obj2.r
            delta /= r
            if r < mind:
                obj1.p += 0.5*delta*(mind-r)
                obj2.p -= 0.5*delta*(mind-r)
                (v1, v2) = (obj1.v, obj2.v)
                v1L = v1.dot(delta)*delta
                v2L = v2.dot(delta)*delta
                v1P = v1-v1L
                v2P = v2-v2L
                (m1, m2) = (obj1.m, obj2.m)
                vcm = (m1*v1L+m2*v2L)/(m1+m2)
                (obj1.v, obj2.v) = (2*vcm-v1L+v1P, 2*vcm-v2L+v2P)


def update(dt):
    for obj in objs:
        obj.updatePos(dt)
    applyCentral()
    for obj in objs:
        obj.updateVelocity(dt)
    solveCollision()


def render():
    win.fill((0, 0, 0))
    for obj in objs:
        obj.render()


objs = []
nsub = 10
dt = 0.1 / nsub
G = 10

# objs.append(Ball(10,100,Vec2(600,360),Vec2(10,0),(255,255,255)))
# objs.append(Ball(10,100,Vec2(680,360),Vec2(-10,0),(255,255,255)))

Elast = 0
Eclock = time.time()
delta_E = 0

def print_energy():
    global Elast, Eclock, delta_E
    E = 0
    for obj in objs:
        E += 0.5 * obj.m * (obj.v.x*obj.v.x+obj.v.y*obj.v.y)
        center = Vec2(W / 2, H / 2)
        dist = (obj.p-center).len()
        E += 0.5 * G * dist * dist
    if time.time() - Eclock >= 0.5:
        Eclock = time.time()
        delta_E = E - Elast
        Elast = E
    E = round(E, 2)
    text_surface = my_font.render(
        'Total Energy: '+str(E), True, (255, 255, 255))
    win.blit(text_surface, (0, 0))
    text_surface = my_font.render(
        'ΔE: '+str(round(delta_E, 2)), True, (255, 255, 255))
    win.blit(text_surface, (0, 20))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i in range(1):
                pos = Vec2(pos[0], pos[1])
                v = Vec2(200*(random.random()-0.5), 200*(random.random()-0.5))
                r = random.randint(20, 255)
                g = random.randint(20, 255)
                b = random.randint(20, 255)
                objs.append(Ball(10, random.randint(50, 150), pos, v, (r, g, b)))
    for i in range(nsub):
        update(dt)
    render()
    print_energy()
    pygame.display.flip()
    fpsClock.tick(60)
