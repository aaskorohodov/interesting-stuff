"""
The most time-efficient way of checking if a number is prime. Not 100% accurate, and I don't really know how and
why it works. But it does!
"""


import random


def miller_rabin_primality_test(candidate, num_iterations=5):
    """Performs Miller-Rabin primality test on a given candidate.

    Args:
        candidate: The number to test for primality.
        num_iterations: The number of iterations for the test. Higher values improve accuracy.

    Returns:
        True if the candidate is likely prime, False otherwise."""

    # Handle base-cases
    if candidate == 2 or candidate == 3:
        return True
    if candidate % 2 == 0:
        return False

    # Express (candidate - 1) as 2^r * s, where s is odd
    r, s = 0, candidate - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    # Perform Miller-Rabin test with num_iterations rounds
    for _ in range(num_iterations):
        # Choose a random witness in the range (2, candidate - 2)
        witness = random.randint(2, candidate - 2)

        # Compute x = witness^s % candidate
        x = pow(witness, s, candidate)

        # Check if x is congruent to 1 or -1 (mod candidate)
        if x == 1 or x == candidate - 1:
            continue

        # Square x r-1 times and check if the result is congruent to -1 (mod candidate)
        for _ in range(r - 1):
            x = pow(x, 2, candidate)
            if x == candidate - 1:
                break
        else:
            return False  # Not prime if the loop completes without finding -1

    return True  # Likely prime after all iterations


print(miller_rabin_primality_test(170141183460469231731687303715884105727, num_iterations=10000))
