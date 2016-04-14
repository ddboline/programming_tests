import gurobipy as gp

# define data coefficients
n = 7
p = [6, 5, 8, 9, 6, 7, 3]
w = [2, 3, 6, 7, 5, 9, 4]
c = 9

# create empty model
m = gp.Model()

x = []

# add decision variables
for idx in range(7):
    x.append(m.addVar(name='x%d' % idx, vtype=gp.GRB.BINARY))

# process pending changes
m.update()

# set objective function
m.setObjective(gp.quicksum([x[i] * p[i] for i in range(len(x))]),
               gp.GRB.MAXIMIZE)

# add constraint
m.addConstr(gp.quicksum([x[i] * w[i] for i in range(len(x))]) <= c)

# solve model
m.optimize()

# display solution
if m.SolCount > 0:
  m.printAttr('X')

# export model
m.write('knapsack.lp')

