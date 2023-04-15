#landuse model

import json
import numpy as np
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum

# Load initial data
with open("data.json", "r") as f:
    data = json.load(f)

n_locations = 10
n_product_types = 3

initial_product_types = data["initial_product_types"]
costs = np.array(data["costs"])

# Create a linear programming problem
problem = LpProblem("Product_Type_Optimization", LpMinimize)

# Define decision variables
x = [[LpVariable(f"x_{i}_{j}", 0, 1, cat="Integer") for j in range(n_product_types)] for i in range(n_locations)]

# Define objective function
problem += lpSum(x[i][j] * costs[i][j] for i in range(n_locations) for j in range(n_product_types))

# Define constraints
for i in range(n_locations):
    problem += lpSum(x[i][j] for j in range(n_product_types)) == 1

for j in range(n_product_types):
    problem += lpSum(x[i][j] for i in range(n_locations)) == initial_product_types.count(j)

# Solve the linear programming problem
problem.solve()

if LpStatus[problem.status] == "Optimal":
    # Get optimized product types
    optimized_product_types = []
    for i in range(n_locations):
        for j in range(n_product_types):
            if x[i][j].varValue == 1:
                optimized_product_types.append(j)

    print("Optimized product types:", optimized_product_types)
    print("Initial total costs:", sum(np.choose(initial_product_types, costs.T)))
    print("Optimized total costs:", sum(np.choose(optimized_product_types, costs.T)))

else:
    print("The optimization problem is infeasible.")
