import random
import numpy as np
import json

# Generate random costs for LU1 and LU2, and set LU cost to 0
costs = np.random.normal(40, 1, size=(10, 2))
costs = np.hstack((np.zeros((10, 1)), costs))

# Randomly assign initial product types to each parcel
initial_landuse_types = [random.randint(0, 2) for _ in range(10)]

#benefits (ESS) values are randomly generated for each parcel
benefits=np.random.normal(15,3, size= (10,1))

#calculate the benefits1 and benefit2 values for each land use
proportions={1:0.6, 2:0.5}
benefit1 = np.zeros((10,3))
benefit2 = np.zeros((10,3))

for landuse_type, propo in proportions.items():
    benefit1[:,landuse_type]= benefits[:, 0] * propo
    benefit2[:,landuse_type]= benefits[:, 0] * (1-propo)

# Calculate the total cost for the initial distribution
initial_total_cost = sum(costs[i][landuse_type - 1] for i, landuse_type in enumerate(initial_landuse_types))

# Print initial distribution of parcels, landuse, benefits and costs
print("Initial parcels, Costs, and land uses and benefits:")
for i, (cost, landuse_type, ben1, ben2) in enumerate(zip(costs, initial_landuse_types, benefit1, benefit2)):
    print(f"Parcel {i+1}: Costs (LU0, LU1, LU2) = {tuple(cost)}, Initial land use: LU{landuse_type}, Cost: {cost[landuse_type]}, benefit1:{tuple(ben1)}, benefit2:{tuple(ben2)}")


# Print the initial total cost
print(f"Initial total cost: {initial_total_cost}")

# Calculate and print the initial total marketing1 and marketing2 values
initial_total_benefit1 = sum(benefit1[i][product_type] for i, product_type in enumerate(initial_landuse_types))
initial_total_benefit2 = sum(benefit2[i][product_type] for i, product_type in enumerate(initial_landuse_types))
print(f"Initial total benefit1: {initial_total_benefit1}")
print(f"Initial total benefit2: {initial_total_benefit2}")

# Save the data to a JSON file
data = {'costs': costs.tolist(), 'initial_landuse_types': initial_landuse_types, 'benefits': benefits.tolist(), 'benefit1':benefit1.tolist(), 'benefit2':benefit2.tolist()}
with open('data.json', 'w') as file:
    json.dump(data, file)
