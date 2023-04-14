
#generate the random costs of every plot/parcel

import random

# Set the mean and standard deviation for the normal distribution
mean = 20
std_dev = 2

#three landuses
landuses=["LUO", "LU1", "LU2"]

# Generate two random costs for each of the 10 products
num_parcels = 10
landuse_dist = []
for i in range(num_parcels):
    cost1 = round(random.gauss(mean, std_dev), 2)
    cost2 = round(random.gauss(mean, std_dev), 2)
    landuse_type = random.choice(landuses)
    landuse_dist.append((cost1, cost2, landuse_type))

# Print the costs for each parcel
for i, (cost1, cost2, landuse_type) in enumerate(landuse_dist):
    print(f"Parcel {i+1}: Cost 1 = {cost1}, Cost 2 = {cost2}, Type = {landuse_type}")