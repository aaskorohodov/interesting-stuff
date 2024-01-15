import multiprocessing
import time

from multiprocessing.managers import SyncManager, ListProxy, DictProxy


def is_prime_range(start: int,
                   end: int,
                   number: int,
                   local_status: DictProxy) -> None:
    """Checks given number for being a Prime, but only in a certain range

    Args:
        start: Number, from which to start checking a given 'number' for being a prime
        end: Number, from which to stop checking a given 'number' for being a prime
        number: Number, that is being checked for being a prime
        local_status: Process-communicator-object"""

    for numb in range(start, end):
        if not number % numb:  # Condition, when given number is not a prime
            local_status['is_prime'] = False
            local_status['finished'] = True
            return

        # Updating process-communicator-object
        if not numb % 100_000_00:
            local_status['completed_iterations'] += 100_000_00

    # Updating process-communicator-object
    local_status['finished'] = True


def is_prime_parallel(initial_number) -> None:
    """Splits job of iterating over a big value into several processes in attempt to find prime number

    Args:
        initial_number: Number to check for being a prime"""

    if initial_number <= 1:
        print(f'{initial_number} is NOT prime number!')
        return

    num_processes = multiprocessing.cpu_count() - 2   # How many processes to use
    overall_iteration = int(initial_number**0.5) + 1  # We can up to here in checking for prime-number
    step = overall_iteration // num_processes         # Number of parts, to split job into (for each process)

    with multiprocessing.Manager() as manager:
        manager: SyncManager
        status = manager.list()  # List, where data from processes will be stored and read from

        processes = []
        for i in range(num_processes):
            local_status = manager.dict()  # Process-communicator, to get data from process
            local_status['completed_iterations'] = 0
            local_status['is_prime'] = True
            local_status['finished'] = False
            status.append(local_status)

            # Creating segments - splitting iterations steps into several groups (100 -> 0-20, 21-40, 41-60...)
            start = i * step + 2
            end = (i + 1) * step + 2 if i < num_processes - 1 else int(initial_number**0.5) + 1

            process = multiprocessing.Process(target=is_prime_range, args=(start, end, initial_number, local_status))
            processes.append(process)
            process.start()

        # Checking status of each process
        while check_status(status, overall_iteration, initial_number):
            time.sleep(1)

        for proc in processes:
            proc.terminate()


def check_status(status: ListProxy,
                 overall_iteration: int,
                 initial_number: int) -> bool:
    """Checks how each process does and if any found the number is not Prime or if all finished

    Args:
        status: Status (ListProxy) with dicts. Each dict is a status for a single process
        overall_iteration: How many iteration needs to be done overall (in all processes)
        initial_number: Number that we are checking for being a prime
    Returns:
        True, if not completed yet"""

    overall_completed_iterations = 0
    processes_finished = 0  # How many processes are finished (got through all their iterations)
    overall_processes = 0   # How many processes are there
    for l_stat in status:
        l_stat: DictProxy

        # Any of the processes figured out that this is not a prime number
        is_prime = l_stat['is_prime']
        if not is_prime:
            print(f'{initial_number} is NOT prime number!')
            return False

        # Calculating, how many iterations overall are completed
        completed_iterations = l_stat['completed_iterations']
        overall_completed_iterations += completed_iterations

        # Figuring out, if all processes are completed (noone had found, that the initial number is NOT a prime)
        finished = l_stat['finished']
        if finished:
            processes_finished += 1
        overall_processes += 1

    # All processes completed, and non of them figured out that this is not a prime number
    if overall_processes == processes_finished:
        print(f'{initial_number} IS prime number!')
        return False

    # Still need to do some iterations in at least some processes
    print(f'{overall_iteration - overall_completed_iterations} left...')
    return True


if __name__ == '__main__':
    # is_prime_parallel(170141183460469231731687303715884105727)  # Don't do this!
    is_prime_parallel(100000000001)
    is_prime_parallel(18181)
    is_prime_parallel(9223372036854775783)
