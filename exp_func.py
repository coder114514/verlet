import math,matplotlib.pyplot as plt

n=100
dt=10/n
t=0
oldx=-dt
x=0

axis1=[]
axis2=[]

vaxis1=[]
vaxis2=[]

eaxis1=[]
eaxis2=[]
for i in range(n+1):
    a=x
    v=x-oldx
    oldx=x
    x+=v+a*dt*dt
    axis2.append(x)
    axis1.append(t)
    vaxis2.append(math.exp(t))
    vaxis1.append(t)
    eaxis2.append(x-math.exp(t))
    eaxis1.append(t)
    print(t,math.exp(t))
    t+=dt
    # print(t)

plt.plot(axis1,axis2,label="approximation")
plt.plot(vaxis1,vaxis2,label="exact")
plt.plot(eaxis1,eaxis2,label="error")
plt.legend()
plt.show()