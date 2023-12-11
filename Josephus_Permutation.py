"""
The initial idea:

Groups of men got into a cave, trapped by enemy soldiers. Men decided not to surrender, but to kill themselves. They
will get into a circle, and start killing people one by one with the step n, until there would be only 1 man left,
who will execute himself. One of the man decided to stay alive and instead surrender. To do so that, this man needs to
figure out, where should he stand in this circle, if the step (n) with which they will kill people is known.


Pythonic idea:

Given a list of sorted elements, we will remove elements one by one. The step will be any selected number (n), and
the first element to remove will be that n'h element. When we get to the end of the list, while the list is not yet
empty, we will return to the list's beginning, just like going in cycles.

Popped elements will be stored in another list, so that other list will be permutation of the first list, where
elements just shifted onto other positions. In a nutshell, we need to figure out, what would be the last element in
a new, permuted list.
"""

import time

from collections import deque


def permutation_slow(array: list[int], step: int) -> int:
    """Returns position of initial list, that would be at the last index in permuted list

    Args:
        array: Initial array of elements
        step: Step, in which elements will be popped into permuted list
    Returns:
        Element from initial list, that would be the at the end of permuted list"""

    permutation = []
    current_index = 0
    while array:
        current_index = (current_index + step - 1) % len(array)  # Let us jump to the beginning of the list
        removed_item = array.pop(current_index)
        permutation.append(removed_item)

    return permutation[-1]


men_in_cave = 1_000_000
arr = [man + 1 for man in range(men_in_cave)]
stp = 3
start_time = time.perf_counter()
where_to_stand_to_be_the_last = permutation_slow(arr, stp)
end_time = time.perf_counter()
print(f'where_to_stand_to_be_the_last = {where_to_stand_to_be_the_last}')
print(f'Time took: {end_time - start_time}')

'''
The problem is this "removed_item = array.pop(current_index)". List in Python are stored in memory in the way,
where we know the beginning address of the list, and we can calculate the index we are looking for, because each next
element would be the next cell. So we need to track pointer, that indicate the first element, calculate where should
this pointer be in order to get required element, and get to this address in memory.

To keep this structure after popping one element, Python needs to move all the rest elements to the left. This takes 
O(n) operations, which is fine, but as we keep integrating over the whole list, time exceeds to O(n²), because for each
element to be popped (O(n)) we need to move other all other elements (another O(n)).

To make this faster, we can use deque, which is a queue, where we know the position of the first and last elements. In
this array, elements are stored in random memory locations, and each element have a pointer, indicating the next and 
previous elements, and the deque itself tracks only the first element. So, knowing the first element, we can see
its pointer to the last element, and the second element.

To get an element from a deque of some index, Python needs to rotate this deque's first and last elements, till 
it gets to the desired element. This does not require to iterate over all elements after we popped ay one, instead 
it starts from the first element and goes to the one wee need, than it changes deque's value of the first element to be
this element, and that it.

Popping elements from deque is O(1).
'''


def permutation_fast(array: list[int], step: int) -> int:
    """Returns position of initial list, that would be at the last index in permuted list

    Args:
        array: Initial array of elements
        step: Step, in which elements will be popped into permuted list
    Returns:
        Element from initial list, that would be the at the end of permuted list"""

    d = deque(array)
    permutation = []
    while d:
        d.rotate(1 - step)
        removed_item = d.popleft()
        permutation.append(removed_item)

    return permutation[-1]


men_in_cave = 1_000_000
arr = [man + 1 for man in range(men_in_cave)]
stp = 3
start_time = time.perf_counter()
where_to_stand_to_be_the_last_2 = permutation_fast(arr, stp)
end_time = time.perf_counter()
print(f'where_to_stand_to_be_the_last = {where_to_stand_to_be_the_last_2}')
print(f'Time took: {end_time - start_time}')
