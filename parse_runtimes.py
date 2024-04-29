import os
import plotter

def getRuntimesMap():
    runtime_map = {}
    txt_files_directory = input("Please enter the name of the directory which holds your txt files. Must be in this project's root dir.\n")
    file_list = sorted(os.listdir(txt_files_directory))
    for file_name in file_list:
        block_name = file_name.split(".")[0]
        with open(txt_files_directory + "/" + file_name, "r") as file:
            lines = file.readlines()
            runtime = int(lines[len(lines)-1].split(":")[1].split(".")[0].strip())
            runtime_map.update({block_name: runtime})
    return runtime_map

def getAverageRuntime(runtime_list: dict):
    sum = 0
    for runtime in runtime_list.values():
        sum += runtime
    return sum / len(runtime_list)

runtime_map = getRuntimesMap()
avg_runtime = getAverageRuntime(runtime_map)

solver_name = input("Enter used solver's name\n")
chart_name = input("Enter your save file's name\n")
plotter.plotSolverResults(runtime_map.keys(), runtime_map.values(), solver_name, chart_name, avg_runtime)