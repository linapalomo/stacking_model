#####Benefits error

import numpy as np
import json

costs1 = np.random.normal(30, 10, size=10)
costs2 = np.random.normal(10, 8, size=10)
costs = np.column_stack((np.zeros((10, 1)), costs1, costs2))

initial_product_types = np.random.randint(0, 3, 10)

tmarketing1 = np.random.normal(10, 2, size=10)
tmarketing2 = np.random.normal(19, 1, size=10)

type1_values = np.zeros((10, 3))
type2_values = np.zeros((10, 3))

proportions = {
    "p1": [0, 0.3, 0.7],
    "p2": [0, 0.4, 0.6]
}

for i in range(10):
    for j in range(1, 3):
        p1_prop = proportions['p1'][j]
        p2_prop = proportions["p2"][j]
        type1_values[i][j] = tmarketing1[i] * p1_prop
        type2_values[i][j] = tmarketing1[i] * (1 - p1_prop)
        type1_values[i][j] = tmarketing2[i] * p2_prop
        type2_values[i][j] = tmarketing2[i] * (1 - p2_prop)

initial_costs = np.zeros(10)
initial_marketing1 = np.zeros(10)
initial_marketing2 = np.zeros(10)

for i, product_type in enumerate(initial_product_types):
    initial_costs[i] = costs[i, product_type]
    initial_marketing1[i] = type1_values[i, product_type]
    initial_marketing2[i] = type2_values[i, product_type]

data = {
    "costs": costs.tolist(),
    "initial_product_types": initial_product_types.tolist(),
    "total_marketing1": tmarketing1.tolist(),
    "total_marketing2": tmarketing2.tolist(),
    "type1_values": type1_values.tolist(),
    "type2_values": type2_values.tolist(),
    "initial_costs": initial_costs.tolist(),
    "initial_marketing1": initial_marketing1.tolist(),
    "initial_marketing2": initial_marketing2.tolist(),
}

with open("datatest.json", "w") as outfile:
    json.dump(data, outfile)
