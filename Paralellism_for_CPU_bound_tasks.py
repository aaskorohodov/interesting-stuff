"""
This code illustrates, how fast CPU-bounded tasks are executed using async/await, threading and multiprocessing.

There are 2 functions to be executed, which plays the role of actual job that a program may do:

    - cpu_bound_task()
    - not_to_much_cpu_bounded_task()

First is actually heavy one, it requires some calculation power, while the second one is lighter and is executed 100
times faster. You will se that:

    - async/await and threading works about the same in speed
    - multiprocessing is much faster, when there are a lot of calculations
    - multiprocessing is slower, when there is not many calculation (because it has to create processes)
"""


import time
import asyncio
import threading
import multiprocessing


# CPU-bound function
def cpu_bound_task(data_segment: list[list[int]]) -> str:
    """Simulate a CPU-bound computation

    Args:
        data_segment: Some imaginary data
    Returns:
        Some imaginary result"""

    for _ in range(100_000_000):  # <- A lot of operations
        pass
    return f"Processed segment: {data_segment}"


# NOT CPU-bound function (relatively light function)
def not_to_much_cpu_bounded_task(data_segment: list[list[int]]) -> str:
    """Simulate some light calculations, bot too much CPU-bounded

    Args:
        data_segment: Some imaginary data
    Returns:
        Some imaginary result"""

    for _ in range(1_000_000):  # <- Not too many operations
        pass
    return f"Processed segment: {data_segment}"


# Async/await approach
async def async_execution(some_data: list[list[int]], function: callable) -> list[str]:
    """Executes some number of operations in parallel using threads

    *The number of parallel calls for the 'function' will be equal to the number of CPU-cores. This is made, so that
    each approach will make the same number of parallel calls, so they all be in equal circumstances.

    Args:
        some_data: Some imaginary data
        function: Function, that will be executed in parallel
    Returns:
        Some imaginary result"""

    loop = asyncio.get_event_loop()
    tasks = [loop.run_in_executor(None, function, segment) for segment in some_data]
    results = await asyncio.gather(*tasks)
    return results


# Threading approach
def threading_execution(some_data: list[list[int]], function: callable) -> list[str]:
    """Executes some number of threads in parallel

    *The number of threads will be equal to the number of CPU-cores. This is made, so that
    each approach will make the same number of parallel calls, so they all be in equal circumstances.

    Args:
        some_data: Some imaginary data
        function: Function, that will be executed in parallel
    Returns:
        Some imaginary result"""

    threads = []
    results = []
    for segment in some_data:
        thread = threading.Thread(target=lambda s: results.append(function(s)), args=(segment,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results


# Multiprocessing approach
def multiprocessing_execution(some_data: list[list[int]], function: callable) -> list[str]:
    """Executes some number of processes in parallel

    *The number of processes will be equal to the number of CPU-cores. This is made, so that
    each approach will make the same number of parallel calls, so they all be in equal circumstances.

    Args:
        some_data: Some imaginary data
        function: Function, that will be executed in parallel
    Returns:
        Some imaginary result"""

    with multiprocessing.Pool(processes=len(some_data)) as pool:
        results = pool.map(function, some_data)
    return results


def run_all_approaches(load_function: callable) -> None:
    """Executes provided function (load) in 3 different approaches

    3 different approaches are:
        - async/await call
        - threading.Thread
        - multiprocessing

    Args:
        load_function: Function to be executed"""

    # Measure time for async/await approach
    start_time = time.time()
    asyncio.run(async_execution(data_segments, load_function))
    async_time = time.time() - start_time
    print(f"\t- Async/Await execution time: {async_time} seconds")

    # Measure time for threading approach
    start_time = time.time()
    threading_execution(data_segments, load_function)
    threading_time = time.time() - start_time
    print(f"\t- Threading execution time: {threading_time} seconds")

    # Measure time for multiprocessing approach
    start_time = time.time()
    multiprocessing_execution(data_segments, load_function)
    multiprocessing_time = time.time() - start_time
    print(f"\t- Multiprocessing execution time: {multiprocessing_time} seconds")
    print('---------------------------------------------------------------')


if __name__ == "__main__":
    # Generate some imaginary data, divided into segments (segments are equal to the number of CPU-cores)
    num_cores = multiprocessing.cpu_count()
    data = list(range(num_cores))  # Imaginary data, that could be calculated into something else
    segment_size = len(data) // num_cores  # Split the data into several segments
    data_segments: list[list[int]] = [data[i:i + segment_size] for i in range(0, len(data), segment_size)]

    '''
    data_segments is a list[list[int]], where the number of inner lists is equal to the number of cores. Ints inside
    nested lists does not play any role, but they are imitating some data, that should be calculated into something
    we want.
    
    Each approach (async/await, threading and multiprocessing) will create as many parallel tasks, as there are nested
    lists, so that each approach will be in the same imaginary situation. It would not be fair, if some approach would
    have 10 parallel operations, while some other would have 20.
    '''

    print('\nExecuting CPU-bounded tasks with 3 different approaches:')
    run_all_approaches(cpu_bound_task)

    print('\nExecuting *NOT* CPU-bounded (lighter function) tasks with 3 different approaches:')
    run_all_approaches(not_to_much_cpu_bounded_task)
