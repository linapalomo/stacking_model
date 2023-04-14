import random
import pulp
import numpy as np

# Generate random costs for p1 and p2, and set p3 cost to 0
costs = np.random.normal(20, 4, size=(10, 2))
costs = np.hstack((costs, np.zeros((10, 1))))

# Randomly assign initial product types to each location
initial_product_types = [random.randint(1, 3) for _ in range(10)]

# Count the number of each product type in the initial assignment
product_type_counts = {j: initial_product_types.count(j) for j in range(1, 4)}
  

# Print current locations, costs, and product types
print("Initial Locations, Costs, and Product Types:")
initial_total_cost = 0
for i, (cost, product_type) in enumerate(zip(costs, initial_product_types)):
    initial_cost = cost[product_type - 1]
    initial_total_cost += initial_cost
    print(f"Location {i+1}: Costs (p1, p2, p3) = {tuple(cost)}, Initial Product Type: p{product_type}, Cost: {initial_cost}")

print(f"Initial total cost: {initial_total_cost}")


# Define the linear programming problem
problem = pulp.LpProblem("Minimize_Total_Costs", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", (range(10), range(1, 4)), cat='Binary')

# Define the objective function
problem += pulp.lpSum([costs[i][j-1] * x[i][j] for i in range(10) for j in range(1, 4)])

# Define constraints
for i in range(10):
    problem += pulp.lpSum([x[i][j] for j in range(1, 4)]) == 1

# Add constraint to maintain the same number of each product type
for j in range(1, 4):
    problem += pulp.lpSum([x[i][j] for i in range(10)]) == product_type_counts[j]

# Solve the optimization problem
problem.solve()

# Print optimized product types for each location
print("\nOptimized Locations and Product Types:")
for i in range(10):
    for j in range(1, 4):
        if x[i][j].varValue == 1:
            print(f"Location {i+1}: Assigned Product Type: p{j}")
