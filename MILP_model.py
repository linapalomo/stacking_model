# MODEL WITH MILP mixed-integer linear programming 

import pulp
import matplotlib.pyplot as plt

# Define the binary variables for the location of each parcel
x0_1 = pulp.LpVariable("x0_1", 0, 1, pulp.LpInteger)
x0_2 = pulp.LpVariable("x0_2", 0, 1, pulp.LpInteger)
x0_3 = pulp.LpVariable("x0_3", 0, 1, pulp.LpInteger)

x1_1 = pulp.LpVariable("x1_1", 0, 1, pulp.LpInteger)
x1_2 = pulp.LpVariable("x1_2", 0, 1, pulp.LpInteger)
x1_3 = pulp.LpVariable("x1_3", 0, 1, pulp.LpInteger)

x2_1 = pulp.LpVariable("x2_1", 0, 1, pulp.LpInteger)
x2_2 = pulp.LpVariable("x2_2", 0, 1, pulp.LpInteger)
x2_3 = pulp.LpVariable("x2_3", 0, 1, pulp.LpInteger)

# Define the optimization problem
model = pulp.LpProblem("Land Parcel Optimization", pulp.LpMinimize)

# Define the objective function
model += 0 * x0_1 + 1.5 * x1_1 + 2.5 * x2_1 + 7 * x1_2 + 5 * x2_2 + 0 * x0_3 + 3 * x1_3 + 5 * x2_3

# Constraints to ensure that each parcel is located in exactly one location
model += x0_1 + x0_2 + x0_3 == 1
model += x1_1 + x1_2 + x1_3 == 1
model += x2_1 + x2_2 + x2_3 == 1

# Constraint for B2 >= 200
model += 3 * x1_1 + 5 * x2_1 >= 200
model += 3 * x1_2 + 5 * x2_2 >= 200
model += 3 * x1_3 + 5 * x2_3 >= 200

# Constraint for B1 >= 300
model += 7 * x1_1 + 5 * x2_1 >= 300
model += 7 * x1_2 + 5 * x2_2 >= 300
model += 7 * x1_3 + 5 * x2_3 >= 300

# Solve the optimization problem
model.solve()

# Print the results
print("Total Cost: ", pulp.value(model.objective))
print("Location of LU0: ", x0_1.varValue, x0_2.varValue, x0_3.varValue)
print("Location of LU1: ", x1_1.varValue, x1_2.varValue, x1_3.varValue)
print("Location of LU2: ", x2_1.varValue, x2_2.varValue, x2_3.varValue)
print("B1: ", 7 * x1_1.varValue + 5 * x2_1.varValue)
print("B2: ", 3 * x1_1.varValue + 5 * x2_1.varValue)
print("B1: ", 7 * x1_2.varValue + 5 * x2_2.varValue)
print("B2: ", 3 * x1_2.varValue + 5 * x2_2.varValue)
print("B1: ", 7 * x1_3.varValue + 5 * x2_3.varValue)
print("B2: ", 3 * x1_3.varValue + 5 * x2_3.varValue)


# plot the location of each land parcel
plt.scatter([0]*36 + [1]*42 + [2]*22, [0]*36 + [1]*42 + [2]*22, c=[0]*36 + [1]*42 + [2]*22)
plt.xlabel("Land parcel location")
plt.ylabel("Land parcel location")
plt.show()

import matplotlib.pyplot as plt

# Create a 2D array to represent the grid
grid = [[0 for i in range(10)] for j in range(10)]

# Assign values to the grid cells based on the land parcel locations
for i in range(36):
    grid[i%10][0] = 0
for i in range(42):
    grid[i%10][1] = 1
for i in range(22):
    grid[i%10][2] = 2

# Plot the grid
plt.imshow(grid, cmap='jet')
plt.xlabel("X")
plt.ylabel("Y")
plt.colorbar()
plt.show()


