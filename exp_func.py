from math import exp
import matplotlib.pyplot as plt

n = 1000
dt = 100 / n
t = 0
oldx = -dt
x = 0

axis_x = []
axis_y = []

vaxis_x = []
vaxis_y = []

eaxis_x = []
eaxis_y = []

epaxis_x = []
epaxis_y = []

for i in range(n+1):
    a = x
    v = x - oldx
    oldx = x
    x += v + a*dt*dt
    axis_y.append(x)
    axis_x.append(t)
    vaxis_y.append(exp(t))
    vaxis_x.append(t)
    eaxis_y.append(x - exp(t))
    eaxis_x.append(t)
    epaxis_y.append(abs(x-exp(t)) / exp(t) * 100)
    epaxis_x.append(t)
    t += dt # t == i*dt

print("error: " + str(epaxis_y[-1]) + "%")

#plt.plot(axis_x, axis_y, label="verlet")
#plt.plot(vaxis_x, vaxis_y, label="exact")
#plt.plot(eaxis_x, eaxis_y, label="error")
plt.plot(epaxis_x, epaxis_y, label="error %")
plt.legend()
plt.show()
