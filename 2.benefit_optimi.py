import json
import pulp
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#benefit model

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
problem = pulp.LpProblem("Minimize_Total_Costs_ben", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", (range(10), range(3)), cat='Binary')


# Set the objective function
problem += pulp.lpSum(costs[i][j] * x[i][j] for i in range(10) for j in range(3))

# Add constraints
for i in range(10):
    problem += pulp.lpSum(x[i][j] for j in range(3)) == 1

# Define tolerance value
tol = 0.1 * (benefit1.sum() + benefit2.sum())


initial_total_benefit1 = benefit1.sum()
initial_total_benefit2 = benefit2.sum()
problem += pulp.lpSum(benefit1[i][j] * x[i][j] for i in range(10) for j in range (3)) + pulp.lpSum(benefit2[i][j] * x[i][j] for i in range(10) for j in range(1, 3)) >= benefit1.sum() + benefit2.sum() - tol

# Solve the optimization problem
problem.solve()

# Print results
print("Status:", pulp.LpStatus[problem.status])

optimized_landuse_types = []
for i in range(10):
    for j in range(3):
        if x[i][j].varValue == 1:
            optimized_landuse_types.append(j)

print("Optimized Land Use Distribution:", optimized_landuse_types)
