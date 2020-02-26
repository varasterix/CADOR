from pulp import *

# Parameters
Week = [i for i in range(7)]                            # days of week
T = [i for i in range(7)]                               # types of contracts
ratios = [1, 0.9, 0.8, 0.75, 0.7, 0.6, 0.5]             # ratio of each type of contract
costs = [1, 0.9143, 0.8571, 0.75, 0.7, 0.6, 0.5]        # cost of each type of contract

# Instance dependant Parameters
bw = 20                                                 # budgeted workforce
N = [[2, 2] for j in Week]                              # workforce Needs for every day and night of every day in week
A = [100 for i in T]                                    # availability for every type of contract
Pp = 0.3                                                # proportion of partial time contracts
P80 = 0.2                                               # proportion of 80% contracts in total partial contracts
a = [0 for i in T]                                      # number of employees already affected for each type of contract

# Variables
W = [LpVariable("W"+str(i), 0, cat=LpInteger) for i in T]     # workforce of every type of contract

# Problem
cador = LpProblem("CADOR", LpMinimize)

# Constraints
cador += lpSum([W[i] * ratios[i] for i in T]) == bw     # budgeted workforce respected
for i in T:
    cador += W[i] <= a[i] + A[i]                        # availability respected
cador += lpSum([W[i] * ratios[i] for i in T]) >= \
         2 * (N[6][0] + N[6][1])                        # employees cannot work two sundays in a row
cador += lpSum([W[i] for i in range(1, 7)]) >= \
         Pp * lpSum([W[i] for i in T])                  # ratio of partial time contracts
cador += W[2] >= \
         P80 * lpSum([W[i] for i in range(1, 7)])       # ratio of 80% contracts in partial time contracts

# Target Function
cador += lpSum([W[i] * costs[i] for i in T]) - W[0]     # minimization of the global cost and maximization of full time

# Solving
status = cador.solve()
print(LpStatus[status])
for i in range(len(W)):
    print("Workforce for type of contract " + str(int(ratios[i]*100)) + "% : " + str(int(value(W[i]))))
