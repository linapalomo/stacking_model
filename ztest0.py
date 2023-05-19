#initial data
#this file will create the random data and the data will be stored in a JSON file called data.py
#the data can be visible in the data frame file called "test_df.py"
###WORKING COMPLETE###

import numpy as np
import json

#np.random.seed(42)
#np.random.seed(0) #will keep the same number random generated in every run
####i have to change the seed number###

with open('combinations.json') as f:
    all_data = json.load(f)

# Select the specific data set. For example, to select the first data set:
data = all_data[0] #change for every data set , starts with 0 finish at 63
mean_lu1=data[0][1]
std_lu1=(data[0][2]*mean_lu1)
mean_b1=data[0][3]
std_b1=(data[0][4]*mean_b1)
prop_lu1=data[0][5]
proplu1_2=round(1-prop_lu1, 1)

mean_lu2=data[1][1]
std_lu2=(data[1][2]*mean_lu1)
mean_b2=data[1][3]
std_b2=(data[1][4]*mean_b1)
prop_lu2=data[1][5]
proplu2_2=round(1-prop_lu2, 1)

num_parcels= 35
landuse_types= 3
# Generate random costs size here=parcels
def generate_costs(mean, std_dev, num_parcels):
    return np.random.normal(mean, std_dev, num_parcels)

costs1 = generate_costs(mean_lu1, std_lu1, num_parcels)
costs2= generate_costs(mean_lu2, std_lu2, num_parcels)
costs = np.column_stack((np.zeros((num_parcels, 1)),costs1, costs2))

# Generate random Land Uses
initial_landuse_types = np.random.randint(0, landuse_types,num_parcels)

#print(benefit1, benefit2)
def generate_benefit(mean_b1, std_dev, num_parcels):
    return np.random.normal(mean_b1, std_dev, num_parcels)

benefit1 = generate_costs(mean_b1, std_b1, num_parcels)
benefit2= generate_costs(mean_b2, std_b2, num_parcels)


# Calculate benefit1 and benefit2 values
benefit1_values = np.zeros((num_parcels, landuse_types))
benefit2_values = np.zeros((num_parcels, landuse_types))

#i can change the proportions for the benefits any time
proportions = {
    "LU1":[0,prop_lu1,proplu1_2],
    "LU2":[0,prop_lu2,proplu2_2]
}
   

for i in range(num_parcels):
    for j in range(1,3):
        LU1_p = proportions['LU1'][j]
        LU2_p = proportions['LU2'][j]
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