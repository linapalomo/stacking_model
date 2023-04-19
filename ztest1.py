#landuse model
#this model will optimise the landuse distribution keeping the original land use values
####WORKING COMPLETE    ###
import json
import numpy as np
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum
import matplotlib.pyplot as plt
import seaborn as sns

# Load initial data
with open("dataz.json", "r") as f:
    data = json.load(f)

n_parcels = 4
n_landuse_types = 3

initial_landuse_types = data["initial_landuse_types"]
costs = np.array(data["costs"])
benefit1_values = np.array(data["benefit1_values"])
benefit2_values = np.array(data["benefit2_values"])


#printing a plot with the initial lnd use distribution for visual comparison
def plot_landuse_grid(landuse_types, title):
    landuse_grid = np.array(landuse_types).reshape(2, 2)
    
    sns.heatmap(landuse_grid, annot=True, cmap="coolwarm", cbar=False, xticklabels=False, yticklabels=False, square=True, linewidths=1, linecolor='black', fmt="d")
    plt.title(title)
    plt.show()

    
plot_landuse_grid(initial_landuse_types, 'Initial Land Use Distribution')

# Linear programming problem
problem = LpProblem("Landuse_Optimization", LpMinimize)

# Decision variables
x = [[LpVariable(f"x_{i}_{j}", 0, 1, cat="Integer") for j in range(n_landuse_types)] for i in range(n_parcels)]

# Objective function
problem += lpSum(x[i][j] * costs[i][j] for i in range(n_parcels) for j in range(n_landuse_types))

# Constraints
for i in range(n_parcels):
    problem += lpSum(x[i][j] for j in range(n_landuse_types)) == 1

for j in range(n_landuse_types):
    problem += lpSum(x[i][j] for i in range(n_parcels)) == initial_landuse_types.count(j)

# Solve the linear programming problem
problem.solve()

if LpStatus[problem.status] == "Optimal":
    # Get optimized Land Use:
    optimized_landuse_types = []
    for i in range(n_parcels):
        for j in range(n_landuse_types):
            if x[i][j].varValue == 1:
                optimized_landuse_types.append(j)

    print("Optimized Land Use distribution:", optimized_landuse_types)
    print("Initial total costs:", sum(np.choose(initial_landuse_types, costs.T)))
    print("Optimized total costs:", sum(np.choose(optimized_landuse_types, costs.T)))
    print("Optimized total ESS1:", sum(np.choose(optimized_landuse_types, benefit1_values.T)))
    print("Optimized total ESS2:", sum(np.choose(optimized_landuse_types, benefit2_values.T)))



else:
    print("Sad! The optimization problem is infeasible.")
    
plot_landuse_grid(optimized_landuse_types, 'Optimized Land Use Distribution with no Land Use loss')