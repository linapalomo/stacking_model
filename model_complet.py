import random
import json
import time
import matplotlib.pyplot as plt
import numpy as np


##Costs model
mean1 = 1
stddev1 = 0.5
mean2 = 2
stddev2 = 1

c1 = random.normalvariate(mean1, stddev1)
c2 = random.normalvariate(mean2, stddev2)

################################
#Benefit model
# Generate total benefits for LU1 and LU2
# LU0 has no benefits
mean_tb1 = 8
stddev_tb1 = 1 
mean_tb2 = 6
stddev_tb2 = 0.5

###Percentages for each total benefit in each LU###
perc_lu1_b1 = 0.5 #percentage of B1 in LU1
perc_lu1_b2 =  0.5 #percentage of B2 in LU1
perc_lu2_b1 = 0.6 #percentage of B1 in LU2
perc_lu2_b2 = 0.4 #percentage of B2 in LU2

tb_lu1 = random.normalvariate(mean_tb1, stddev_tb1) #total benenfit lu1
tb_lu2 = random.normalvariate(mean_tb2, stddev_tb2) #total benefit lu2

b1_lu1 = tb_lu1 * perc_lu1_b1
b2_lu1 = tb_lu1 * perc_lu1_b2
b1_lu2 = tb_lu2 * perc_lu2_b1
b2_lu2 = tb_lu2 * perc_lu2_b2

## Generate the landscapes and save them in a json file.
lu0 = {"cost0": 0, "b1_lu0": 0, "b2_lu0": 0}
lu1 = {"c1": c1, "b1_lu1": b1_lu1, "b2_lu1": b2_lu1}
lu2 = {"c2": c2, "b1_lu2": b1_lu2, "b2_lu2": b2_lu2}

landscape = [lu0, lu1, lu2]

filename = "landscape.json"

with open(filename, "w") as f:
    json.dump(landscape, f, indent=4)

print("Landscape data saved to", filename)
counter = 0
# Timestamp to keep track of different versions of the landscape
timestamp = int(time.time())

filename = f'landscape_{counter}.json'
with open(filename, "w") as f:
    json.dump(landscape, f)
    
counter += 1
time.sleep(10)

print("Landscape data saved to", filename)
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




