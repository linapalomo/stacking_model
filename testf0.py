#initial data
#this file will create the random data and the data will be stored in a JSON file called data.py
#the data can be visible in the data frame file called "test_df.py"
###WORKING COMPLETE###

import numpy as np
import json

np.random.seed(42)

# Generate random costs
costs = np.random.normal(8, 0.5, size=(10, 2))
costs = np.column_stack((np.zeros((10, 1)),costs))

# Generate random Land Uses
initial_landuse_types = np.random.randint(0, 3, 10)

# Generate random benefits/ESS values
benefits = np.random.normal(10, 2, size=(10, 2))

# Calculate benefit1 and benefit2 values
benefit1_values = np.zeros((10, 3))
benefit2_values = np.zeros((10, 3))

proportions = [0, 0.6, 0.5]
for i in range(10):
    for j in range(1, 3):
        benefit1_values[i][j] = benefits[i][j-1] * proportions[j]
        benefit2_values[i][j] = benefits[i][j-1] * (1 - proportions[j])

# Save data to JSON file
data = {
    "costs": costs.tolist(),
    "initial_landuse_types": initial_landuse_types.tolist(),
    "benefits": benefits.tolist(),
    "benefit1_values": benefit1_values.tolist(),
    "benefit2_values": benefit2_values.tolist()
}

with open("data.json", "w") as outfile:
    json.dump(data, outfile)

# Print initial data
print("Current costs:", np.choose(initial_landuse_types, costs.T))
print("Current Land uses:", initial_landuse_types)

