from pulp import *
from time import time

# Parameters
Week = [i for i in range(7)]  # days of week
T = [i for i in range(1, 8)]  # types of contracts
ratios = [1, 0.9, 0.8, 0.75, 0.7, 0.6, 0.5]  # ratio of each type of contract
costs = [1, 0.9143, 0.8571, 0.75, 0.7, 0.6, 0.5]  # cost of each type of contract

# Instance dependant Parameters
bw = 20  # budgeted workforce
N = [{"M": 2, "J": 1, "S": 2, "N": 1} for j in Week]  # workforce needs for every shifts of every day in week
A = [100 for i in T]  # availability for every type of contract
Pp = 0.3  # proportion of partial time contracts
P80 = 0.2  # proportion of 80% contracts in total partial contracts
a = [0 for i in T]  # number of employees already affected for each type of contract

# Variables
W = [LpVariable("W"+str(i), 0, cat=LpInteger) for i in T]  # workforce of every type of contract

# Problem
cador = LpProblem("CADOR", LpMinimize)

# Constraints

# Budgeted workforce respected
cador += lpSum([W[i - 1] * ratios[i - 1] for i in T]) == bw

# Availability respected
for i in T:
    cador += W[i - 1] <= a[i - 1] + A[i - 1]

# Employees cannot work two sundays in a row
cador += lpSum([W[i - 1] * ratios[i - 1] for i in T]) >= 2 * sum([N[6][shift] for shift in N[6]])

# Ratio of partial time contracts
cador += lpSum([W[i - 1] for i in range(2, 8)]) >= Pp * lpSum([W[i - 1] for i in T])

# Ratio of 80% contracts in partial time contracts
cador += W[2] >= P80 * lpSum([W[i - 1] for i in range(2, 8)])

# Target Function
# Minimization of the global cost and maximization of full time
cador += lpSum([W[i - 1] * costs[i - 1] for i in T]) - W[0]

# Solving
start_time = time()
status = cador.solve()
print("Problem solved in " + str(round(time()-start_time, 3)) + " seconds")
print(LpStatus[status])
for i in range(len(W)):
    print("Workforce for type of contract " + str(int(ratios[i]*100)) + "% : " + str(int(value(W[i]))))
