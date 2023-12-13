"""
The goal is to split an integer into some number of parts, as evenly as possible, without creating floats.

E.x.:

    Split 7 into 3 parts -> [2, 2, 3]
    Split 7 into 7 parts -> [1, 1, 1, 1, 1, 1, 1]
    Split 7 into 8 parts -> [0, 1, 1, 1, 1, 1, 1, 1]
    Split 0 into 2 parts -> [0, 0]
"""


def split_integer(number, parts) -> list[int]:
    """Splits integer into required number of parts

    Args:
        number: Number to split
        parts: How much parts required
    Returns:
        List[with integers, each int represents split part]"""

    # Quotient is a whole number, can be placed into each part (7/3 -> quotient = 2)
    # Reminder is an integer, that will be left (7/3 -> reminder = 1)
    quotient, reminder = divmod(number, parts)

    # Calculating the number of parts, that will go as it is, without adding any extra integer to them
    # 7/3 -> 3 - 1 = 2 -> 2 parts will be integers, equal to quotient -> [2, 2, 3] <- first two 2s
    base_parts_number = parts - reminder

    # Creating a list with calculated number if integers, that does not require to handle any reminder
    # 7/3 -> [2, 2]
    base_parts = base_parts_number * [quotient]

    # Creating a list with extra numbers (7/3 -> [3] <- only part will cary extra 1 (2+1), as reminder is 1)
    extra_parts = reminder * [quotient + 1]

    # Returning a list, consists of base parts and extra parts
    return base_parts + extra_parts


print('7/3 ->', split_integer(7, 3))
print('1/3 ->', split_integer(1, 3))
print('0/3 ->', split_integer(0, 3))
print('2/2 ->', split_integer(2, 2))
print('4/2 ->', split_integer(4, 2))
print('10/3 ->', split_integer(10, 3))
