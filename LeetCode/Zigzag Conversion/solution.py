from typing import Optional


class Solution:
    """Solution to zigzag-conversion

    Attributes:
        matrix: List, emulating matrix with zigzag-string
        last_row_index_in_matrix: Index for the last row in our matrix
        current_row: Current row, that we are working with in a matrix, when filling it
        current_col: Current column, that we are working with in a matrix, when filling it
        filling_matrix_down: Indicating, if we are currently filling matrix down
        filling_matrix_up: Indicating, if we are currently filling matrix up
        num_rows: Number of rows, that we were requested to fill
        input_string: String to convert into zigzag-pattern"""

    def __init__(self):
        """Init"""

        self.matrix:                   Optional[list[list[str]]] = None
        self.last_row_index_in_matrix: Optional[int]             = None
        self.current_row:              int                       = 0
        self.current_col:              int                       = 0
        self.filling_matrix_down:      bool                      = True
        self.filling_matrix_up:        bool                      = False
        self.num_rows:                 Optional[int]             = None
        self.input_string:             Optional[str]             = None

    def convert(self,
                input_string: str,
                num_rows: int) -> str:
        """Converts string into zigzag string

        Examples:
            MyStringToConvert, rows=4 ->
            m    n    n
            y  i g  o v
            s r  t c  e t
            t    o    r
            -> mnnyigovsrtcettor
        Args:
            input_string: String to convert
            num_rows: Number of rows to make
        Returns:
            String, converted into zigzag-mode"""

        print(f'Received this string: {input_string}')
        self._reset_attributes()

        self.input_string = input_string
        self.num_rows = num_rows

        if self._check_if_string_too_short():
            return self.input_string

        self._create_empty_matrix()
        self._fill_matrix()

        self._print_matrix()
        return self._convert_matrix_into_string()

    def _check_if_string_too_short(self) -> bool:
        """Checks if string os too short

        Returns:
            True, if there is no need to fill matrix and we can return input-string as it is"""

        if self.num_rows == 1 or self.num_rows >= len(self.input_string):
            return True
        return False

    def _create_empty_matrix(self) -> None:
        """Creates an empty matrix with sizes, required for this string and requested row-number"""

        matrix = []
        for _row in range(self.num_rows):
            row_in_matrix = ['' for _letter in range(len(self.input_string))]
            matrix.append(row_in_matrix)

        self.matrix = matrix

    def _fill_matrix(self) -> None:
        """Fills matrix with string in zigzag-pattern"""

        self.last_row_index_in_matrix = self.num_rows - 1

        for letter in self.input_string:
            self.matrix[self.current_row][self.current_col] = letter
            self._update_current_matrix_coordinates()

    def _update_current_matrix_coordinates(self) -> None:
        """Updates indexes of row and column, to fill next letter"""

        if self.filling_matrix_down:
            last_row_reached = (self.current_row == self.last_row_index_in_matrix)
            if last_row_reached:
                # Getting 1 row up and 1 column right
                self.filling_matrix_down = False
                self.filling_matrix_up   = True
                self.current_row -= 1
                self.current_col += 1
            else:
                # Getting 1 row down
                self.current_row += 1

        elif self.filling_matrix_up:
            first_row_reached = (self.current_row == 0)
            if first_row_reached:
                self.filling_matrix_down = True
                self.filling_matrix_up   = False
                self.current_row += 1
            else:
                self.current_row -= 1
                self.current_col += 1

    def _convert_matrix_into_string(self) -> str:
        """Converts matrix into a single string, read row-by-row

        Returns:
            Matrix, converted into single string, which is created by reading matrix row-by-row"""

        single_string = ''.join([''.join(row) for row in self.matrix])
        return single_string

    def _print_matrix(self) -> None:
        """Prints matrix in zigzag-pattern

        Examples:
            P  I  N
            A LS IG
            YA HR
            P  I
        """

        print('Your matrix is:')
        print('--- Matrix ---')
        for row in self.matrix:
            print(''.join(letter if letter else ' ' for letter in row))
        print('--- End ---')

    def _reset_attributes(self) -> None:
        """Resets attributes to allow instance on this class to be reused"""

        self.matrix                   = None
        self.last_row_index_in_matrix = None
        self.current_row              = 0
        self.current_col              = 0
        self.filling_matrix_down      = True
        self.filling_matrix_up        = False
        self.num_rows                 = None
        self.input_string             = None


solution = Solution()

result = solution.convert("PAYPALISHIRING", 3)
assert result == 'PAHNAPLSIIGYIR'
print(f'Result is: {result}')
print('---------------\n')

result = solution.convert("PAYPALISHIRING", 4)
assert result == 'PINALSIGYAHRPI'
print(f'Result is: {result}')
print('---------------\n')

result = solution.convert("A", 1)
assert result == 'A'
print(f'Result is: {result}')
print('---------------\n')
