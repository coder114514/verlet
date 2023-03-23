import pygame
import sys
import math
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()
(W, H) = (1360, 768)
screen = pygame.display.set_mode((W, H))

# parameters
gravity = 0.8
bounce = 0.9
friction = 0.99


class Point:
    def __init__(self, x, y, oldx, oldy, fixed=False, hidden=True):
        self.x = x
        self.y = y
        self.oldx = oldx
        self.oldy = oldy
        self.fixed = fixed
        self.hidden = hidden


class Sticstiffness: # stick with stiffness
    def __init__(self, p1, p2, len, hidden=False):
        self.p1 = p1
        self.p2 = p2
        self.len = len
        self.hidden = hidden


class Spring:
    def __init__(self, p1, p2, len, stiffness):
        self.p1 = p1
        self.p2 = p2
        self.len = len
        self.stiffness = stiffness
        self.hidden = False


class Rect:
    def __init__(self, p1, p2, p3, p4):
        self.points = [p1, p2, p3, p4]


class Engine:
    def __init__(self, x, y, A, angle, speed):
        self.x = self.x0 = x
        self.y = self.y0 = y
        self.A = A
        self.angle = angle
        self.speed = speed
        self.fixed = True


points = {}
sticstiffnesss = {}
rects = {}
engines = {}
springs = {}


def dist(p1, p2):
    dx = p1.x-p2.x
    dy = p1.y-p2.y
    return math.sqrt(dx*dx+dy*dy)


points[1] = Point(630, 500, 630, 500, hidden=False)
points[2] = Point(730, 500, 730, 500)
points[3] = Point(730, 600, 730, 600)
points[4] = Point(630, 600, 630, 600)
points[5] = Point(680, 400, 680, 400, hidden=False)
points[6] = Point(680, 300, 680, 300, hidden=False)
points[7] = Point(680, 450, 680, 450, hidden=False)
points[8] = Point(680, 350, 680, 350, hidden=False)

engines[1] = Engine(680, 200, 100, 0, 0.1)

sticstiffnesss[1] = Sticstiffness(points[1], points[2], dist(points[1], points[2]), True)
sticstiffnesss[2] = Sticstiffness(points[2], points[3], dist(points[2], points[3]), True)
sticstiffnesss[3] = Sticstiffness(points[3], points[4], dist(points[3], points[4]), True)
sticstiffnesss[4] = Sticstiffness(points[1], points[4], dist(points[1], points[4]), True)
sticstiffnesss[5] = Sticstiffness(points[1], points[3], dist(points[1], points[3]), True)
sticstiffnesss[6] = Sticstiffness(points[2], points[4], dist(points[2], points[4]), True)
sticstiffnesss[7] = Sticstiffness(points[1], points[7], dist(points[1], points[7]))
sticstiffnesss[8] = Sticstiffness(points[5], points[7], dist(points[5], points[7]))
sticstiffnesss[9] = Sticstiffness(points[5], points[8], dist(points[5], points[8]))
# sticstiffnesss[10]=Sticstiffness(points[8],points[6],dist(points[8],points[6]))
sticstiffnesss[11] = Sticstiffness(points[6], engines[1], dist(points[6], engines[1]))

# springs[1]=Spring(points[6],engines[1],dist(points[6],engines[1]),0.0005)
springs[2] = Spring(points[8], points[6], dist(points[8], points[6]), 0.001)

rects[1] = Rect(points[1], points[2], points[3], points[4])


def updatePoints():
    for i in points:
        p = points[i]
        if p.fixed:
            continue
        vx = (p.x-p.oldx)*friction
        vy = (p.y-p.oldy)*friction
        p.oldx = p.x
        p.oldy = p.y
        p.x += vx
        p.y += vy
        p.y += gravity


def renderPoints():
    for i in points:
        point = points[i]
        if point.hidden:
            continue
        pygame.draw.circle(screen, (255, 255, 255), (point.x, point.y), 3)
        # print(point.x,point.y)


def constrainPoints():
    for i in points:
        p = points[i]
        if p.fixed:
            continue
        vx = (p.x-p.oldx) * bounce
        vy = (p.y-p.oldy) * bounce
        if p.x >= W:
            p.x = W
            p.oldx = p.x + vx
        elif p.x <= 0:
            p.x = 0
            p.oldx = p.x + vx
        if p.y >= H:
            p.y = H
            p.oldy = p.y + vy
        elif p.y <= 0:
            p.oldy = p.y + vy


def updateSticstiffnesss():
    for i in sticstiffnesss:
        s = sticstiffnesss[i]
        dx = s.p1.x-s.p2.x
        dy = s.p1.y-s.p2.y
        d = dist(s.p1, s.p2)
        percent = (d-s.len)/s.len/2
        # print(dx)
        if not s.p1.fixed:
            s.p1.x -= dx*percent
            s.p1.y -= dy*percent
        if not s.p2.fixed:
            s.p2.x += dx*percent
            s.p2.y += dy*percent


def renderSticstiffnesss():
    for i in sticstiffnesss:
        s = sticstiffnesss[i]
        if s.hidden:
            continue
        pygame.draw.line(screen, (255, 255, 255),
                         (s.p1.x, s.p1.y), (s.p2.x, s.p2.y))


def updateSprings():
    for i in springs:
        s = springs[i]
        dx = s.p1.x-s.p2.x
        dy = s.p1.y-s.p2.y
        d = dist(s.p1, s.p2)
        percent = (d - s.len)*s.stiffness / 2
        if not s.p1.fixed:
            s.p1.x -= dx*percent
            s.p1.y -= dy*percent
        if not s.p2.fixed:
            s.p2.x += dx*percent
            s.p2.y += dy*percent


def renderSprings():
    for i in springs:
        s = springs[i]
        if s.hidden:
            continue
        pygame.draw.line(screen, (255, 0, 0),
                         (s.p1.x, s.p1.y), (s.p2.x, s.p2.y))


def renderRects():
    for i in rects:
        r = rects[i]
        points = []
        for p in r.points:
            points.append((p.x, p.y))
        pygame.draw.polygon(screen, (0, 0, 255), points)


def updateEngines():
    for i in engines:
        e = engines[i]
        e.x = e.x0 + e.A * math.cos(e.angle)
        e.y = e.y0 + e.A * math.sin(e.angle)
        e.angle += e.speed


def renderEngines():
    for i in engines:
        e = engines[i]
        pygame.draw.circle(screen, (255, 255, 255), (e.x, e.y), 5)
        pygame.draw.circle(screen, (255, 255, 255), (e.x0, e.y0), e.A, 1)
        pygame.draw.line(screen, (255, 255, 255),
                         (e.x0-e.A, e.y0), (e.x0+e.A, e.y0))
        pygame.draw.line(screen, (255, 255, 255),
                         (e.x0, e.y0-e.A), (e.x0, e.y0+e.A))


buttonDown = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit(0)
        if event.type == MOUSEBUTTONDOWN:
            buttonDown = True
            pygame.mouse.set_pos((engines[1].x0, engines[1].y0))
        elif event.type == MOUSEBUTTONUP:
            buttonDown = False
        if event.type == MOUSEMOTION and buttonDown:
            (engines[1].x0, engines[1].y0) = pygame.mouse.get_pos()
    updatePoints()
    updateEngines()
    updateSprings()
    for i in range(3):
        constrainPoints()
        updateSticstiffnesss()
    screen.fill((0, 0, 0))
    renderPoints()
    renderSticstiffnesss()
    renderSprings()
    renderRects()
    renderEngines()
    pygame.display.flip()
    fpsClock.tick(60)
