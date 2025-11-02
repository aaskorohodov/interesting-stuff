import time
import multiprocessing


def load_cpu() -> None:
    """This loop keeps the CPU busy"""

    while True:
        pass


def run_for_duration(duration: int) -> None:
    """Run the load for a specified duration in seconds

    Args:
        duration: How long to run test in seconds"""

    start_time = time.time()
    num_cores = multiprocessing.cpu_count()
    load_this_number_of_cores = num_cores - 4
    processes = []

    # Create a process for each CPU core
    for _ in range(load_this_number_of_cores):
        process = multiprocessing.Process(target=load_cpu)
        process.start()
        processes.append(process)

    # Run for the specified duration
    while time.time() - start_time < duration:
        time.sleep(1)  # Sleep for a short duration to avoid busy-waiting
        print(int(duration - (time.time() - start_time)))

    # Terminate all processes after the duration has elapsed
    for process in processes:
        process.terminate()
        process.join()


if __name__ == "__main__":
    # Run the load for 10 minutes (600 seconds)
    run_for_duration(610)
