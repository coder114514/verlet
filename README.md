# verlet

some simple physics simulation using verlet integration (in python)

## Dependency

pygame

## Derivation
### regular verlet integration
$x(t+h)=x(t)+v(t)h+a(t)\frac{h^2}{2}+a'(t)\frac{h^3}{6}+...\hspace{1cm}\text{(1)}$

$x(t-h)=x(t)-v(t)h+a(t)\frac{h^2}{2}-a'(t)\frac{h^3}{6}+...\hspace{1cm}\text{(2)}$

$x(t+h)+x(t-h)=2x(t)+a(t)h^2+\mathcal{O}(h^4)\hspace{1.4cm}\text{(3): (1)+(2)}$

$x(t+h)=2x(t)-x(t-h)+a(t)h^2+\mathcal{O}(h^4)\hspace{1.4cm}\text{(4): solve for } x(t+h) \text{ in (3)}$

$x(t+h)-x(t-h)=2v(t)h+\mathcal{O}(h^3)\hspace{2.8cm}\text{(5): (1)-(2)}$

$v(t)=\frac{x(t+h)-x(t-h)}{2h}+\mathcal{O}(h^2)\hspace{4.45cm}\text{(6): solve for } v(t) \text{ in (5)}$

then (4) and (6) are the formulas for verlet integration

### velocity verlet

$x(t-h)=x(t+h)-2v(t)h+\mathcal{O}(h^3)\hspace{3.95cm}\text{(7): solve for }x(t-h)\text{ in (5)}$

$x(t+h)=x(t)+v(t)h+a(t)\frac{h^2}{2}+\mathcal{O}(h^3)\hspace{3.25cm}\text{(8): plug (7) into (4), then solve for }x(t+h)$

$x(t+2h)=2x(t+h)-x(t)+a(t+h)h^2+\mathcal{O}(h^4)\hspace{1.6cm}\text{(9): }t\rightarrow t+h\text{ in (4)}$

$v(t+h)=\frac{x(t+2h)-x(t)}{2h}+\mathcal{O}(h^2)\hspace{5.15cm}\text{(10): }t\rightarrow t+h\text{ in (6)}$

$v(t+h)=\frac{x(t+h)-x(t)}{h}+a(t+h)\frac{h}{2}+\mathcal{O}(h^2)\hspace{3cm}\text{(11): sub (9) into (10)}$

$v(t+h)=v(t)+\frac{h}{2}[a(t)+a(t+h)]+\mathcal{O}(h^2)\hspace{2.7cm}\text{(12): sub (1) into (11)}$

then (8) and (12) are the formulas for velocity verlet
