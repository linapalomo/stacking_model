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
def generate_costs(mean, std_dev, num_parcels):
    return np.random.normal(mean, std_dev, num_parcels)

costs1 = generate_costs(300, 10, 10)
costs2= generate_costs(100, 8, 10)
costs = np.column_stack((np.zeros((10, 1)),costs1, costs2))

# Generate random Land Uses
initial_landuse_types = np.random.randint(0, 3, 10)

# Generate random benefits/ESS values
def generate_benefits(mean1, std_dev1, mean2, std_dev2, corr_coef, num_parcels):
    mean = [mean1, mean2]
    cov = [[std_dev1**2, corr_coef*std_dev1*std_dev2],
           [corr_coef*std_dev1*std_dev2, std_dev2**2]]
    

    benefit1, benefit2 = np.random.multivariate_normal(mean, cov, num_parcels).T

    return np.column_stack((benefit1, benefit2))

benefits_numbers = generate_benefits(mean1=12, std_dev1=2, mean2=19, std_dev2=1, corr_coef=0.8, num_parcels=10)

benefit1 = benefits_numbers[:, 0]
benefit2 = benefits_numbers[:, 1]

#print(benefit1, benefit2)

"""benefit1 = np.random.normal(12, 2, size=10) #i can change the media a standard deviation
benefit2 = np.random.normal(19, 1, size=10)"""

# Calculate benefit1 and benefit2 values
benefit1_values = np.zeros((10, 3))
benefit2_values = np.zeros((10, 3))

#i can change the proportions for the benefits any time
proportions = {
    "LU1":[0,0.3,0.7],
    "LU2":[0,0.4,0.6]
}
   

for i in range(10):
    for j in range(1,3):
        LU1_p = proportions['LU1'][j]
        LU2_p = proportions["LU2"][j]
        benefit1_values[i][j]=benefit1[i] * LU1_p
        benefit2_values[i][j]=benefit1[i] * (1-LU1_p)
        benefit1_values[i][j]=benefit2[i] * LU2_p
        benefit2_values[i][j]=benefit2[i] * (1-LU2_p)

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
print("Current ES1:", np.choose(initial_landuse_types, benefit1_values.T))
print("Current ES2:", np.choose(initial_landuse_types, benefit2_values.T))
print("Total ES1:", sum(np.choose(initial_landuse_types, benefit1_values.T)))
print("Total ES2:", sum(np.choose(initial_landuse_types, benefit2_values.T)))


#print(type(data))