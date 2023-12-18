"""Loads all cores of CPU"""


import multiprocessing


def load_cpu() -> None:
    """This loop keeps the CPU busy"""

    while True:
        pass


if __name__ == "__main__":
    # Get the number of CPU cores available
    num_cores = multiprocessing.cpu_count()

    # Indicate how much cores should be loaded
    load_this_number_of_cores = num_cores - 3

    # Create a process for each CPU core
    processes = []
    for _ in range(load_this_number_of_cores):
        process = multiprocessing.Process(target=load_cpu)
        process.start()
        processes.append(process)

    # Wait for all processes to complete
    for process in processes:
        process.join()
