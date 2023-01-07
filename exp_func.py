from math import exp
import matplotlib.pyplot as plt

#equation: a = x, v(0) = 1, x(0) = 1
#exact solution: x = exp(t)

n = 100000
dt = 100 / n

axis_t = []
axis_exact = []

for i in range(n+1):
    axis_t.append(i*dt)
    axis_exact.append(exp(i*dt))

def euler():
    x = 1
    v = 1
    xa = []
    ea = []
    for t in axis_t:
        xa.append(x)
        ea.append((x-exp(t))/exp(t)*100)
        a = x
        x += v * dt
        v += a * dt
    return xa,ea

def verlet():
    oldx = 1 - dt
    x = 1
    xa = []
    ea = []
    for t in axis_t:
        xa.append(x)
        ea.append((x-exp(t))/exp(t)*100)
        a = x
        v = x - oldx
        oldx = x
        x += v + a*dt*dt
    return xa,ea

axis_euler,axis_euler_error = euler()
axis_verlet,axis_verlet_error = verlet()

print("euler error: " + str(axis_euler_error[-1]) + "%")
print("verlet error: " + str(axis_verlet_error[-1]) + "%")

#plt.plot(axis_t, axis_exact, label="exact")
#plt.plot(axis_t, axis_euler, label="euler")
#plt.plot(axis_t, axis_verlet, label="verlet")
plt.plot(axis_t, axis_euler_error, label="euler error")
plt.plot(axis_t, axis_verlet_error, label="verlet error")
plt.legend()
plt.show()

