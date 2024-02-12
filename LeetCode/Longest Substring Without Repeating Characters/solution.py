def length_of_longest_substring(string: str) -> int:
    """Finds longest substring without repeating characters, in a given string

    Args:
        string: String, to find longest substring in
    Returns:
        Length of the longest substring without repeating characters"""

    unique_symbols_in_current_substring = set()
    current_substring_length = 0
    max_registered_length = 0
    for symbol in string:
        if symbol not in unique_symbols_in_current_substring:
            unique_symbols_in_current_substring.add(symbol)
            current_substring_length += 1
        else:
            unique_symbols_in_current_substring = set(symbol)
            max_registered_length = max(current_substring_length, max_registered_length)
            current_substring_length = 1

    return max_registered_length


print(length_of_longest_substring('abcabcbb'))
print(length_of_longest_substring('bbbbb'))
print(length_of_longest_substring('pwwkew'))
