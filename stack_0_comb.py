import itertools
import json

# Define the options for each variable
lu_types = ['LU1', 'LU2']
mean_lu = [300, 100]
std_dev_lu = [0.25]
benefit_mean = [10, 30]
std_dev_b=[0.25]
proportion_options = [0.8, 0.2]



# Generate all combinations for each product type
combinations_p1 = list(itertools.product([lu_types[0]], mean_lu, std_dev_lu, benefit_mean, std_dev_b, proportion_options))
combinations_p2 = list(itertools.product([lu_types[1]], mean_lu, std_dev_lu, benefit_mean,std_dev_b, proportion_options))

# Combine the two sets of combinations
combinations = list(itertools.product(combinations_p1, combinations_p2))

# Filter redundant combinations
filtered_combinations = []
for combo in combinations:
    p1_combo, p2_combo = combo
    if p1_combo != p2_combo:  # Check if P1 and P2 have different combinations
        filtered_combinations.append(combo)


    
# Print the combinations
for combination in combinations:
    print(combination)
    
number=len(combinations)
print(number)

with open('combinations.json', 'w') as f:
    json.dump(combinations, f)

print(type(combinations))
