def two_sum(given_numbers: list[int], target_number: int) -> list[int, int]:
    """Finds out, how to get target_number from 2 numbers in a given_numbers

    Solution is to iterate over given_numbers, and for each number - find out how much we need to add to it, to get
    target_number, for example:
        target_number = 10
        some_number_from_list = 2
        we_need = 2 + 9 => we need 8

    Now, knowing that we need 8, we can check, if 8 is in given_numbers. We already know that 2 is there, so if 8
    is also there - here are our numbers.

    Args:
        given_numbers: List of numbers, may not be sorted, must NOT contain duplicates
        target_number: Target number

    Raises:
        ValueError: In case given_numbers does not have a pair of numbers to create target_number
    Returns:
        List with 2 integers, representing indices in nums, from which target is summed"""

    nums_with_indices = {num: index for index, num in enumerate(given_numbers)}  # [2, 7, 11] -> {2: 0, 7: 1, 11: 3}

    for index_1 in range(len(given_numbers)):
        random_number = given_numbers[index_1]

        if random_number >= target_number:
            continue

        how_much_till_target = target_number - random_number
        we_need_the_same_number_till_target = how_much_till_target == target_number / 2
        if (how_much_till_target in nums_with_indices) and not we_need_the_same_number_till_target:
            index_2 = nums_with_indices[how_much_till_target]
            return [index_1, index_2]

    raise ValueError('Your initial does not have a pair of numbers, to create target_number!')


nums = [2, 7, 11, 15]
target = 9
expected_result = [0, 1]
actual_result = two_sum(nums, target)
assert expected_result == actual_result

nums = [2, 10]
target = 12
expected_result = [0, 1]
actual_result = two_sum(nums, target)
assert expected_result == actual_result

nums = [3, 2, 4]
target = 6
expected_result = [1, 2]
actual_result = two_sum(nums, target)
assert expected_result == actual_result

nums = [2, 7, 11, 15, 16, 25, 145, 1, 745, 55, 6, 254, 88]
target = 256
expected_result = [0, 11]
actual_result = two_sum(nums, target)
assert expected_result == actual_result
