import pygame,sys,math,random,time
from pygame.locals import *

pygame.init()
fpsClock=pygame.time.Clock()
win=pygame.display.set_mode((1280,720))

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)

class Vec2:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def len(self):
        return math.sqrt(self.x**2+self.y**2)
    def __add__(self,o):
        return Vec2(self.x+o.x,self.y+o.y)
    def __sub__(self,o):
        return Vec2(self.x-o.x,self.y-o.y)
    def __truediv__(self,o):
        return Vec2(self.x/o,self.y/o)
    def __mul__(self,o):
        return Vec2(self.x*o,self.y*o)
    __rmul__=__mul__
    def dot(self,o):
        return self.x*o.x+self.y*o.y

# velocity verlet
# p'=p+v*dt+0.5*a*dt*dt 
# v'=v+0.5*(a+a')*dt

class Ball:
    def __init__(self,r,m,p0,v0,color):
        self.r=r
        self.m=m
        self.p=p0
        self.v=v0
        self.a=self.olda=Vec2(0,0)
        self.color=color
    
    def render(self):
        pygame.draw.circle(win,self.color,(self.p.x,self.p.y),self.r)
    
    def updatePos(self,dt):
        self.p+=self.v*dt+0.5*self.a*dt*dt
        self.olda=self.a
        self.a=Vec2(0,0)
    
    def updateVelocity(self,dt):
        self.v+=0.5*(self.olda+self.a)*dt

def applyGravity():
    center=Vec2(1280/2,720/2)
    for obj in objs:
        obj.olda=obj.a
    for obj1 in objs:
        for obj2 in objs:
            if obj1==obj2:continue
            r=obj2.p-obj1.p
            d=r.len()
            obj1.a+=G*obj2.m*r/(d**3)

def solveCollision():
    for i in range(len(objs)):
        for j in range(i+1,len(objs)):
            obj1=objs[i]
            obj2=objs[j]
            delta=obj1.p-obj2.p
            r=delta.len()
            mind=obj1.r+obj2.r
            delta/=r
            if r<mind:
                obj1.p+=0.5*delta*(mind-r)
                obj2.p-=0.5*delta*(mind-r)
                (v1,v2)=(obj1.v,obj2.v)
                v1L=v1.dot(delta)*delta
                v2L=v2.dot(delta)*delta
                v1P=v1-v1L
                v2P=v2-v2L
                (m1,m2)=(obj1.m,obj2.m)
                vcm=(m1*v1L+m2*v2L)/(m1+m2)
                (obj1.v,obj2.v)=(2*vcm-v1L+v1P,2*vcm-v2L+v2P)


def update(dt):
    for obj in objs:
        obj.updatePos(dt)
    applyGravity()
    for obj in objs:
        obj.updateVelocity(dt)
    solveCollision()

def render():
    win.fill((0,0,0))
    for obj in objs:
        obj.render()

objs=[]
nsub=10
dt=0.1/nsub
G=1000

# objs.append(Ball(10,100,Vec2(600,360),Vec2(10,0),(255,255,255)))
# objs.append(Ball(10,100,Vec2(680,360),Vec2(-10,0),(255,255,255)))

Elast = 0
Eclock = time.time()
delta_E = 0

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            v=Vec2(10*(random.random()-0.5),10*(random.random()-0.5))
            objs.append(Ball(10,random.randint(100,500),Vec2(pos[0],pos[1]),v,color))
    for i in range(nsub):
        update(dt)
    render()
    E = 0
    for obj in objs:
        E += 0.5 * obj.m * (obj.v.x*obj.v.x+obj.v.y*obj.v.y)
    for obj1 in objs:
        for obj2 in objs:
            if obj1==obj2:continue
            r=obj2.p-obj1.p
            d=r.len()
            E-=G*obj1.m*obj2.m/d
    if  time.time() - Eclock >= 0.5:
        Eclock =  time.time()
        delta_E = E - Elast
        Elast = E
    E = round(E,2)
    text_surface = my_font.render('Total Energy: '+str(E), True, (255, 255, 255))
    win.blit(text_surface, (0,0))
    text_surface = my_font.render('ΔE: '+str(round(delta_E,2)), True, (255, 255, 255))
    win.blit(text_surface, (0,20))
    pygame.display.flip()
    fpsClock.tick(60)
    
