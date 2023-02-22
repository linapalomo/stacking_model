import random
import json
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


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

## Generate the landscapes and save them in a json file.
lu0 = {"cost0": lu0_cost, "b1_lu0": lu0_benefit1, "b2_lu0": lu0_benefit2}
lu1 = {"c1": lu1_cost, "b1_lu1": lu1_benefit1, "b2_lu1": lu1_benefit2}
lu2 = {"c2": lu2_cost, "b1_lu2": lu2_benefit1, "b2_lu2": lu2_benefit2}

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





