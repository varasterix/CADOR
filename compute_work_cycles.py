import subprocess
import src.constants as constants

planning_csv_data_file_path = 'data/planning_data_file_0.csv'
exportation_file_path = constants.EXPORTATION_REPOSITORY_PATH
export_results = 1  # boolean

if __name__ == "__main__":
    python_script = "work_cycles_model.py"
    solver_args = ["python", python_script,
                   planning_csv_data_file_path, exportation_file_path, str(export_results)]
    subprocess.call(args=solver_args)
