import itertools

# Define the options for each variable
product_types = ['P1', 'P2']
mean_options = ['High', 'Low']
std_dev_options = ['High', 'Low']
marketing_value_options = ['High', 'Low']
proportion_options = ['High', 'Low', 'Equal']

# Define the variable names
variable_names = {
    0: 'Product Type',
    1: 'Mean',
    2: 'Standard Deviation',
    3: 'Marketing Value',
    4: 'Proportion'
}

# Generate all combinations for each product type
combinations_p1 = list(itertools.product([product_types[0]], mean_options, std_dev_options, marketing_value_options, proportion_options))
combinations_p2 = list(itertools.product([product_types[1]], mean_options, std_dev_options, marketing_value_options, proportion_options))

# Combine the two sets of combinations
combinations = list(itertools.product(combinations_p1, combinations_p2))

# Print the combinations with variable names
for combination in combinations:
    combo_dict = {}
    for i, value in enumerate(combination[0]):
        variable_name = variable_names[i]
        combo_dict[variable_name] = value
    for i, value in enumerate(combination[1]):
        variable_name = variable_names[i]
        combo_dict[variable_name] = value
    print(combo_dict)
