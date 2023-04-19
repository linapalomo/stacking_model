import numpy as np
import json

np.random.seed(0)  # For reproducibility
num_locations = 10

# Costs for each product type
costs_p1 = np.random.normal(70, 2, num_locations)
costs_p2 = np.random.normal(40, 1, num_locations)

# Marketing values for each product type
marketing_type1 = np.random.normal(8, 1, num_locations)
marketing1_p1 = marketing_type1 * 0.8
marketing2_p1 = marketing_type1 * 0.2

marketing_type2 = np.random.normal(8, 1, num_locations)
marketing1_p2 = marketing_type2 * 0.4
marketing2_p2 = marketing_type2 * 0.6

# Randomly assign product types to locations
assigned_product_types = np.random.randint(0, 3, num_locations)

# Store costs and marketing values for assigned product types
location_costs = np.zeros(num_locations)
location_marketing1 = np.zeros(num_locations)
location_marketing2 = np.zeros(num_locations)

for i, product_type in enumerate(assigned_product_types):
    if product_type == 0:
        location_costs[i] = 0
        location_marketing1[i] = 0
        location_marketing2[i] = 0
    elif product_type == 1:
        location_costs[i] = costs_p1[i]
        location_marketing1[i] = marketing1_p1[i]
        location_marketing2[i] = marketing2_p1[i]
    elif product_type == 2:
        location_costs[i] = costs_p2[i]
        location_marketing1[i] = marketing1_p2[i]
        location_marketing2[i] = marketing2_p2[i]

# Organize the data in a dictionary
data = {
    'assigned_product_types': assigned_product_types.tolist(),
    'location_costs': location_costs.tolist(),
    'location_marketing1': location_marketing1.tolist(),
    'location_marketing2': location_marketing2.tolist()
}

# Save the data to a JSON file
with open('location_data.json', 'w') as outfile:
    json.dump(data, outfile)

print("Data saved to 'location_data.json'")
