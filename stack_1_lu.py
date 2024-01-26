#Offsetting scheme with fixed land use trading
#Code to simulate the offsetting schem with fixed land use trading.
#this model will optimise the landuse distribution keeping the original land use values.
####WORKING COMPLETE    ###
import json
import numpy as np
from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum
from collections import Counter

# Load initial data
with open("dataz.json", "r") as f:
    data = json.load(f)

n_parcels = 48
n_landuse_types = 3

initial_landuse_types = data["initial_landuse_types"]
costs = np.array(data["costs"])
benefit1_values = np.array(data["benefit1_values"])
benefit2_values = np.array(data["benefit2_values"])


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
    print('initial land use distributiion:', initial_landuse_types)
    print("Optimized Land Use distribution with LU restrictions:", optimized_landuse_types)
    print("Initial total costs:", sum(np.choose(initial_landuse_types, costs.T)))
    print("Optimized total costs:", sum(np.choose(optimized_landuse_types, costs.T)))
    print("Optimized total ES1:", sum(np.choose(optimized_landuse_types, benefit1_values.T)))
    print("Optimized total ES2:", sum(np.choose(optimized_landuse_types, benefit2_values.T)))
    counter = Counter(optimized_landuse_types)
    countlu0 = counter[0]
    countlu1 = counter[1]
    countlu2 = counter[2]
    print("total LU0:",countlu0)  
    print("total LU1:",countlu1) 
    print("total LU2:",countlu2)
    
else:
    print("Sad! The optimization problem is infeasible.")
    

