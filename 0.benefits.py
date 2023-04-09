import numpy as np
import json


# Generate total benefits for LU1 and LU2
# LU0 has no benefits
mean_tb1 = 8 #mean total benefit lu1
stddev_tb1 = 1  #stdev total benefit lu2 
mean_tb2 = 6 #mean total benefit lu2
stddev_tb2 = 0.5 #standard deviation benefit lu2
tb_lu1_total = np.random.normal(mean_tb1, stddev_tb1) 
tb_lu2_total = np.random.normal(mean_tb2, stddev_tb2)

# Define percentage for each benefit variable in each land use, tengo que cambiar esto conforme a lambda
b1_lu1_pct = 0.6 #percentage of B1 in LU1
b2_lu1_pct = 0.4 #percentage of B2 in LU1
b1_lu2_pct = 0.8 #percentage of B1 in LU2
b2_lu2_pct = 0.2 #percentage of B2 in LU2

# Calculate the benefit variables for each land use
b1_lu0 = 0
b2_lu0 = 0
b1_lu1 = b1_lu1_pct * tb_lu1_total
b2_lu1 = b2_lu1_pct * tb_lu1_total
b1_lu2 = b1_lu2_pct * tb_lu2_total
b2_lu2 = b2_lu2_pct * tb_lu2_total

# Print the results
print("Total benefit for land use 1:", tb_lu1_total)
print("Total benefit for land use 2:", tb_lu2_total)
print("Benefit 1 for land use 1:", b1_lu1)
print("Benefit 2 for land use 1:", b2_lu1)
print("Benefit 1 for land use 2:", b1_lu2)
print("Benefit 2 for land use 2:", b2_lu2)


# Create a dictionary with the benfit model 
benefits = {
    "b1_lu0": b1_lu0,
    "b2_lu0": b2_lu0,
    "b1_lu1": b1_lu1,
    "b2_lu1": b2_lu1,
    "b1_lu2": b1_lu2,
    "b2_lu2": b2_lu2, 
    "Percentage of b1_lu1": b1_lu1_pct,
    "Percentage of b2_lu2": b2_lu1_pct,
    "Percentage of b1_lu2": b1_lu2_pct,
    "Percentage of b2_lu2": b2_lu2_pct,
    "total_benefit_lu1": tb_lu1_total,
    "total_benefit_lu2": tb_lu2_total
}

# Save the benefits in a JSON file
with open('benefits.json', 'w') as f:
    json.dump(benefits, f)

# Print a confirmation message
print("Benefits of each LU are saved in benefits.json. Please save the data for the work")

###