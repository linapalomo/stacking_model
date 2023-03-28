import pandas as pd
import pulp
import json




###WORKING BITCH###



##this is the optimization model for panda, continuation
## of the model_2

df = pd.read_json('landscapedf.json')
print(df)


# Create decision variables for each row in the dataframe
#x_names = ['x0', 'x1', 'x2']
#x = pulp.LpVariable.dicts("x", x_names, lowBound=0, cat='Continuous')

#x = {}
#for i in df.index:
 #   x[i] = pulp.LpVariable(f"x{i}", lowBound=0, upBound=100, cat='Integer') #chanege to 200 plots
    
 #Define the decision variables
vars_dict = pulp.LpVariable.dict("x", df['landuse'], lowBound=0, cat='Integer')
df['x'] = df['landuse'].apply(lambda x: vars_dict[x])



print(df)

# Define the LP problem
lp_prob = pulp.LpProblem("Costs_minimizing", pulp.LpMinimize)

# Add the objective function using the dataframe
lp_prob += pulp.lpSum((df['costs'][0]*df['x'] * df['costs'][1]*df['x'] + df['costs'][2]*df['x'])), "Total Cost"
#lp_prob += pulp.lpSum([df.loc[i, 'costs'] * df['x'] * df['count'] for i in df.index]) + \
#pulp.lpSum([df.loc[i, 'benefit1'] * df['x'] * df[ 'count'] for i in df.index]) + \
#pulp.lpSum([df.loc[i, 'benefit2'] * df['x'] * df['count'] for i in df.index])

#lp_prob += pulp.lpSum([df.loc[i, 'costs'] * x[i] * df.loc[i, 'count'] for i in df.index]) + pulp.lpSum([x[i] * df.loc[i, 'count'] for i in df.index])


#bring the total benefits for the constraints
with open('total_benefits.json', 'r') as f:
    tbenefits_data = json.load(f)
    total_benefit1 = tbenefits_data['total_benefit_1']
    total_benefit2 = tbenefits_data['total_benefit_2']
    

# Define the constraints

# Add a constraint that enforces the non-negative constraint
for i in df['x'].keys():
    lp_prob += df['x'][i] >= 0, f"non_negative_constraint_{i}"
    
lp_prob += pulp.lpSum(df['x']) == 100, "Total Number of lands Constraint"
lp_prob += pulp.lpSum(df['benefit1']*df['x']) >= pulp.lpSum(df['count']*df['benefit1']), "benefit1 Constraint"
lp_prob += pulp.lpSum(df['benefit2']*df['x']) >= pulp.lpSum(df['count']*df['benefit2']), "benefit2 Constraint"


# Create a linear expression for the left-hand side of the inequality
#lhs_expr = pulp.lpSum([df.loc[i, 'benefit1'] * df['x'][i] for i in df.index])

# Add a new constraint that enforces the strict inequality
#lp_prob += lhs_expr >= total_benefit1 + 1e-6, "benefit1_constraint"  #add a small epsilon to ensure strict inequality
#lp_prob += lhs_expr >= total_benefit1 + 1e-6, "benefit1_constraint"

##second constraint
#lhs_expr = pulp.lpSum([df.loc[i, 'benefit2'] * df['x'][i] for i in df.index])
#lp_prob += lhs_expr >= total_benefit2 + 1e-6,  "benefit2_constraint"  #add a small epsilon to ensure strict inequality

#it must consider all 200 plots
total_plots=100
#lp_prob += pulp.lpSum([x[i] * df.loc[i, 'count'] for i in df.index]) == total_plots
#lp_prob += pulp.lpSum([df['x'][i]]) == total_plots, "total_count"  # ensure that the sum of all decision variables is equal to 200
# The factor 1000 is used to ensure that the right-hand side is negative when z = 0 and positive when z = 1

# Solve the LP problem
lp_prob.solve()



# Print the optimal solution
for variable in lp_prob.variables():
    print(variable.name, "=", variable.varValue)
    # add a print statement for each variable to show its value
    if variable.name == 'x_0':
        print("x_0 value =", variable.varValue)
    elif variable.name == 'x_1':
        print("x_1 value =", variable.varValue)
    elif variable.name == 'x_2':
        print("x_2 value =", variable.varValue)

print("Total cost =", pulp.value(lp_prob.objective))

# Print the constraint values
for constraint in lp_prob.constraints.values():
    print(constraint.name, ":", constraint.value())

# Check if the first constraint is met
lhs_value = sum([df.loc[i, 'benefit1'] * df['x'][i].value() for i in df.index])
if lhs_value >= total_benefit1:
    print("First constraint is met!")
else:
    print("First constraint is not met.")
    
# Check if the second constraint is met
lhs_value = sum([df.loc[i, 'benefit2'] * df['x'][i].value() for i in df.index])
if lhs_value >= total_benefit2:
    print("Second constraint is met!")
else:
    print("Second constraint is not met.")
    
print(df['x'])


