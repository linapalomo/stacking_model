from scipy.optimize import linprog

# Define the objective function coefficients
c = [-0, -1.5, -2.5] #C0, C1, C2 for testing

# Define the constraint coefficients
A = [[0, 7, 5], [0, 3, 5], [-1, 1, 0]]
b = [100, 200, -300]

# Define the bounds on the variables
x0_bounds = (0, 36) #parcels LU0
x1_bounds = (0, 42) #parcels LU1
x2_bounds = (0, 22) #parcels LU2
bounds = [x0_bounds, x1_bounds, x2_bounds]

# Solve the linear programming problem
res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='simplex')

# Calculate the total values of B1 and B2
total_B1 = res.x[0] * 7 + res.x[1] * 7 + res.x[2] * 5
total_B2 = res.x[0] * 5 + res.x[1] * 3 + res.x[2] * 5

# Print the solution
print("The optimal values of the variables are: ", res.x)
print("The minimum cost is: ", res.fun)
print("The total value of B1 is: ", total_B1)
print("The total value of B2 is: ", total_B2)

'''These constraints ensure that the sum of the binary variables for parcel LU0 is equal to 1, meaning that parcel LU0 is located in exactly one location. 
The second and third constraints ensure that the binary variables are either 0 or 1, meaning that each parcel is either located at a particular location or not.
I would then need to modify the c and A variables to account for the new binary variables and the costs associated with each location. 
The c variable would be modified to include the cost associated with each possible location, 
and the A variable would be modified to include the constraints associated with each location.

This type of optimization problem is called a mixed-integer linear programming (MILP) problem, 
as it involves both continuous and integer variables. 
These types of problems can be solved using specialized optimization libraries:
-PuLP
-Pyomo
-Gurobi
-CVXOPT

'''




