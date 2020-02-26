from pulp import *
from time import time

# Parameters
Week = [i for i in range(7)]                            # days of week
T = [i for i in range(7)]                               # types of contracts
Shifts = {                                              # types of shifts
    "Morning": {"code": "M", "beginningTime_t": 6, "duration_D": 7.5, "completionTime_c": 14, "breakDuration": 0.5},
    "Day": {"code": "J", "beginningTime_t": 9, "duration_D": 7.5, "completionTime_c": 17, "breakDuration": 0.5},
    "Evening": {"code": "S", "beginningTime_t": 14, "duration_D": 7.5, "completionTime_c": 22, "breakDuration": 0.5},
    "Night": {"code": "N", "beginningTime_t": 20, "duration_D": 10, "completionTime_c": 6, "breakDuration": None},
}

# Instance dependant Parameters

# Variables

# Problem
cador = LpProblem("CADOR", LpMinimize)

# Constraints

# Target Function

# Solving
start_time = time()
status = cador.solve()
print("Problem solved in " + str(round(time()-start_time, 3)) + " seconds")
print(LpStatus[status])
