import os
import btc_utils
import time

print("Welcome to create sat solver runner script")
cnf_files_directory = input("Please enter the name of the directory which holds your CNF files. Must be in this project's root dir.\n")
sat_solver_results_directory = cnf_files_directory + "_txts"
solver_name = input("Please enter the name of the SAT solver file which will run the solver.\n")
run_solver_command = "./" + solver_name + " " + cnf_files_directory + "/{} > " + sat_solver_results_directory + "/{}"

if not os.path.exists(sat_solver_results_directory):
    os.mkdir(sat_solver_results_directory)
    print(f"Directory '{sat_solver_results_directory}' created.")
else:
    print(f"Directory '{sat_solver_results_directory}' already exists.")

counter = 1
sum_of_runtimes = 0
for filename in os.listdir(cnf_files_directory):
    start_time = time.time()
    result_txt = filename.split(".")[0] + ".txt"
    command = run_solver_command.format(filename, result_txt)
    print(str(counter) + ". run with command: " + command)
    btc_utils.execute_command_detailed(command)
    counter += 1
    end_time = time.time()
    runtime = end_time - start_time
    sum_of_runtimes += runtime
    runtime_line = "Runtime of solver: " + str(runtime) + " seconds"
    print(runtime_line)

    with open(sat_solver_results_directory + "/" + result_txt, "a") as file:
        file.write(runtime_line)

avg_runtime = sum_of_runtimes / counter
avg_runtime_line = "Average runtime of " + solver_name + " over " + str(counter) + " cnf files: " + str(avg_runtime)
print(avg_runtime_line)
with open("avg_runtime.txt", "w") as file:
    file.write(avg_runtime_line)
