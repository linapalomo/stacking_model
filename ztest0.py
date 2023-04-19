#initial data
#this file will create the random data and the data will be stored in a JSON file called data.py
#the data can be visible in the data frame file called "test_df.py"
###WORKING COMPLETE###

import numpy as np
import json

#np.random.seed(42)
#np.random.seed(0) #will keep the same number random generated in every run
####i have to change the seed number###

# Generate random costs size here=parcels
costs1 = np.random.normal(300, 10, size=4) #mean ,standard dev
costs2= np.random.normal(100, 8, size=4)
costs = np.column_stack((np.zeros((4, 1)),costs1, costs2))


# Generate random Land Uses
initial_landuse_types = np.random.randint(0, 3, 4)

# Generate random benefits/ESS values
benefit1 = np.random.normal(12, 2, size=4) #i can change the media a standard deviation
benefit2 = np.random.normal(19, 1, size=4)

# Calculate benefit1 and benefit2 values
benefit1_values = np.zeros((4, 3))
benefit2_values = np.zeros((4, 3))

#i can change the proportions for the benefits any time
proportions = {
    "LU1":[0,0.3,0.7],
    "LU2":[0,0.4,0.6]
}
   

for i in range(4):
    for j in range(1,3):
        LU1_p = proportions['LU1'][j]
        LU2_p = proportions["LU2"][j]
        benefit1_values[i][1]=benefit1[i] * LU1_p
        benefit2_values[i][1]=benefit1[i] * (1-LU1_p)
        benefit1_values[i][2]=benefit2[i] * LU2_p
        benefit2_values[i][2]=benefit2[i] * (1-LU2_p)

# Save data to JSON file
data = {
    "costs": costs.tolist(),
    "initial_landuse_types": initial_landuse_types.tolist(),
    "benefitLU1": benefit1.tolist(),
    "benefitLU2":benefit2.tolist(),
    "benefit1_values": benefit1_values.tolist(),
    "benefit2_values": benefit2_values.tolist(),
    "Total_ESS1": sum(np.choose(initial_landuse_types, benefit1_values.T)), #####new
    "Total_ESS2":sum(np.choose(initial_landuse_types, benefit2_values.T)) #new
}

with open("dataz.json", "w") as outfile:
    json.dump(data, outfile)

# Print initial data
print("Current costs:", sum(np.choose(initial_landuse_types, costs.T)))
print("Current Land uses:", initial_landuse_types)
print("Current ESS1:", np.choose(initial_landuse_types, benefit1_values.T))
print("Current ESS2:", np.choose(initial_landuse_types, benefit2_values.T))
print("Total ESS1:", sum(np.choose(initial_landuse_types, benefit1_values.T)))
print("Total ESS2:", sum(np.choose(initial_landuse_types, benefit2_values.T)))


#print(type(data))