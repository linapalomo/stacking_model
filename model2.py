import random
import json
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import minimize


###COSTS###
##Import data from the Costs model
with open('costs.json', 'r') as f:
    cost_data = json.load(f)

lu0_cost = cost_data['Costs LU0']
lu1_cost = cost_data['Costs LU1']
lu2_cost = cost_data['Costs LU2']


###BENEFITS###
#Import data from the benefits model
with open('benefits.json', 'r') as f:
    benefits_data = json.load(f)

lu0_benefit1 = benefits_data['b1_lu0']
lu0_benefit2 = benefits_data['b2_lu0']
lu1_benefit1 = benefits_data['b1_lu1']
lu1_benefit2 = benefits_data['b2_lu1']
lu2_benefit1 = benefits_data['b1_lu2']
lu2_benefit2 = benefits_data['b2_lu2']

## Generate the landscapes and save them in a json file
lu0 = {'type_id':0, "cost": lu0_cost, "b1": lu0_benefit1, "b2": lu0_benefit2}
lu1 = {'type_id':1,"cost": lu1_cost, "b1": lu1_benefit1, "b2": lu1_benefit2}
lu2 = {'type_id':2,"cost": lu2_cost, "b1": lu2_benefit1, "b2": lu2_benefit2}

landscape = [lu0, lu1, lu2]

filename = "landscape.json"

with open(filename, "w") as f:
    json.dump(landscape, f, indent=4)

print("Landscape data saved to", filename)
counter = 1
# Timestamp to keep track of different versions of the landscape
timestamp = int(time.time())

filename = f'landscape_{counter}.json'
with open(filename, "w") as f:
    json.dump(landscape, f)
    
counter += 1
time.sleep(1) #CHANGE EVRY RUN TO SAVE LANDSCAPES

print("Landscape data saved to", filename)

# Total number of land parcels =200

parcel_numbers = list(range(200))

LU_prob = np.random.dirichlet(np.ones(3), size=1).tolist()[0]
LU0, LU1, LU2 = [int(prob * 100) for prob in LU_prob]


n_plots = 200
LU0_parcels = int(n_plots * LU0 / 100)
LU1_parcels = int(n_plots * LU1 / 100)
LU2_parcels = int(n_plots * LU2 / 100)


LU_distribution = {
    "LU0": LU0_parcels,
    "LU1": LU1_parcels,
    "LU2": LU2_parcels
}

with open("LU_distribution.json", "w") as f:
    json.dump(LU_distribution, f)

print("LU0: ", LU0_parcels)
print("LU1: ", LU1_parcels)
print("LU2: ", LU2_parcels)
print("Distribution saved in LU_distribution file")
print("SAVE IT")

#obtain the total benefits in the land distribution

# Load the JSON file
with open('landscape.json', 'r') as f:
    data_lu = json.load(f)

# Extract the list of LU types
LU_types = [d['type_id'] for d in data_lu]

# Convert the list of LU types to a NumPy array
LU_costs = np.array([d['cost'] for d in data_lu])
LU_services = np.array([[d['b1'], d['b2']] for d in data_lu])

def calculate_costs_and_services(parcels, lu_types):
    # Convert the parcels list to a NumPy array
    num_parcels = np.array(parcels)

    # Calculate the total costs of the parcels
    total_costs = np.sum(num_parcels * lu_types['cost'])

    # Calculate the minimum service level for each service
    benefits_total = np.zeros(2)
    for i in range(2):
        benefits_total[i] = np.min(lu_types['b{}'.format(i+1)][:, i], axis=0).dot(num_parcels)

    # Calculate the total service level
    total_benefits = np.sum(benefits_total)

    return total_costs, total_benefits

# Load the LU types from a JSON file
with open('landscape.json', 'r') as f:
    data_lu = json.load(f)
    LU_types = data_lu[2]


# Compute the total costs and services of the parcel distribution
total_costs, total_services = calculate_costs_and_services(LU_distribution, LU_types)

# Print the total costs and services
print("Total costs: ${:.2f}".format(total_costs))
print("Total service level: {:.2f}".format(total_services))






total_benefit1_LU1= LU1_parcels * lu1_benefit1
total_benefit1_LU2= LU2_parcels * lu2_benefit1
total_benefit1 = total_benefit1_LU1 + total_benefit1_LU2
print("Total benefits 1:", total_benefit1)


total_benefit2_LU1= LU1_parcels * lu1_benefit2
total_benefit2_LU2= LU2_parcels * lu2_benefit2
total_benefit2 = total_benefit2_LU1 + total_benefit2_LU2
print("Total benefits 2:", total_benefit2)

#save total benefits in a dictionary
total_benefits = {
    "total_benefit_1":total_benefit1,
    "total_benefit_2":total_benefit2
}

# Save the benefits in a JSON file
with open('total_benefits.json', 'w') as f:
    json.dump(total_benefits, f)

print("total benefits are saved in total_benefits.json")



# Constraints on B1 and B2
B1_constraint = (total_benefit1, None)
B2_constraint = (total_benefit2, None)

# Define the objective function
def objective(x):
    B1 = x[0]
    B2 = x[1]
    costs = 0
    for i in range(LU0_parcels):
        costs += lu0_cost + lu0_benefit1 + lu0_benefit2
    for i in range(LU1_parcels):
        costs += lu1_cost + B1 * lu1_benefit1 + B2 * lu1_benefit2
    for i in range(LU2_parcels):
        costs += lu2_cost + B1 * lu2_benefit1 + B2 * lu2_benefit2
    return costs

# Define the constraints
cons = ({'type': 'ineq', 'fun': lambda x: x[1] - total_benefit1},
        {'type': 'ineq', 'fun': lambda x: total_benefit2 - x[0]})

# Minimize the objective function subject to the constraints
x0 = [0, 0]
res = minimize(objective, x0, method='SLSQP', constraints=cons)

print("Number of LU0 parcels: ", LU0_parcels)
print("Number of LU1 parcels: ", LU1_parcels)
print("Number of LU2 parcels: ", LU2_parcels)
print("Optimal value of objective function:", res.fun)
print("Optimal values of variables:", res.x)

# Calculate the optimal number of land use per type
n_opt_LU0 = int(round(res.x[0]))
n_opt_LU1 = int(round(res.x[1]*7))
n_opt_LU2 = int(round(res.x[1]*5))

# Print the optimal number of land use per type
print("Optimal number of LU0 parcels: ", n_opt_LU0)
print("Optimal number of LU1 parcels: ", n_opt_LU1)
print("Optimal number of LU2 parcels: ", n_opt_LU2)


if res.success:
    print("The optimization was successful!")
    print("Optimal values: B1 = {0:.2f}, B2 = {1:.2f}".format(res.x[0], res.x[1]))
    
    
else:
    print("The optimization failed, take a look to the input data.")



'''

###generate the random distribution of parcels 
total_plots = 100
land_uses = [lu0, lu1, lu2]

distribution = [random.choice(land_uses) for _ in range(total_plots)]

filename = "distribution.json"

with open(filename, "w") as f:
    json.dump(distribution, f, indent=4)

print("Land use distribution saved to", filename)

# Timestamp to keep track of different versions of the distribution
timestamp = int(time.time())

filename = "distribution_{}.json".format(timestamp)

with open(filename, "w") as f:
    json.dump(distribution, f, indent=4)

print("Land use distribution saved to", filename)


# Load the distribution data from the JSON file
with open("distribution.json", "r") as f:
    distribution = json.load(f)

# Create a 2D array with the same number of rows and columns as the number of plots
grid = np.array(distribution).reshape(10, 10)

# Plot the grid using matplotlib's imshow function
plt.imshow(grid, cmap="hot")

# Add a colorbar to the plot
plt.colorbar()

# Add a title to the plot
plt.title("Plot Distribution")

# Show the plot
plt.show()

'''





