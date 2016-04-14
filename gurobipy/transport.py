import gurobipy as gp
from collections import defaultdict

# define index sets and data coefficients
warehouses, capacity = gp.multidict(
  {'A': 6,
   'B': 5,
   'C': 4,
   'D': 6 })

centers, demand = gp.multidict(
  {'X': 3,
   'Y': 3,
   'Z': 8 })

cost = {
  ('A', 'X'): 8, ('A', 'Y'): 6, ('A', 'Z'): 10,
  ('B', 'X'): 3, ('B', 'Y'): 1, ('B', 'Z'): 8,
  ('C', 'X'): 1, ('C', 'Y'): 8, ('C', 'Z'): 5,
  ('D', 'X'): 6, ('D', 'Y'): 2, ('D', 'Z'): 6 }

# create empty model
m = gp.Model()

ship = defaultdict(dict)
# add decision variables
for w in warehouses:
    for c in centers:
        ship[w][c] = m.addVar(vtype=gp.GRB.INTEGER)

# process pending changes
m.update()

# set objective function
m.setObjective(gp.quicksum([ship[w][c] * cost[(w, c)]
                            for (w, c) in cost]), gp.GRB.MINIMIZE)

# add constraints
for c in centers:
    m.addConstr(gp.quicksum([ship[w][c] for w in warehouses]) == demand[c])

for w in warehouses:
    m.addConstr(gp.quicksum(ship[w][c] for c in centers) <= capacity[w])

for v in ship.values():
    for v_ in v.values():
        m.addConstr(v_ >= 0)

# solve model
m.optimize()

# display solution
if m.SolCount > 0:
  m.printAttr('X')

# export model
m.write('transport.lp')

