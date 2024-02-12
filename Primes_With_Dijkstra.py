"""
This code illustrates Dijkstra's approach to gather prime-numbers from 2 to some specific number (or to determine if
a given number is prime). The algorithm itself can be seen here: https://www.youtube.com/watch?v=fwxjMKBMR7s

Its implementations rely on heapq, which can create a heap from any list. This heap is a binary tree, in which we are
only interested in one of its properties - this tree has the lowest element on its top.
"""


import heapq


class PrimeManager:
    """
    Attributes:
        primes_and_their_multiples_pool: list[tuple[prime_multiple, prime]]
        primes: list[prime, prime, prime, ...]
    """

    def __init__(self):
        self.primes_and_their_multiples_pool: list[tuple[int, int]] = []
        self.primes: list[int] = []

    def is_this_number_prime(self, given_number: int) -> None:
        """Determines if the given number is prime

        Args:
            given_number: Number to check if it's prime
        Returns:
            True if given_number is prime"""

        if given_number < 2:
            self._print_result(given_number)
            return

        self.primes_and_their_multiples_pool = [(4, 2)]  # Initial pool (multiple and prime); multiple = prime *squared
        heapq.heapify(self.primes_and_their_multiples_pool)
        self.primes = [2]

        # As we already created case for 2 (2 is prime) => starting from 3
        for number in range(3, given_number + 1):

            # 'number' is not prime => increasing smallest multiple, till it gets to number or higher
            while self._get_smallest_multiple() < number:
                self._increase_smallest_multiple()

            # Increasing smallest multiple, but only once! Due to the logic of Dijkstra's itself
            if self._get_smallest_multiple() == number:
                self._increase_smallest_multiple()

            else:
                self._add_new_prime(number)

        self._print_heap_structure(self.primes_and_their_multiples_pool)
        self._print_result(given_number)

    def _increase_smallest_multiple(self):
        """Increases smallest multiply by adding its prime to it"""

        multiple, prime = heapq.heappop(self.primes_and_their_multiples_pool)
        heapq.heappush(self.primes_and_their_multiples_pool, (multiple + prime, prime))

    def _add_new_prime(self, new_prime: int) -> None:
        """Adds new prime into

        Args:
            new_prime: New prime to add"""

        self.primes.append(new_prime)

        primes_multiple = new_prime * new_prime
        heapq.heappush(self.primes_and_their_multiples_pool, (primes_multiple, new_prime))

    def _get_smallest_multiple(self) -> int:
        """Returns smallest multiple

        Notes:
            As self.primes_and_their_multiples_pool is a heapq – smallest multiple is always at index 0. This heap
            automatically sorts its structure, each time new element is added or removed."""

        return self.primes_and_their_multiples_pool[0][0]

    # Prints

    def _print_result(self, given_number: int) -> None:
        """Prints result

        Args:
            given_number: Initially provided number, which was tested"""

        if given_number in self.primes:
            print(f'{given_number} is prime')
        else:
            print(f'{given_number} is NOT prime')

    def _print_heap_structure(self, heap: list) -> None:
        """Prints heap's structure, to better understand it visually

        Args:
            heap: List, converted to heap"""

        print('--------- Heap structure ---------')
        self._print_levels_recursively(0, 0, heap)
        print('--------- Heap structure ends ---------\n')

    def _print_levels_recursively(self, node_index: int, level: int, heap: list) -> None:
        """Recursively prints each level of the heap

        Args:
            node_index: Index of the current node
            level: Current level (heap is a tree, so this is a tree level)
            heap: Heap itself"""

        if node_index < len(heap):
            self._print_levels_recursively(2 * node_index + 2, level + 1, heap)
            print("   " * level + str(heap[node_index]))
            self._print_levels_recursively(2 * node_index + 1, level + 1, heap)


PrimeManager().is_this_number_prime(28)
