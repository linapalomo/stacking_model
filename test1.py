#new optimization
import json
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, LpBinary
import numpy as np

# Load data from JSON file
with open("data.json", "r") as infile:
    data = json.load(infile)

costs = data["costs"]
initial_product_types = data["initial_product_types"]
tmarketing = data["tmarketing"]
marketing1_values = data["marketing1_values"]
marketing2_values = data["marketing2_values"]

n_locations = len(costs)
n_product_types = len(costs[0])

# Create optimization problem
problem = LpProblem("Minimize Total Costs", LpMinimize)

# Define decision variables
x = [[LpVariable(f"x_{i}_{j}", cat=LpBinary) for j in range(n_product_types)] for i in range(n_locations)]

# Add constraints
for i in range(n_locations):
    problem += lpSum(x[i][j] for j in range(n_product_types)) == 1

for j in range(n_product_types):
    problem += lpSum(x[i][j] * marketing1_values[i][j] for i in range(n_locations)) >= sum(
        marketing1_values[i][j] for i in range(n_locations) if initial_product_types[i] == j)
    problem += lpSum(x[i][j] * marketing2_values[i][j] for i in range(n_locations)) >= sum(
        marketing2_values[i][j] for i in range(n_locations) if initial_product_types[i] == j)

# Define objective function
problem += lpSum(x[i][j] * costs[i][j] for i in range(n_locations) for j in range(n_product_types))

# Solve the problem
problem.solve()

if LpStatus[problem.status] == "Optimal":
    # Get optimized product types
    optimized_product_types = []
    for i in range(n_locations):
        for j in range(n_product_types):
            if x[i][j].varValue == 1:
                optimized_product_types.append(j)

    print("Optimized product types:", optimized_product_types)
    print("Initial total costs:", sum(np.choose(initial_product_types, np.array(costs).T)))
    print("Optimized total costs:", sum(np.choose(optimized_product_types, np.array(costs).T)))


    # Calculate the total of marketing1 and marketing2 for initial and optimized distributions
    initial_total_marketing1 = [sum(marketing1_values[i][j] for i in range(n_locations) if initial_product_types[i] == j) for j in range(n_product_types)]
    initial_total_marketing2 = [sum(marketing2_values[i][j] for i in range(n_locations) if initial_product_types[i] == j) for j in range(n_product_types)]
    optimized_total_marketing1 = [sum(x[i][j].varValue * marketing1_values[i][j] for i in range(n_locations)) for j in range(n_product_types)]
    optimized_total_marketing2 = [sum(x[i][j].varValue * marketing2_values[i][j] for i in range(n_locations)) for j in range(n_product_types)]

    print("Initial total marketing1:", initial_total_marketing1)
    print("Optimized total marketing1:", optimized_total_marketing1)
    print("Initial total marketing2:", initial_total_marketing2)
    print("Optimized total marketing2:", optimized_total_marketing2)

else:
    print("The optimization problem is infeasible.")
