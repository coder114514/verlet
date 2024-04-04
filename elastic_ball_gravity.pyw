import pygame
import sys
import random
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()
win = pygame.display.set_mode((1280, 720))

pygame.font.init()
my_font = pygame.font.SysFont('Arial', 20)


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def len(self):
        return (self.x*self.x+self.y*self.y)**0.5

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


def applyGravity():
    for obj1 in objs:
        for obj2 in objs:
            if obj1 == obj2:
                continue
            r = obj2.p-obj1.p
            d = r.len()
            obj1.a += G*obj2.m*r/(d**3)


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
    applyGravity()
    for obj in objs:
        obj.updateVelocity(dt)
    solveCollision()


def render():
    win.fill((0, 0, 0))
    tx, ty, tm = 0, 0, 0
    for obj in objs:
        obj.render()
        tx += obj.p.x * obj.m
        ty += obj.p.y * obj.m
        tm += obj.m
    pygame.draw.circle(win, (255,0,0), (tx/tm, ty/tm), 3)


objs = []
nsub = 40
dt = 0.1/nsub
G = 1000

objs.append(Ball(10,100,Vec2(640,320),Vec2(25,0),(0,0,255)))
objs.append(Ball(10,100,Vec2(640,400),Vec2(-25,0),(0,0,255)))

displayE = 0
Es = []

def print_energy():
    global displayE, Es
    E = 0
    for obj in objs:
        E += 0.5 * obj.m * (obj.v.x*obj.v.x+obj.v.y*obj.v.y)
    for obj1 in objs:
        for obj2 in objs:
            if obj1 == obj2:
                continue
            r = obj2.p-obj1.p
            d = r.len()
            E += G*obj1.m*obj2.m*(1/20-1/d)
    Es.append(E)
    if len(Es) > 100: del Es[0]
    displayE = round(sum(Es)/100, 3)
    text_surface = my_font.render('E   '+str(displayE), True, (255, 255, 255))
    win.blit(text_surface, (0, 0))
    text_surface = my_font.render('#    '+str(len(objs)), True, (255, 255, 255))
    win.blit(text_surface, (0, 20))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and event.button != 3:
            pos = pygame.mouse.get_pos()
            mass = random.randint(10, 100)
            color = (0, round((100-mass)/90*255), round((mass-10)/90*255))
            v = Vec2(50*(random.random()-0.5), 50*(random.random()-0.5))
            objs.append(Ball(10, mass, Vec2(pos[0], pos[1]), v, color))
        elif event.type == MOUSEBUTTONDOWN and event.button == 3:
            if len(objs) > 1: del objs[0]
    for i in range(nsub):
        update(dt)
    render()
    print_energy()
    pygame.display.flip()
    fpsClock.tick(60)
