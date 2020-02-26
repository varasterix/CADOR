from pulp import *
from time import time

# Parameters

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
