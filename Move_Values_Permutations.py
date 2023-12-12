"""
The goal is to move all elements that meet some criteria (e.x. all zeros) to the end of the list

For example:

    my_list = [1, 2, 3, 0, 4, 0]
    results = [1, 2, 3, 4, 0, 0]
"""


import time
import random


def long_approach(array: list[int]) -> list[int]:
    """Removing and then inserting an element into the end of a list, if it meets criteria

    Args:
        array: Initial list
    Returns:
        List, with all zeros moved at the end"""

    for i in array:             # O(n)
        if i == 0:
            array.remove(i)     # Another up to O(n), inside the loop, which is already O(n)
            array.append(i)

    return array


def fast_approach(array: list[int]) -> list[int]:
    """Removing and then inserting an element into the end of a list, if it meets criteria

    Args:
        array: Initial list
    Returns:
        List, with all zeros moved at the end"""

    new_array = []
    counter = 0
    for el in array:            # O(n)
        if el == 0:
            counter += 1
            continue
        new_array.append(el)    # O(1)

    for i in range(counter):    # O(n), but outside the first loop
        new_array.append(0)     # O(1)

    return new_array


# Generating list with random numbers (from 0 to 9)
list_length = 200_000
my_list = [random.randint(0, 9) for _ in range(list_length)]

t1_start = time.perf_counter()
long_approach_results = long_approach(my_list)
t1_end = time.perf_counter()
long_approach_time = t1_end - t1_start
print(f'Long approach took: {long_approach_time} seconds')

t2_start = time.perf_counter()
fast_approach_results = fast_approach(my_list)
t2_end = time.perf_counter()
fast_approach_time = t2_end - t2_start
print(f'Long approach took: {fast_approach_time} seconds')

if long_approach_results == fast_approach_results:
    print('Both results are equal!')
