import json
import pulp
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#landuse model WORKING-----

# Load the data from the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)
    
costs = np.array(data['costs'])
initial_landuse_types = data['initial_landuse_types']
benefits = np.array(data['benefits'])
benefit1 = np.array(data['benefit1'])
benefit2 = np.array(data['benefit2'])

def plot_landuse_grid(landuse_types, title):
    landuse_grid = np.array(landuse_types).reshape(2, 5)
    
    sns.heatmap(landuse_grid, annot=True, cmap="coolwarm", cbar=False, xticklabels=False, yticklabels=False, square=True, linewidths=1, linecolor='black', fmt="d")
    plt.title(title)
    plt.show()

    
plot_landuse_grid(initial_landuse_types, 'Initial Land Use Distribution')

# Define the linear programming problem to minimize the total costs of the landscape
problem = pulp.LpProblem("Minimize_Total_Costs", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", (range(10), range(3)), cat='Binary')

# Define the objective function
problem += pulp.lpSum([costs[i][j-1] * x[i][j] for i in range(10) for j in range(3)])

# Define constraints
for i in range(10):
    problem += pulp.lpSum([x[i][j] for j in range(3)]) == 1

# Add constraint to maintain the same number of each land use
landuse_type_counts = {j: initial_landuse_types.count(j) for j in range(3)}
for j in range(3):
    problem += pulp.lpSum([x[i][j] for i in range(10)]) == landuse_type_counts[j]

# Solve the optimization problem
problem.solve()

# Print optimized land use types for each parcel
print("Optimized Parcels and landuse:")
for i in range(10):
    for j in range(3):
        if x[i][j].varValue == 1:
            print(f"Parcel {i+1}: Assigned landuse : LU{j}")
            
            
# Calculate optimized  land use
optimized_landuse_types = [0] * 10
for i in range(10):
    for j in range(3):
        if x[i][j].varValue == 1:
            optimized_landuse_types[i] = j
            
# Calculate the total benefit1 and benefit2 values after optimization
optimized_total_benefit1 = sum(benefit1[i][product_type] for i, product_type in enumerate(optimized_landuse_types))
optimized_total_benefit2 = sum(benefit2[i][product_type] for i, product_type in enumerate(optimized_landuse_types))
print(f"Optimized total benefit1: {optimized_total_benefit1}")
print(f"Optimized total benefit2: {optimized_total_benefit2}")

plot_landuse_grid(optimized_landuse_types, 'Optimized Land Use Distribution')