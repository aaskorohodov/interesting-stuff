"""This illustrates that List comprehensions are faster than for-loop"""


import random
import time
import matplotlib.pyplot as plt
import numpy as np


def for_loop(n: int) -> list[int]:
    """Creates a list with ints in required range, using for-loop

    Args:
        n: Your range
    Returns:
        List with ints"""

    my_list = []
    for x in range(n):
        my_list.append(x)
    return my_list


def list_comp(n: int) -> list[int]:
    """Creates a list with ints in required range, using list-comprehension

    Args:
        n: Your range
    Returns:
        List with ints"""

    my_list = [y for y in range(n)]
    return my_list


time_benchmark = {
    'for_loop': [],     # Time in seconds, took to create each list using for-loop
    'list_comp': [],    # Time in seconds, took to create each list using list-comprehension
    'list_length': []   # Length of the list, that was created
}

# Creating the same lists, using for-loop and list-comprehension. Saving time took for each method
iterations = 300
for i in range(iterations):
    # Savin length of each list
    numb = random.randint(1_000, 1_000_000)
    time_benchmark['list_length'].append(numb)

    # Generating list using for-loop
    fl_start = time.perf_counter()
    _ = for_loop(numb)
    fl_end = time.perf_counter()
    fl_time = fl_end - fl_start
    time_benchmark['for_loop'].append(fl_time)

    # Generating the same list using list-comp
    lc_start = time.perf_counter()
    _ = list_comp(numb)
    lc_end = time.perf_counter()
    lc_time = lc_end - lc_start
    time_benchmark['list_comp'].append(lc_time)

    # Printing iterations
    iteration = i + 1
    if iteration % 10 == 0:
        print(f'Iteration #{iteration}/{iterations}')


# Reading benchmarks results
for_loop = time_benchmark['for_loop']
list_comp = time_benchmark['list_comp']
list_length = time_benchmark['list_length']

# Drawing dots, representing each result (time VS list-length)
plt.scatter(list_length, for_loop, color='blue', label='for_loop', s=5, alpha=0.2)
plt.scatter(list_length, list_comp, color='green', label='list_comp', s=5, alpha=0.2)

# Fit polynomial regression models for for_loop and list_comp
degree = 2
coeffs_for_loop = np.polyfit(list_length, for_loop, degree)
coeffs_list_comp = np.polyfit(list_length, list_comp, degree)

# Generate polynomial functions from coefficients
poly_for_loop = np.poly1d(coeffs_for_loop)
poly_list_comp = np.poly1d(coeffs_list_comp)

# Create x values for smooth curve
x_smooth = np.linspace(min(list_length), max(list_length), 100)

# Calculate corresponding y values using polynomial functions
y_smooth_for_loop = poly_for_loop(x_smooth)
y_smooth_list_comp = poly_list_comp(x_smooth)

# Plot trend lines for for_loop and list_comp
plt.plot(x_smooth, y_smooth_for_loop, color='blue', label='Trend line for_loop', linewidth=3.0)
plt.plot(x_smooth, y_smooth_list_comp, color='green', label='Trend line list_comp', linewidth=3.0)

plt.xlabel('List Length')
plt.ylabel('Seconds to generate each list')
plt.title('Execution Time Comparison')
plt.legend()

# Display the plot
plt.show()
