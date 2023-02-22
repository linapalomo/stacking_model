import pandas as pd
import numpy as np
import json
import random
import pulp 
import time
import model as stack
from numpy.random import default_rng

### I can use the timestamp to safe uniques json files for every iteration.


# Define the problem
prob_stacking = pulp.LpProblem("Landuse Optimization", pulp.LpMinimize)

    
# Define the decision variables
x0 = pulp.LpVariable("x0", lowBound=0, cat='Integer') # Number of plots with L0 landuse
x1 = pulp.LpVariable("x1", lowBound=0, cat='Integer') # Number of plots with L1 landuse
x2 = pulp.LpVariable("x2", lowBound=0, cat='Integer') # Number of plots with L2 landuse

counter = 0

while True:

###COST MODEL
# Generate the variables from a normal distribution (all the values are for testing purposes)
C1_mean= 1
C2_mean= 2 
C1_stddev = 0.5
C2_stddev = 0.5
C0 = 0
C1 = np.random.normal(C1_mean, C1_stddev)
C2 = np.random.normal(C2_mean, C2_stddev)


#BENEFITS MODEL 
#makes no sense, i cannor see the study of the STACKING here :S
##text Dr. Drechsler.

# Generate the variables from a bivariate normal distribution
B0 = 0 #is this necessary?
meanB1 = 1
meanB2 = 2
stdB1 = 0.5
stdB2 = 0.6
corr = 0.8 # Pearson correlation coefficient of 0.8 strong positive 
cov = corr * stdB1 * stdB2

B1 = np.random.normal(meanB1, stdB1, 1)
B2 = meanB2 + cov/stdB1 * (B1 - meanB1) + np.random.normal(0, stdB2, 1)
# Generate two random variables with the specified mean, covariance and correlation
print("B1: ", B1[0])
print("B2: ", B2[0])

# Create a dictionary containing the costs and benefits
data = {'LU1': {'C1': C1, 'B1': B1},
            'LU2': {'C2': C2, 'B2': B2}, 'LU0' :{'C0': C0, 'B0': B0}}

# Save the dictionary to a JSON file
file_name = f'costs_benefits_{counter}.json'
with open(file_name, 'w') as f:
    json.dump(data, f)

counter += 1
time.sleep(10) # wait for 10 second before generating new data

##Generate the random Landscape
LU_prob = np.random.dirichlet(np.ones(3), size=1).tolist()[0]
LU0, LU1, LU2 = [int(prob * 100) for prob in LU_prob]


n_plots = 200 #for testing 
LU0_parcels = int(n_plots * LU0 / 100)
LU1_parcels = int(n_plots * LU1 / 100)
LU2_parcels = int(n_plots * LU2 / 100)


LU_distribution = {
    "LU0": LU0_parcels,
    "LU1": LU1_parcels,
    "LU2": LU2_parcels
}

with open("LU_distribution.json", "w") as f:
    json.dump(LU_distribution, f)

################################################################


# Objective function: Minimize the total cost
prob += C1 * x1 + C2 * x2 + C0 * x0, "Total Cost"

# Constraints
prob += x1 + x2 + x0 <= 100, "Total plots"
prob += x1 >= x1_initial, "Minimum L1 plots"
prob += x2 >= x2_initial, "Minimum L2 plots"
prob += B1 * x1 + B2 * x2 >= 0, "Total Benefit"

# Solve the optimization problem
prob.solve()

# Print the optimization results
print("Optimal Solution:")
print("x1 = ", x1.varValue)
print("x2 = ", x2.varValue)
print("Total Cost = ", pulp.value(prob.objective))

rng = default_rng()
#vals = rng.standard_normal(10)
#more_vals = rng.standard_normal(10)
'''
cost_lu1 = np.random.normal(loc=1.0, scale=0.5, size=1) #loc: mean, scale:sd, size:output shape
cost_lu2 = np.random.normal(loc=1.0, scale=0.5, size=1)
benefit1 = np.random.normal(loc=0.5, scale=1, size=1) #investigar aqui como hago una distribucion que sea solo numeros negativos hasta 1
benefit2 = 1 - benefit1
lu1 = {
    'cost1':cost_lu1, 'cost2':cost_lu2}


'''

mean = 1
standard_deviation = 0.5
random_number = random.normalvariate(mean, standard_deviation)
print(random_number)

'''def generate_probability(n):
    lu_0 = 0
    lu_1 = 0
    lu_2 = 0
    for i in range(n):
        rand = random.random()
        if rand < 1/3:
            lu_0 += 1
        elif rand < 2/3:
            lu_1 += 1
        else:
            lu_2 += 1
    return lu_0/n, lu_1/n, lu_2/n'''

"""
    i can adjust the conditions in order to generate different probabilities 
if rand < 0.25:
    lu_0 += 1
elif rand < 0.55:
    lu_1 += 1
else:
    lu_2 += 1

    """
'''
prob_lu_0, prob_lu_1, prob_lu_2 = generate_probability(100)
print("Probability of lu_0: ", prob_lu_0)
print("Probability of lu_1: ", prob_lu_1)
print("Probability of lu_2: ", prob_lu_2)
'''

   
'''
import json

# Load existing data from file
try:
    with open("data.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {}

# Add new data to existing data
data["new_field"] = "new value"

# Write updated data back to file
with open("data.json", "w") as file:
    json.dump(data, file)

'''


'''
 Cómo crear un landscape en mi codigo?
1. Crear los landscapes individualmente despúes de obtener los datos de las distribuciones
2. Crear un json con cada landscape creado o con cada lu creado.
3.Porque luego tengo que usar dos distintas restricciones. Se corre dos veces.
4. necesitaré una api para traer los datos ?
5. 
'''




