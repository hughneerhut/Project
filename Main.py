from pyswarm import pso

def banana(x):
    x1 = x[0]
    x2 = x[1]
    return 100*(x1 - (x2)**2)**2 + (x2 - 1)**2


lb = [0, 0]
ub = [15, 30]

xopt, fopt = pso(banana, lb, ub)

print(xopt)
print(fopt)