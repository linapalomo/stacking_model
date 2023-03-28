import pandas as pd
from pulp import *

# Load the data into a pandas DataFrame
data = {
    'Kid': ['A', 'B', 'C'],
    'costs': [1.009000, 3.302078, 7.795149],
    'requer1': [0.000000, 5.212786, 4.595318],
    'requer2': [0.000000, 3.475191, 1.148830],
    'count': [36, 44, 20]
}
df = pd.DataFrame(data)

# Create a pulp LpProblem
prob = LpProblem("Optimization Problem", LpMinimize)

# Define the decision variables
xA = LpVariable("xA", lowBound=0, cat='Integer')
xB = LpVariable("xB", lowBound=0, cat='Integer')
xC = LpVariable("xC", lowBound=0, cat='Integer')

# Define the objective function
prob += df['costs'][0]*xA + df['costs'][1]*xB + df['costs'][2]*xC, "Total Cost"

# Define the constraints
prob += xA + xB + xC <= 100, "Total Number of Students Constraint"
prob += df['requer1'][0]*xA + df['requer1'][1]*xB + df['requer1'][2]*xC >= df['count'][0]*df['requer1'][0] + df['count'][1]*df['requer1'][1] + df['count'][2]*df['requer1'][2], "Requer1 Constraint"
prob += df['requer2'][0]*xA + df['requer2'][1]*xB + df['requer2'][2]*xC >= df['count'][0]*df['requer2'][0] + df['count'][1]*df['requer2'][1] + df['count'][2]*df['requer2'][2], "Requer2 Constraint"

# Solve the problem
prob.solve()

# Print the optimal solution
print("Optimal Solution:")
print("x_A = {}".format(int(xA.value())))
print("x_B = {}".format(int(xB.value())))
print("x_C = {}".format(int(xC.value())))
print("Total Cost = ${:.2f}".format(value(prob.objective)))
