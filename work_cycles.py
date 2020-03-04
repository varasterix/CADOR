from pulp import *
import numpy as np
from time import time

# Parameters
Week = [i for i in range(7)]                            # days of week
T = [i for i in range(7)]                               # types of contracts
Night_Shifts = {"N": 3}                                 # types of night shifts
Day_Shifts = {"M": 0, "J": 1, "S": 2}                   # types of day shifts
Off_Shifts = {"Jca": 4, "Repos": 5}                     # types of off shifts
Shifts = {**Night_Shifts, **Day_Shifts, **Off_Shifts}

# Instance dependant Parameters
beginningTime_t = {"M": 6, "J": 9, "S": 14, "N": 20}
completionTime_c = {"M": 14, "J": 17, "S": 22, "N": 6}
duration_D = {"M": 7.5, "J": 7.5, "S": 7.5, "N": 10}
breakDuration = {"M": 0.5, "J": 0.5, "S": 0.5}
N = [{"M": 2, "J": 1, "S": 2, "N": 1} for j in Week]    # workforce Needs for every shifts of every day in week
Eff = [3 for i in T]                                    # number of employees already affected for each type of contract
# Work cycles length (not a variable in this model)
HC_r = [eff for eff in Eff]
# Overall work cycle length
HC = int(np.lcm.reduce(HC_r))
# Horizon of the plannings creation

# Variables
X = [[[[LpVariable("x" + str(i) + "_" + str(j) + "_" + str(r) + "_" + str(e_r), 0, 1, cat=LpInteger)
        for i in range(len(Shifts))] for j in range(1, len(Week) * HC)] for e_r in range(Eff[r])] for r in
     range(len(T))]

# Problem
cador = LpProblem("CADOR", LpMinimize)

# Constraints
# Constraint 0: Repetition of the patterns for each type of contract
for r in T:
    for e_r in range(Eff[r]):
        for i in range(len(Shifts)):
            for j in range(1, HC_r[r]):
                if HC_r[r] != HC:
                    for k in range(1, HC // HC_r[r]):
                        cador += X[i][j][e_r][r] == X[i][j + k * HC_r[r]][e_r][r]

# Constraint 1.a: respect of needs
for i, shift in enumerate(Shifts):
    for j in range(len(Week)):
        for k in range(HC):
            cador += lpSum([lpSum([X[i][j][r] for e_r in range(Eff[r])]) for r in T]) >= N[j + k * len(Week)][shift]

# Constraint 1.b: only one shift per day per person
for r in T:
    for e_r in range(Eff[r]):
        for j in range(1, len(Week)*HC_r[r]):
            cador += lpSum([X[i][j][r] for i in range(len(Shifts))]) == 1

# Constraint 1.c: no single work day
for r in T:
    for e_r in range(Eff[r]):
        for j in range(1, HC_r[r] - 1):
            temp1 = 0
            temp2 = 0
            temp3 = 0
            for s in {**Day_Shifts, **Night_Shifts}:
                temp1 += X[Shifts[s]][j + 1][e_r]
                temp2 += X[Shifts[s]][j][e_r]
                temp3 += X[Shifts[s]][j + 2][e_r]
            cador += temp1 <= temp2 + temp3

# Constraint 1.d: Maximum of 5 consecutive days of work
for r in T:
    for e_r in range(Eff[r]):
        for j in range(1, len(Week)*HC_r[r] - 4):
            cador += lpSum([lpSum([X[Shifts[s]][j + k][e_r][r]
                                   for s in {**Day_Shifts, **Night_Shifts}]) for k in range(0, 6)]) <= 5

# Constraint 1.e: same shift on saturday as on sunday
for r in T:
    for er in range(Eff[r]):
        for k in range(er):
            for i in range(len(Shifts)):
                cador += X[i][k*5][er] == X[i][k*6][er]

# Target Function

# Solving
start_time = time()
status = cador.solve()
print("Problem solved in " + str(round(time() - start_time, 3)) + " seconds")
print(LpStatus[status])
