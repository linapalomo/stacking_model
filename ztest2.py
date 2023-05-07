#ESS benefits model
##WORKING COMPLETE
#this model will optimise the land use distribution costs with the restriction that the ESS (benefits in the code)
# will stay the same amount or it will increase. Not net loss.
import json
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, LpBinary
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data from JSON file
with open("dataz.json", "r") as infile:
    data = json.load(infile)

costs = data["costs"]
initial_landuse_types = data["initial_landuse_types"]
#benefit1 = data["benefitLU1"]
#benefit2= data["benefitLU2"]
benefit1_values = data["benefit1_values"]
benefit2_values = data["benefit2_values"]

n_parcels = len(costs)
n_landuse_types = len(costs[0])

#print land use distribution
def plot_landuse_grid(landuse_types, title):
    landuse_grid = np.array(landuse_types).reshape(2, 5)
    
    sns.heatmap(landuse_grid, annot=True, cmap="coolwarm", cbar=False, xticklabels=False, yticklabels=False, square=True, linewidths=1, linecolor='black', fmt="d")
    plt.title(title)
    plt.show()


# Optimization problem
problem = LpProblem("Minimize Total Costs", LpMinimize)

# Decision variables
x = [[LpVariable(f"x_{i}_{j}", cat=LpBinary) for j in range(n_landuse_types)] for i in range(n_parcels)]

# Objective function
problem += lpSum(x[i][j] * costs[i][j] for i in range(n_parcels) for j in range(n_landuse_types))


#initial_benefit1_total = sum(benefit1_values[i][j] for i in range(n_parcels) for j in range(n_landuse_types))
#initial_benefit2_total = sum(benefit2_values[i][j] for i in range(n_parcels) for j in range(n_landuse_types))



# Constraints
for i in range(n_parcels):
    problem += lpSum(x[i][j] for j in range(n_landuse_types)) == 1
    
# i think is finally working this one
initial_total_benefit1 = sum(benefit1_values[i][initial_landuse_types[i]] for i in range(n_parcels))
initial_total_benefit2 = sum(benefit2_values[i][initial_landuse_types[i]] for i in range(n_parcels))

problem += lpSum(x[i][j] * benefit1_values[i][j] for i in range(n_parcels) for j in range(n_landuse_types)) >= initial_total_benefit1
problem += lpSum(x[i][j] * benefit2_values[i][j] for i in range(n_parcels) for j in range(n_landuse_types)) >= initial_total_benefit2


'''# Calculate the initial benefit1 and benefit2 totals for each landuse
initial_benefit1_totals = [sum(benefit1_values[i][j] for i in range(n_parcels) if initial_landuse_types[i] == j) for j in range(n_landuse_types)]
initial_benefit2_totals = [sum(benefit2_values[i][j] for i in range(n_parcels) if initial_landuse_types[i] == j) for j in range(n_landuse_types)]

for j in range(n_landuse_types):

    problem += lpSum(x[i][j] * benefit1_values[i][j] for i in range(n_parcels)) >= initial_benefit1_totals[j]
    problem += lpSum(x[i][j] * benefit2_values[i][j] for i in range(n_parcels)) >= initial_benefit2_totals[j]
'''

#problem += lpSum(x[i][j] * benefit1_values[i][j] for i in range(n_parcels) for j in range(n_landuse_types)) >= initial_benefit1_total
#problem += lpSum(x[i][j] * benefit2_values[i][j] for i in range(n_parcels) for j in range(n_landuse_types)) >= initial_benefit2_total

'''
for j in range(n_landuse_types):
    problem += (
        lpSum(x[i][j] * benefit1_values[i][j] for i in range(n_parcels)) +
        lpSum(x[i][j] * benefit2_values[i][j] for i in range(n_parcels))
    ) >= sum(
        benefit1_values[i][j] + benefit2_values[i][j]
        for i in range(n_parcels) if initial_landuse_types[i] == j)
    '''
    
    #for j in range(n_product_types):
    # Marketing 1 constraint
    #problem += lpSum(x[i][j] * marketing1_values[i][j] for i in range(n_locations)) >= sum(
    #    marketing1_values[i][j] for i in range(n_locations) if initial_product_types[i] == j)

    # Marketing 2 constraint
   # problem += lpSum(x[i][j] * marketing2_values[i][j] for i in range(n_locations)) >= sum(
    #    marketing2_values[i][j] for i in range(n_locations) if initial_product_types[i] == j)

    
#for i in range(n_parcels):
  #   problem += lpSum(x[i][j] * benefit1_values[i][j] for i in n_parcels for j in n_landuse_types) >= sum(
   #     benefit1_values[i][j] for i in n_parcels if initial_landuse_types[i] == j)
    # problem += lpSum(x[i][j] * benefit2_values[i][j] for i in n_parcels for j in n_landuse_types) >= sum(
     #    benefit2_values[i][j] for i in n_parcels if initial_landuse_types[i] == j)



problem.solve()

if LpStatus[problem.status] == "Optimal":
    # Get optimized land Use
    optimized_landuse_types = []
    for i in range(n_parcels):
        for j in range(n_landuse_types):
            if x[i][j].varValue == 1:
                optimized_landuse_types.append(j)

    print("Optimized Land Use:", optimized_landuse_types)
    print("Initial total costs:", sum(np.choose(initial_landuse_types, np.array(costs).T)))
    print("Optimized total costs:", sum(np.choose(optimized_landuse_types, np.array(costs).T)))


    # Calculate the total of benefit1 and benefit2 for initial and optimized distributions
    initial_total_benefit1 = [sum(benefit1_values[i][j] for i in range(n_parcels) if initial_landuse_types[i] == j) for j in range(n_landuse_types)]
    initial_total_benefit2 = [sum(benefit2_values[i][j] for i in range(n_parcels) if initial_landuse_types[i] == j) for j in range(n_landuse_types)]
    optimized_total_benefit1 = [sum(x[i][j].varValue * benefit1_values[i][j] for i in range(n_parcels)) for j in range(n_landuse_types)]
    optimized_total_benefit2 = [sum(x[i][j].varValue * benefit2_values[i][j] for i in range(n_parcels)) for j in range(n_landuse_types)]

    print("Initial total benefit1/ES1:", sum(initial_total_benefit1))
    print("Optimized total benefit1/ES1:", sum(optimized_total_benefit1))
    print("Initial total Benefit2/ES2:", sum(initial_total_benefit2))
    print("Optimized total benefit2/ES2:", sum(optimized_total_benefit2))
    


else:
    print("Sad!. The optimization problem is infeasible.")
    
plot_landuse_grid(optimized_landuse_types, 'Optimized Land Use Distribution with no ESS loss')