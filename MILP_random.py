import numpy as np
import matplotlib.pyplot as plt
import random
import json
import pandas as pd
from scipy.optimize import minimize

# Initial costs for each parcel
costs0 = 0
costs1 = 1.5
costs2 = 2.5

# Constraints on B1 and B2
B1_constraint = (500, None)
B2_constraint = (700, None)

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

# randomly assign land use to each parcel
land_use = []
for i in range(200):
    rand_num = random.randint(0, 2)
    if rand_num == 0:
        land_use.append("LU0")
    elif rand_num == 1:
        land_use.append("LU1")
    else:
        land_use.append("LU2")

# create a pandas Series from the land_use list
land_use_series = pd.Series(land_use)

# use value_counts() to get a summary of each land use type
land_use_summary = land_use_series.value_counts()

# print the summary
print(land_use_summary)

# create a dictionary to store the land use of each parcel
parcel_dict = {}
for i in range(200):
    parcel_dict[parcel_numbers[i]] = land_use[i]

print("Parcel number and land use:")
for i in parcel_dict.keys():
    print("Parcel number:", i, "Land use:", parcel_dict[i])    

# Generate random locations for each type of parcel
locations_LU0 = np.zeros((LU0_parcels, 2))
locations_LU1 = np.zeros((LU1_parcels, 2))
locations_LU2 = np.zeros((LU2_parcels, 2))

for i in range(LU0_parcels):
    locations_LU0[i, 0] = random.randint(0, 9)
    locations_LU0[i, 1] = random.randint(0, 9)
for i in range(LU1_parcels):
    locations_LU1[i, 0] = random.randint(0, 9)
    locations_LU1[i, 1] = random.randint(0, 9)
for i in range(LU2_parcels):
    locations_LU2[i, 0] = random.randint(0, 9)
    locations_LU2[i, 1] = random.randint(0, 9)


# Define the objective function
def objective(x):
    B1 = x[0]
    B2 = x[1]
    costs = 0
    for i in range(LU0_parcels):
        costs += 0
    for i in range(LU1_parcels):
        costs += 1.5 + B1 * 7 + B2 * 3
    for i in range(LU2_parcels):
        costs += 2.5 + B1 * 5 + B2 * 5
    return costs

# Define the constraints
cons = ({'type': 'ineq', 'fun': lambda x: x[1] - 500},
        {'type': 'ineq', 'fun': lambda x: 700 - x[0]})

# Minimize the objective function subject to the constraints
x0 = [0, 0]
res = minimize(objective, x0, method='SLSQP', constraints=cons)

print("Number of LU0 parcels: ", LU0_parcels)
print("Number of LU1 parcels: ", LU1_parcels)
print("Number of LU2 parcels: ", LU2_parcels)
print("Optimal value of objective function:", res.fun)
print("Optimal values of variables:", res.x)

if res.success:
    print("The optimization was successful!")
    print("Optimal values: B1 = {0:.2f}, B2 = {1:.2f}".format(res.x[0], res.x[1]))
  
    
else:
    print("The optimization failed, take a look to the input data.")



# Plot the locations of the land parcels
grid = np.zeros((10, 10))
for i in range(LU0_parcels):
    grid[int(locations_LU0[i, 0]), int(locations_LU0[i, 1])] = 0 #blue colour
for i in range(LU1_parcels):
    grid[int(locations_LU1[i, 0]), int(locations_LU1[i, 1])] = 1 #green colour 
for i in range(LU2_parcels):
    grid[int(locations_LU2[i, 0]), int(locations_LU2[i, 1])] = 2 #red colour

'''plt.imshow(grid, cmap='jet')
plt.xlabel("X")
plt.ylabel("Y")
plt.colorbar()
plt.title("Land Distribution")
plt.show()'''

fig, ax = plt.subplots()
cax = ax.imshow(grid, cmap='jet')

ax.set_xlabel("X")
ax.set_ylabel("Y")

# Set the title of the plot
ax.set_title("Land Distribution")

# Add colorbar to show the land use type
cbar = fig.colorbar(cax, ticks=[0, 1, 2], orientation='horizontal')
cbar.ax.set_xticklabels(['LU0', 'LU1', 'LU2'])
plt.show()

#

################################################################
'''
# Initial costs for each parcel
costs0 = 0
costs1 = 1.5
costs2 = 2.5

# Constraints on B1 and B2
B1_constraint = (300, None)
B2_constraint = (200, None)

# Total number of land parcels
total_parcels = 100

# Number of each type of parcel
n0 = 36
n1 = 42
n2 = 22

# Generate random locations for each type of parcel
locations0 = np.array([[random.randint(0, 100), random.randint(0, 100)] for i in range(n0)])
locations1 = np.array([[random.randint(0, 100), random.randint(0, 100)] for i in range(n1)])
locations2 = np.array([[random.randint(0, 100), random.randint(0, 100)] for i in range(n2)])

# Combine all the locations into one array
locations = np.concatenate((locations0, locations1, locations2), axis=0)

# Define the objective function to minimize
def objective_function(x):
    B1 = x[:total_parcels]
    B2 = x[total_parcels:]
    costs = n0 * costs0 + n1 * costs1 + n2 * costs2 + np.dot(B1, B1) + np.dot(B2, B2)
    return costs

# Define the constraints
def constraints(x):
    B1 = x[:total_parcels]
    B2 = x[total_parcels:]
    B1_con = np.array([B1[i] - B1_constraint[0] for i in range(total_parcels)])
    B2_con = np.array([B2[i] - B2_constraint[0] for i in range(total_parcels)])
    return np.concatenate((B1_con, B2_con))

# Initialize the decision variables
x0 = np.concatenate((np.zeros(total_parcels), np.zeros(total_parcels)))

# Call the optimizer
res = minimize(objective_function, x0, constraints={"type": "ineq", "fun": constraints})

# Plot the locations of the parcels
plt.scatter(locations0[:, 0], locations0[:, 1], color="red")
plt.scatter(locations1[:, 0], locations1[:, 1], color="green")
plt.scatter(locations2[:, 0], locations2[:, 1], color="blue")

# Show the plot
plt.show()
'''