import json
import numpy as np
from pulp import LpVariable, LpProblem, LpMinimize, lpSum, LpStatus

with open('datatest.json') as f:
    data = json.load(f)

n_locations = len(data['costs'])
n_products = len(data['costs'][0])
costs = np.array(data['costs'])
initial_product_types = np.array(data['initial_product_types'])
type1_values = np.array(data['type1_values'])
type2_values = np.array(data['type2_values'])

problem = LpProblem('Optimization', LpMinimize)

x = [[LpVariable(f'x{i}{j}', cat='Binary') for j in range(n_products)] for i in range(n_locations)]

problem += lpSum(costs[i][j] * x[i][j] for i in range(n_locations) for j in range(n_products))

for i in range(n_locations):
    problem += lpSum(x[i][j] for j in range(n_products)) == 1

for j in range(n_products):
    problem += lpSum(x[i][j] for i in range(n_locations)) >= 1

initial_total_marketing1 = sum(data['initial_marketing1'])
initial_total_marketing2 = sum(data['initial_marketing2'])

problem += lpSum(type1_values[i][j] * x[i][j] for i in range(n_locations) for j in range(n_products) if j != 0) + \
           lpSum(type2_values[i][j] * x[i][j] for i in range(n_locations) for j in range(n_products) if j != 0) \
           >= initial_total_marketing1 + initial_total_marketing2

problem.solve()

print("Status:", LpStatus[problem.status])

optimized_product_types = []
for i in range(n_locations):
    for j in range(n_products):
        if x[i][j].varValue == 1:
            optimized_product_types.append(j)

print("Optimized Product Types:", optimized_product_types)

print("Initial total costs:", sum(data['initial_costs']))
print("Optimized total costs:", sum(np.choose(optimized_product_types, costs.T)))

initial_marketing1 = np.sum(type1_values * (initial_product_types.reshape(-1, 1) == np.arange(n_products)), axis=1)
initial_marketing2 = np.sum(type2_values * (initial_product_types.reshape(-1, 1) == np.arange(n_products)), axis=1)
optimized_marketing1 = np.sum(type1_values * (np.array(optimized_product_types).reshape(-1, 1) == np.arange(n_products)), axis=1)
optimized_marketing2 = np.sum(type2_values * (np.array(optimized_product_types).reshape(-1, 1) == np.arange(n_products)), axis=1)
print("Initial Marketing1 values:", initial_marketing1)
print("Initial Marketing2 values:", initial_marketing2)
print("Optimized Marketing1 values:", optimized_marketing1)
print("Optimized Marketing2 values:", optimized_marketing2)
