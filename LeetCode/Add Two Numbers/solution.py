class ReversedListIterator:
    """Can return numbers from a given list in reversed order

    Attributes:
        _reversed_list: List, from which numbers will be returned"""

    def __init__(self, your_list: list[int]):
        """Init

        Args:
            your_list: List, from which numbers will be returned in reversed order"""

        self._reversed_list: list[int] = your_list

    def __iter__(self) -> 'ReversedListIterator':
        """Python's iteration-protocol wants this method to be implemented to return self"""

        return self

    def __next__(self) -> int:
        """Implementing iteration-protocol (what to return)

        Raises:
            StopIteration: When there is no more numbers in self._reversed_list
        Returns:
            Last number from self._reversed_list"""

        if self._reversed_list:
            return self._reversed_list.pop(0)
        else:
            raise StopIteration

    def is_not_empty(self) -> bool:
        """Checks if there are any numbers left"""

        return len(self._reversed_list) > 0


def add_two_numbers_from_reversed_list(list_1: list[int], list_2: list[int]) -> list[int]:
    """Adds two reversed list, as if they were single number each.

    Examples:
        list_1 = [1, 2, 3]  -> 321
        list_2 = [4, 5 ,6]  -> 654
        321 + 654 = 975
        975 -> [5, 7, 9]

    Args:
        list_1: List, representing number in reversed order
        list_2: List, representing number in reversed order

    Returns:
        List, representing a sum of lists from arguments, also in reversed order"""

    iterator_1 = ReversedListIterator(list_1)
    iterator_2 = ReversedListIterator(list_2)
    resulting_number = []
    carry = 0  # 10 + 2 -> 12 -> 'writing down 2, 1 is a carry'

    while (iterator_1.is_not_empty() or iterator_2.is_not_empty()) or carry:
        number_1, number_2 = get_numbers_from_iterators(iterator_1, iterator_2)
        summ = number_1 + number_2 + carry  # 10 + 2 -> 12 + carry (1) -> 13

        ones = summ % 10   # 13 -> ones = 3
        tens = summ // 10  # 13 -> tens = 1
        carry = tens

        resulting_number.append(ones)

    return resulting_number


def get_numbers_from_iterators(*args: iter) -> list[int]:
    """Reads numbers from any number of iterators. In case StopIteration – returns 0 as a number

    Args:
        args: Any number of iterators
    Returns:
        List with number from iterators, where each StopIteration replaced with 0"""

    numbers = []
    for iterator in args:
        try:
            number = iterator.__next__()
            numbers.append(number)
        except StopIteration:
            numbers.append(0)

    return numbers


l1 = [2, 4, 3]
l2 = [5, 6, 4]
expected = [7, 0, 8]
actual = add_two_numbers_from_reversed_list(l1, l2)
assert expected == actual

l1 = [0]
l2 = [0]
expected = [0]
actual = add_two_numbers_from_reversed_list(l1, l2)
assert expected == actual

l1 = [0, 0, 1]
l2 = [0, 1]
expected = [0, 1, 1]
actual = add_two_numbers_from_reversed_list(l1, l2)
assert expected == actual

l1 = [9, 9, 9, 9, 9, 9, 9]
l2 = [9, 9, 9, 9]
expected = [8, 9, 9, 9, 0, 0, 0, 1]
actual = add_two_numbers_from_reversed_list(l1, l2)
assert expected == actual
