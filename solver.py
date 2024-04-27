import os
import btc_utils
import time

print("Welcome to create sat solver runner script")
cnf_files_directory = input("Please enter the name of the directory which holds your CNF files. Must be in this project's root dir.\n")
sat_solver_results_directory = cnf_files_directory + "_txts"
solver_name = input("Please enter the name of the SAT solver file which will run the solver. (If you use an executable file like manysat in this project's root dir, add './' at the beginning\n")
run_solver_command = solver_name + " " + cnf_files_directory + "/{} > " + sat_solver_results_directory + "/{}"

if not os.path.exists(sat_solver_results_directory):
    os.mkdir(sat_solver_results_directory)
    print(f"Directory '{sat_solver_results_directory}' created.")
else:
    print(f"Directory '{sat_solver_results_directory}' already exists.")

runtime_of_blocks = []
counter = 1
sum_of_runtimes = 0
file_list = sorted(os.listdir(cnf_files_directory))
for filename in file_list:
    start_time = time.time()
    result_txt = filename.split(".")[0] + ".txt"
    command = run_solver_command.format(filename, result_txt)
    print(str(counter) + ". run with command: " + command)
    btc_utils.execute_command_detailed(command)
    counter += 1
    end_time = time.time()
    runtime = end_time - start_time
    sum_of_runtimes += runtime
    runtime_line = "Runtime of solver on " + filename + ": " + str(runtime) + " seconds\n"
    print(runtime_line)
    runtime_of_blocks.append(runtime_line)

    with open(sat_solver_results_directory + "/" + result_txt, "a") as file:
        file.write(runtime_line)

avg_runtime = sum_of_runtimes / counter
avg_runtime_line = "Average runtime of " + solver_name + " over " + str(counter) + " cnf files: " + str(avg_runtime) + "\n"
print(avg_runtime_line)
runtime_of_blocks.append(avg_runtime_line)
with open("avg_runtime.txt", "w") as file:
    file.writelines(runtime_of_blocks)
