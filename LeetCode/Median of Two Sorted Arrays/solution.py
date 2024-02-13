class CustomList(list):
    """Custom list with additional attributes, to read element after an element convenient

    Attributes:
        pointer: Index of self, to keep track of the current element
        current_value: Value under current pointer
        list_completed: True, if there are no more values"""

    def __init__(self, my_list: list):
        """Init

        Args:
            my_list: Any list"""

        super().__init__(my_list)
        self.pointer: int = 0
        self.current_value: int = self[self.pointer]
        self.list_completed = False

    def get_to_next_value(self):
        """Changes pointer to the next value. Sets flag, in case there are no more values"""

        try:
            self.pointer += 1
            self.current_value = self[self.pointer]
        except IndexError:
            self.list_completed = True


class ListCombiner:
    """Combines two lists and finds median in result"""

    def combine_lists_saving_sorting(self, *your_lists: list[int]) -> list[int]:
        """Combines two lists into single one, and saves sorting of the result, without resorting result

        Args:
            your_lists: Any number of lists, each sorted
        Returns:
            Combined list, sorted"""

        non_empty_lists = self._remove_empty_lists(your_lists)
        custom_lists = self._create_custom_list(non_empty_lists)
        resulting_list = []
        while custom_lists:
            self._add_one_value_to_result(custom_lists, resulting_list)

        return resulting_list

    def get_median(self, your_list: list[int]) -> int | float:
        """Gets median value from a given list

        Args:
            your_list: List, to get median from
        Returns:
            Median value"""

        number_of_elements = len(your_list)

        # Odd number => there is a median value, no calculations needed
        if number_of_elements % 2:
            median_index = number_of_elements // 2 + 1
            median_value = your_list[median_index]
            return median_value

        # Even number => median consists of 2 values (Example: [1, 2, 3, 4])
        else:
            first_median_index = number_of_elements // 2                    # [1, 2, 3, 4] -> index = 1
            second_median_index = first_median_index + 1                    # [1, 2, 3, 4] -> index = 2
            first_median_value = your_list[first_median_index]              # [1, 2, 3, 4] -> 2 (number)
            second_median_value = your_list[second_median_index]            # [1, 2, 3, 4] -> 3 (number)
            median_value = (first_median_value + second_median_value) / 2   # (2 + 3) / 2  -> 2.5 (median)

            return median_value

    def _create_custom_list(self, your_lists: list[list[int]]) -> list[CustomList]:
        """Creates custom list from provided regular lists

        Args:
            your_lists: Lists, which will be converted into custom lists
        Returns:
            List of Custom lists"""

        custom_lists = []
        for your_list in your_lists:
            custom_list = CustomList(your_list)
            custom_lists.append(custom_list)

        return custom_lists

    def _remove_empty_lists(self, lists: tuple[list[int]]) -> list[list[int]]:
        """Removes empty lists from provided

        Args:
            lists: Tuple with lists
        Returns:
            List of lists, where each inner list is not empty"""

        not_empty_lists = []
        for your_list in lists:
            if your_list:
                not_empty_lists.append(your_list)

        return not_empty_lists

    def _get_min_value(self, custom_lists: list[CustomList]) -> CustomList:
        """Gets min current_value from provided CustomLists

        Args:
            custom_lists: List with CustomList, from which min_value will be returned
        Returns:
            Instance of CustomList with min CustomList.current_value"""

        return min(custom_lists, key=lambda yur_list: yur_list.current_value)

    def _add_one_value_to_result(self, custom_lists: list[CustomList], resulting_list: list[int]) -> None:
        """Adds one value to the result_list, taken from provided CustomList.

        Args:
            custom_lists: List with CustomList, from which min-value will be taken
            resulting_list: Resulting list, that we are currently building"""

        min_value_list = self._get_min_value(custom_lists)
        resulting_list.append(min_value_list.current_value)
        min_value_list.get_to_next_value()

        if min_value_list.list_completed:
            self._remove_custom_list(custom_lists, min_value_list)

    def _remove_custom_list(self, custom_lists: list[CustomList], min_value_list: CustomList) -> None:
        """Removes min_value_list from custom_lists, as min_value_list is completed and there are no more values in it

        Args:
            custom_lists: All CustomLists, from which we are combining result_list
            min_value_list: CustomList with minimum value"""

        min_value_list_index = custom_lists.index(min_value_list)
        custom_lists.pop(min_value_list_index)


list_1 = [i for i in range(1_000_000)]
list_2 = [i for i in range(5_000_00)]
list_combiner = ListCombiner()
combined_list = list_combiner.combine_lists_saving_sorting(list_1, list_2)
median = list_combiner.get_median(combined_list)
print(median)
