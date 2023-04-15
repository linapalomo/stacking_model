#initial data.py
import numpy as np
import json

np.random.seed(42)

# Generate random costs
costs = np.random.normal(8, 0.5, size=(10, 2))
costs = np.column_stack((costs, np.zeros((10, 1))))

# Generate random product types
initial_product_types = np.random.randint(0, 3, 10)

# Generate random tmarketing values
tmarketing = np.random.normal(10, 2, size=(10, 2))

# Calculate marketing1 and marketing2 values
marketing1_values = np.zeros((10, 3))
marketing2_values = np.zeros((10, 3))

proportions = [0, 0.6, 0.5]
for i in range(10):
    for j in range(1, 3):
        marketing1_values[i][j] = tmarketing[i][j-1] * proportions[j]
        marketing2_values[i][j] = tmarketing[i][j-1] * (1 - proportions[j])

# Save data to JSON file
data = {
    "costs": costs.tolist(),
    "initial_product_types": initial_product_types.tolist(),
    "tmarketing": tmarketing.tolist(),
    "marketing1_values": marketing1_values.tolist(),
    "marketing2_values": marketing2_values.tolist()
}

with open("data.json", "w") as outfile:
    json.dump(data, outfile)

# Print initial data
print("Current costs:", np.choose(initial_product_types, costs.T))
print("Current product types:", initial_product_types)
