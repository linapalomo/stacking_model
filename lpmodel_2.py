##this model contains a data frame that where i will try to add the info in
#a better way to perform the optimization.
import random
import json
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


###COSTS###
##Import data from the Costs model
with open('costs.json', 'r') as f:
    cost_data = json.load(f)

lu0_cost = cost_data['Costs LU0']
lu1_cost = cost_data['Costs LU1']
lu2_cost = cost_data['Costs LU2']


###BENEFITS###
#Import data from the benefits model
with open('benefits.json', 'r') as f:
    benefits_data = json.load(f)

lu0_benefit1 = benefits_data['b1_lu0']
lu0_benefit2 = benefits_data['b2_lu0']
lu1_benefit1 = benefits_data['b1_lu1']
lu1_benefit2 = benefits_data['b2_lu1']
lu2_benefit1 = benefits_data['b1_lu2']
lu2_benefit2 = benefits_data['b2_lu2']



lu0 = {"cost0": lu0_cost, "b1_lu0": lu0_benefit1, "b2_lu0": lu0_benefit2}
lu1 = {"c1": lu1_cost, "b1_lu1": lu1_benefit1, "b2_lu1": lu1_benefit2}
lu2 = {"c2": lu2_cost, "b1_lu2": lu2_benefit1, "b2_lu2": lu2_benefit2}

landscape = {"lu0": lu0, "lu1": lu1, "lu2": lu2}

filename = "landscape.json"

with open(filename, "w") as f:
    json.dump(landscape, f, indent=4)

print("Landscape data saved to", filename)
counter = 1
# Timestamp to keep track of different versions of the landscape
timestamp = int(time.time())

filename = f'landscape_{counter}.json'
with open(filename, "w") as f:
    json.dump(landscape, f)
    
counter += 1
time.sleep(1) #CHANGE EVRY RUN TO SAVE LANDSCAPES

print("Landscape data saved to", filename)

# Total number of land parcels =200

n_plots = 100
LU_prob = np.random.dirichlet(np.ones(3), size=1).tolist()[0]
LU0_parcels = int(n_plots * LU_prob[0])
LU1_parcels = int(n_plots * LU_prob[1])
LU2_parcels = n_plots - LU0_parcels - LU1_parcels
n_plots = 100


LU_distribution = {
    "LU0": LU0_parcels,
    "LU1": LU1_parcels,
    "LU2": LU2_parcels
}

with open("LU_distribution.json", "w") as f:
    json.dump(LU_distribution, f)

print("LU0: ", LU0_parcels)
print("LU1: ", LU1_parcels)
print("LU2: ", LU2_parcels)
print("Distribution saved in LU_distribution file")
print("SAVE IT")


totalcost1= LU1_parcels * lu1_cost
totalcost2= LU2_parcels * lu2_cost
total = totalcost1 + totalcost2
print("total costs", total)

## Generate the landscapes create a dataframe and save them in a json file.

land = {"landuse": ["LU0", "LU1", "LU2"],
        "costs":[lu0_cost, lu1_cost, lu2_cost],
        "benefit1":[lu0_benefit1, lu1_benefit1, lu2_benefit1], 
        "benefit2":[lu0_benefit2, lu1_benefit2, lu2_benefit2], "count":[LU0_parcels, LU1_parcels, LU2_parcels] }

df = pd.DataFrame(land)

print(df)

df.to_json('landscapedf.json', orient='records')

#obtain the total benefits in the land distribution
total_benefit1_LU1= LU1_parcels * lu1_benefit1
total_benefit1_LU2= LU2_parcels * lu2_benefit1
total_benefit1 = total_benefit1_LU1 + total_benefit1_LU2
print("Total benefits 1:", total_benefit1)


total_benefit2_LU1= LU1_parcels * lu1_benefit2
total_benefit2_LU2= LU2_parcels * lu2_benefit2
total_benefit2 = total_benefit2_LU1 + total_benefit2_LU2
print("Total benefits 2:", total_benefit2)

#save total benefits in a dictionary
total_benefits = {
    "total_benefit_1":total_benefit1,
    "total_benefit_2":total_benefit2
}

# Save the benefits in a JSON file
with open('total_benefits.json', 'w') as f:
    json.dump(total_benefits, f)

print("total benefits are saved in total_benefits.json")



