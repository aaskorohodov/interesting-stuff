"""
Challenge: Palindrome Checker

Write a Python function called is_palindrome that takes a string as input and returns True if the string is a
palindrome and False otherwise. A palindrome is a word, phrase, or sequence of characters that reads the same
backward as forward, ignoring spaces, punctuation, and capitalization.


Example:
    > is_palindrome("racecar")
    >> True

    > is_palindrome("A man a plan a canal Panama")
    >> True

    > is_palindrome("python")
    >> False
"""


def is_palindrome(string: str) -> bool:
    """Checks if provided string is a palindrome, which can be a word or a phrase

    Args:
        string: A string to check
    Returns:
        True, if the string is a palindrome"""

    formatted_string = string.replace(' ', '').lower()  # Removing spaces and lowering all symbols
    this_is_a_palindrome = True
    string_length = len(formatted_string)
    for i in range(len(formatted_string) // 2):  # Will only go through a half of the string
        el_a = formatted_string[i]  # Elements from the beginning of the string
        el_b = formatted_string[string_length - (i + 1)]  # Elements from the end of the string
        if el_a != el_b:
            this_is_a_palindrome = False
            break
    return this_is_a_palindrome


def test() -> None:
    cases = {
        1: is_palindrome("racecar") is True,
        2: is_palindrome("A man a plan a canal Panama") is True,
        3: is_palindrome("python") is False
    }

    all_passed = True
    for test_number, result in cases.items():
        if not result:
            all_passed = False
            print(f'Test #{test_number} failed!')

    if not all_passed:
        raise AssertionError
    else:
        print('All tests passed!')


if __name__ == '__main__':
    test()
