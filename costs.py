import random
import json

##Costs model
mean1 = 1
stddev1 = 0.5
mean2 = 2
stddev2 = 1

c0= 0
c1 = random.normalvariate(mean1, stddev1)
c2 = random.normalvariate(mean2, stddev2)

# Print the results
print("Total costs for land use 0:", c0)
print("Total costs for land use 1:", c1)
print("Total costs for land use 2:", c2)




# Create a dictionary to with the costs
costs = {
    "Costs LU0": 0,
    "Costs LU1": c1,
    "Costs LU2": c2,
    
}

# Save the costs in a JSON file
with open('costs.json', 'w') as f:
    json.dump(costs, f)

# Print a confirmation message
print("Costs of each LU are saved in costs.json. Please save the data for the work")
print("PLEASE COPY THE DATA FOR THE ANALYSIS")
###
