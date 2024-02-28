import subprocess
import time
import os
import matplotlib.pyplot as plt

def generate_cnf_file(filename, num_clauses):
    # create file if it doesn't exist
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            # write the p line to the file, the values doesn't matter
            f.write(f"p cnf 5 {num_clauses}\n")
    with open(filename, 'a') as f:
        for i in range(num_clauses):
            # Fill the file with clauses
            clause = ' '.join(str(j) for j in range(1, 11)) + " 0\n"
            f.write(clause)

def measure_runtime(filename):
    start_time = time.time()
    subprocess.run(["python3", "dimacs_formatter.py", filename])
    end_time = time.time()
    return end_time - start_time

def main():
    num_clauses = 1000
    max_iterations = 20

    filename = "cnf.cnf"

    runtime_map = {}

    for i in range(max_iterations):
        generate_cnf_file(filename, num_clauses)
        runtime = measure_runtime(filename)
        runtime_map[num_clauses] = runtime
        num_clauses += 1000

    os.remove(filename)

    x = list(runtime_map.keys())
    y = list(runtime_map.values())

    # Plot the runtime with dots for each entry point.
    plt.plot(x, y, marker='o', label='Runtime')

    plt.xlabel('Number of Clauses (with 10 literals each)')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime vs Number of Clauses')

    # Show the grid to make it easier to read the plot.
    plt.grid(True)

    # 0.1 second is the limit for having a feeling of instant response.
    plt.axhline(y=0.1, color='g', linestyle='-', label='0.1 seconds')

    # 1 second is the limit for having a feeling of slow response.
    plt.axhline(y=1, color='r', linestyle='-', label='1 second')

    plt.legend(loc='upper left')

    plt.show()

    
if __name__ == "__main__":
    main()
