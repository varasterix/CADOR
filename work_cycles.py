from pulp import *
import numpy as np
from time import time

# Parameters
Week = [i for i in range(7)]                            # days of week
T = [i for i in range(7)]                               # types of contracts
Night_Shifts = ["N"]                                    # types of night shifts
Day_Shifts = ["M", "J", "S"]                            # types of day shifts
Off_Shifts = ["Jca", "Repos"]                           # types of off shifts
Shifts = Night_Shifts + Day_Shifts + Off_Shifts

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
X = [[[LpVariable("x"+str(i)+"_"+str(j)+"_"+str(r), 0, 1, cat=LpInteger)
       for i in range(len(Shifts))] for j in range(len(Week))] for r in range(len(T))]

# Problem
cador = LpProblem("CADOR", LpMinimize)

# Constraints

# Target Function

# Solving
start_time = time()
status = cador.solve()
print("Problem solved in " + str(round(time()-start_time, 3)) + " seconds")
print(LpStatus[status])
