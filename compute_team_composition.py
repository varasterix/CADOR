import subprocess
import src.constants as constants

team_composition_csv_data_file_path = 'test/team_composition_data_file_0.csv'
exportation_file_path = constants.EXPORTATION_REPOSITORY_PATH
export_results = 1  # boolean

if __name__ == "__main__":
    python_script = "team_composition_model.py"
    solver_args = ["python", python_script,
                   team_composition_csv_data_file_path, exportation_file_path, str(export_results)]
    subprocess.call(args=solver_args)
