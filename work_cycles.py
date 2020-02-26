from pulp import *
from time import time

# Parameters

# Instance dependant Parameters

# Variables
X = [[[LpVariable("x"+str(i)+"_"+str(j)+"_"+str(r), 0, 1, LpInteger)
       for i in range(4)] for j in range(7)] for r in range(7)]
HCR = [LpVariable("Hc"+str(i), 0, cat=LpInteger) for i in range(7)]

# Problem
cador = LpProblem("CADOR", LpMinimize)

# Constraints

# Target Function

# Solving
start_time = time()
status = cador.solve()
print("Problem solved in " + str(round(time()-start_time, 3)) + " seconds")
print(LpStatus[status])
