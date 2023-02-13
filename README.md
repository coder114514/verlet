# verlet

some simple physics simulation using verlet integration (in python)

## dependency

pygame

## derivation
### regular verlet integration
$x(t+h)=x(t)+v(t)h+a(t)\frac{h^2}{2}+a'(t)\frac{h^3}{6}+...$ ___(1)

$x(t-h)=x(t)-v(t)h+a(t)\frac{h^2}{2}-a'(t)\frac{h^3}{6}+...$ ___(2)

$x(t+h)+x(t-h)=2x(t)+a(t)h^2+\mathcal{O}(h^4)$ ___(3): (1)+(2)

$x(t+h)=2x(t)-x(t-h)+a(t)h^2+\mathcal{O}(h^4)$ ___(4): solve for $x(t+h)$ in (3)

$x(t+h)-x(t-h)=2v(t)h+\mathcal{O}(h^3)$ ___(5): (1)-(2)

$v(t)=\frac{x(t+h)-x(t-h)}{2h}+\mathcal{O}(h^2)$ ___(6): solve for $v(t)$ in (5)

then (4) and (6) are the formulas for verlet integration

### velocity verlet

$x(t-h)=x(t+h)-2v(t)h+\mathcal{O}(h^3)$ ___(7): solve for $x(t-h)$ in (5)

$x(t+h)=x(t)+v(t)h+a(t)\frac{h^2}{2}+\mathcal{O}(h^3)$ ___(8): plug (7) into (4), then solve for $x(t+h)$

$x(t+2h)=2x(t+h)-x(t)+a(t+h)h^2+\mathcal{O}(h^4)$ ___(9): $t\rightarrow t+h$ in (4)

$v(t+h)=\frac{x(t+2h)-x(t)}{2h}+\mathcal{O}(h^2)$ ___(10): $t\rightarrow t+h$ in (6)

$v(t+h)=\frac{x(t+h)-x(t)}{h}+a(t+h)\frac{h}{2}+\mathcal{O}(h^2)$ ___(11): sub (9) into (10)

$v(t+h)=v(t)+\frac{h}{2}[a(t)+a(t+h)]+\mathcal{O}(h^2)$ ___(12): sub (1) into (11)

then (8) and (12) are the formulas for velocity verlet
