#!/usr/bin/env python3.7

# Copyright 2020, Gurobi Optimization, LLC

# Solve a network flow problem. 
# One products is produced in 2 cities ('Detroit' and 'Denver') and must be sent to
# warehouses in 3 cities ('Boston', 'New York', and 'Seattle') to
# satisfy demand ('inflow[i]').
#
# Flows on the transportation network must respect arc capacity constraints
# ('capacity[i,j]'). The objective is to minimize the sum of the arc
# transportation costs ('cost[i,j]').

import gurobipy as gp
from gurobipy import GRB

# Base data
nodes = ['Detroit', 'Denver', 'Boston', 'New York', 'Seattle']

arcs, capacity = gp.multidict({
    ('Detroit', 'Boston'):   100,
    ('Detroit', 'New York'):  80,
    ('Detroit', 'Seattle'):  120,
    ('Denver',  'Boston'):   120,
    ('Denver',  'New York'): 120,
    ('Denver',  'Seattle'):  120})

# Cost for pairs source-destination
cost = {
    ('Detroit', 'Boston'):   10,
    ('Detroit', 'New York'): 20,
    ('Detroit', 'Seattle'):  60,
    ('Denver',  'Boston'):   40,
    ('Denver',  'New York'): 40,
    ('Denver',  'Seattle'):  30 }

# Demand for city
inflow = {
    ('Detroit'):   50,
    ('Denver'):    60,
    ('Boston'):   -50,
    ('New York'): -50,
    ('Seattle'):  -10 }

# Create optimization model
m = gp.Model('netflow')

# Create variables
x = m.addVars(arcs, obj=cost, name="x")

# Arc-capacity constraints
m.addConstrs((x[i, j] <= capacity[i, j] for i, j in arcs), "cap")

# Equivalent version using Python looping
# for i, j in arcs:
#   m.addConstr(x[i, j] <= capacity[i, j], "cap[%s, %s]" % (i, j))


# Flow-conservation constraints
m.addConstrs((x.sum('*', j) + inflow[j] == x.sum(j, '*') for j in nodes), "node")

# Alternate version:
# m.addConstrs(
#   (gp.quicksum(x[i, j] for i, j in arcs.select('*', j)) + inflow[j] ==
#     gp.quicksum(x[j, k] for j, k in arcs.select(j, '*'))
#     for j in nodes), "node")


# write problem
m.write('network.lp')

# Compute optimal solution
m.optimize()

# Print solution
if m.status == GRB.OPTIMAL:
    solution = m.getAttr('x', x)
    print('\nOptimal network flows:')
    for i, j in arcs:
        if solution[i, j] > 0:
            print('%s -> %s: %g' % (i, j, solution[i, j]))
