#!/usr/bin/env python3.7

import gurobipy as gp
from gurobipy import GRB

# size of problem
n = 5

## set
nodes = range(n)

# demand
b = [-5, 10, 0, -2, -3] 

#b = {
#    0: -5,
#    1: 10,
#    2: 0,
#    3: -2,
#    4: -3 }

# cost matrix
cost = {
    (0, 1): 2,
    (0, 2): 5,
    (1, 2): 3,
    (2, 3): 1,
    (2, 4): 2,
    (3, 0): 0,
    (3, 4): 2,
    (4, 1): 4 }

# capacity matrix
arcs, cap = gp.multidict({
    (0, 1): 10,
    (0, 2): 10,
    (1, 2): 10,
    (2, 3): 10,
    (2, 5): 10,
    (3, 0): 10,
    (3, 4): 10,
    (4, 1): 10})

# set model
m = gp.Model('minimum_cost_flow')

# add variables
x = m.addVars(arcs,obj=cost,name='x')

# set objective function
m.modelSense = GRB.MINIMIZE

# Arc-capacity constraints
m.addConstrs((x[i, j] <= cap[i, j] for i, j in arcs), "cap")

# Flow-conservation constraints
m.addConstrs((x.sum('*', j) + inflow[j] == x.sum(j, '*') for j in nodes), "flow")

# Write problem
m.write("min_cost_flow.lp")

# Solve problem
m.optimize()

# Print solution
if m.status == GRB.OPTIMAL:
    print('Optimal solution: %g' % m.objVal)
    solution = m.getAttr('x', x)
    print('\nOptimal flows:')
    for i, j in arcs:
        if solution[i, j] > 0:
            print('%s -> %s: %g' % (i, j, solution[i, j]))
