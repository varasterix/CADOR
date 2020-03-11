from pulp import *
import time
from src.utils import read_team_composition_data_from_csv, export_team_composition_results_as_csv

# Loading team composition csv data file
data_file_path = sys.argv[1]
exportation_path = sys.argv[2]
export_results = bool(sys.argv[3])

# Parameters + Instance dependant Parameters
instance_id, bw, Pp, P80, T, ratios, costs, A, a, week_days, week_indices, N, shifts = \
    read_team_composition_data_from_csv(data_file_path)

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
start_time = time.time()
status = cador.solve()
solving_time = time.time() - start_time

if export_results:
    workforce = [int(value(W[i])) for i in range(len(W))]
    export_team_composition_results_as_csv(exportation_path, instance_id,
                                           LpStatus[status], solving_time, T, ratios, workforce)
