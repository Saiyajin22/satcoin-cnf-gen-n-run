import matplotlib.pyplot as plt

def plotSolverResults(blocks, runtimes, solver_name, saveFileName: str, avg_runtime, hide_x: bool):
    fig = plt.figure(figsize = (12, 6))
    plt.bar(blocks, runtimes, color ='maroon', width=0.4)
    plt.xlabel("Blocks")
    plt.ylabel("Runtimes in seconds")
    plt.title("Runtime for solver: " + solver_name + " on " + str(len(runtimes)) + " different blocks. Avg: " + str(avg_runtime))

    if hide_x:
        plt.xticks([])

    if len(saveFileName) > 0:
        plt.savefig(saveFileName)
    else:
        plt.show()

# plotSolverResults(
#     ['block_780000', 'block_780001','block_780002','block_780003',],
#     [22, 33,21,40,],
#     "cryptominisat",
#     "blocks_test.png"
#     )