##MODELO LANDUSE###

import pulp
from pulp import *
import json

# Define the problem
prob = LpProblem("Landuse in Regions Allocation Problem", LpMinimize)

# Define the decision variables
landuse = ["LU0", "LU1", "LU2"]
regions = ["R1", "R2", "R3"]

#bring the costs from the costs model:
with open('costs.json', 'r') as f:
    cost_data = json.load(f)

lu0_cost = cost_data['Costs LU0']
lu1_cost = cost_data['Costs LU1']
lu2_cost = cost_data['Costs LU2']

# Define the landuse costs
landuse_costs = {"LU0": lu0_cost, "LU1": lu1_cost, "LU2": lu2_cost}

# Define the maximum capacity for each region
capacity = {"R1": 39, "R2": 48, "R3": 13}

# Define the conservation/additional costs for each landuse and region
#do i need to generate the numbers from normal distributions?
additional_costs = {"LU0": {"R1": 2, "R2": -1, "R3": 1},
                 "LU1": {"R1": 2, "R2": -1, "R3": 1},
                 "LU2": {"R1": 2, "R2": -1, "R3": 1}}

#bring the current distribution of land uses from the landscape model:
with open('LU_distribution.json', 'r') as f:
    count_data = json.load(f)

lu0_count = count_data['LU0']
lu1_count = count_data['LU1']
lu2_count = count_data['LU2']

# Define the current number each landuse
landscape = {"LU0": lu0_count, "LU1": lu1_count, "LU2": lu2_count}

# Create the decision variable x[i][j]
x = LpVariable.dicts("x", [(i, j) for i in landuse for j in regions], lowBound=0, cat='Integer')

# Define the objective function
prob += lpSum([additional_costs[i][j] * x[(i, j)] for i in landuse for j in regions]) + lpSum([landuse_costs[i] * x[(i, j)] for i in landuse for j in regions])


# Define the constraints
for i in landuse:
    prob += lpSum([x[(i, j)] for j in regions]) == landscape[i]
for j in regions:
    prob += lpSum([x[(i, j)] for i in landuse]) <= capacity[j]

# Solve the problem
prob.solve()
#solver = pulp.GLPK_CMD()   # Replace CPLEX_PY with the solver of your choice (e.g., COIN_CMD, GUROBI, GLPK, etc.)
#pulp.pulpTestAll()  # Test the availability of the solver
#pulp.LpSolverDefault = solver  # Set the solver as the default solver for PuLP

# Print the results
for i in landuse:
    for j in regions:
        print("Allocating %s to %s: %d units" % (i, j, x[(i, j)].varValue))
print("Total Cost = ", value(prob.objective))



#solver = pulp.COIN_CMD()  # Replace CPLEX_PY with the solver of your choice (e.g., COIN_CMD, GUROBI, GLPK, etc.)
#pulp.pulpTestAll()  # Test the availability of the solver
#pulp.LpSolverDefault = solver  # Set the solver as the default solver for PuLP
