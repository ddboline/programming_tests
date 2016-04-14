# import gurobipy module
import gurobipy as gp

# create empty model
m = gp.Model()

# change model name attribute
m.ModelName = 'My Second Model'

x = m.addVar(vtype=gp.GRB.BINARY, name='x')
y = m.addVar(vtype=gp.GRB.BINARY, name='y')
z = m.addVar(vtype=gp.GRB.BINARY, name='z')

m.setObjective(x+y+2*z, gp.GRB.MAXIMIZE)

m.addConstr(x+2*y+3*z <= 4, name='c0')
m.addConstr(x+y >= 1, name='c1')

# process the pending change
m.update()

# export model to file
m.write('MyModel.mps')

m.optimize()

# print to console
# print 'This program creates an empty model named:', m.Modelname
# print 'Model exported to file named: MyModel.mps'

