from pulp import *
import time
from src.utils import read_planning_data_from_csv, export_team_composition_results_as_csv
from src.workforce import compute_required_workforce

# Loading team composition csv data file
planning_data_file_path = sys.argv[1]
exportation_path = sys.argv[2]
export_results = bool(int(sys.argv[3]))

# Parameters + Instance dependant Parameters
instance_id, year, bw, annual_hours_fix, annual_hours_var, Pp, P80, T, ratios, costs, A, a, Day_Shifts, Night_Shifts, \
    Off_Shifts, week_days, Week, N, beginningTime_t, completionTime_c, duration_D, breakDuration = \
    read_planning_data_from_csv(planning_data_file_path)

# Checking if a budgeted workforce is given. Otherwise, the budgeted workforce required is used.
is_bw_given = False if bw is None else True
if not is_bw_given:
    bw = compute_required_workforce(N, Day_Shifts, Night_Shifts, duration_D, breakDuration, annual_hours_fix,
                                    annual_hours_var, Week, year)

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
    if LpStatus[status] == 'Optimal':
        workforce = [int(value(W[i])) for i in range(len(W))]
        export_team_composition_results_as_csv(exportation_path, instance_id,
                                               LpStatus[status], solving_time, T, ratios, workforce)
    else:
        export_team_composition_results_as_csv(exportation_path, instance_id,
                                               LpStatus[status], solving_time, T, ratios, None)
