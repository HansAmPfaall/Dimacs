import unittest
import dimacs_formatter

class TestDimacsFormatterCnf(unittest.TestCase):
    def test_format_cnf_01(self):
        # Test case for input with a comment
        input_data = "c comment"
        expected_output = "c comment"
        self.assertEqual(dimacs_formatter.format_cnf(input_data), expected_output)

    def test_format_cnf_02(self):
        # Test case for input with problem line
        input_data = "p cnf 3 3"
        expected_output = "p cnf 3 3"
        self.assertEqual(dimacs_formatter.format_cnf(input_data), expected_output)

    def test_format_cnf_03(self):
        # Test case for second problem line
        input_data = "p cnf 3 3"
        expected_output = None
        self.assertEqual(dimacs_formatter.format_cnf(input_data), expected_output)

    def test_format_cnf_04(self):
        # Test case for input with clauses
        input_data = "1 2 - 3 0"
        expected_output = "1 2 -3 0\n"
        self.assertEqual(dimacs_formatter.format_cnf(input_data), expected_output)

    def test_format_cnf_05(self):
        # Test case for empty input
        input_data = ""
        expected_output = None
        self.assertEqual(dimacs_formatter.format_cnf(input_data), expected_output)

    def test_format_cnf_06(self):
        # Test case for input with multiple clauses
        input_data = "1 2 3 04 -5 0-1 -2 -3 0"
        expected_output = "1 2 3 0\n4 -5 0\n-1 -2 -3 0\n"
        self.assertEqual(dimacs_formatter.format_cnf(input_data), expected_output)

    def test_format_cnf_07(self):
        # Test case for input with leading/trailing whitespace
        input_data = "  1 2 3 0  \n"
        expected_output = "1 2 3 0\n"
        self.assertEqual(dimacs_formatter.format_cnf(input_data), expected_output)

    def test_format_cnf_08(self):
        # Test case for input with missing terminating zero
        input_data = "  1 2 3  \n"
        expected_output = "1 2 3 0\n"
        self.assertEqual(dimacs_formatter.format_cnf(input_data), expected_output)

    def test_format_cnf_09(self):
        # Test case for input with non-numeric characters
        input_data = "hallo1 -2a 3asd"
        expected_output = "1 -2 3 0\n"
        self.assertEqual(dimacs_formatter.format_cnf(input_data), expected_output)

    def test_format_cnf_10(self):
        # Test case for checking number of clauses, variables, and saw_pline flag
        self.assertEqual(dimacs_formatter.number_of_clauses, 7)
        self.assertEqual(dimacs_formatter.number_of_variables, 5)
        self.assertEqual(dimacs_formatter.saw_pline, True)


class TestDimacsFormatterWcnf(unittest.TestCase):
    def test_format_wcnf_01(self):
        # Test case for input with a comment
        input_data = "c comment"
        expected_output = "c comment"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_02(self):
        # Test with negative weights
        input_data = "-3 5 -1 0"
        expected_output = "3 5 -1 0\n"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_03(self):
        # Test case for input with weighted clauses
        input_data = "1 5 1 2 3 0"
        expected_output = "1 5 1 2 3 0\n"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_04(self):
        # Test case for empty input
        input_data = ""
        expected_output = None
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_05(self):
        # Test case multiple clauses in one line
        input_data = "1 1 2 3 0 1 4 -5 0 h -1 -2 -3 0"
        expected_output = "1 1 2 3 0\n1 4 -5 0\nh -1 -2 -3 0\n"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_06(self):
        # Test case for input with leading/trailing whitespace
        input_data = "  1 1 2 3 0   \n"
        expected_output = "1 1 2 3 0\n"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_07(self):
        # Test case for input with missing terminating zero
        input_data = "  1 1 2 3 5  \n"
        expected_output = "1 1 2 3 5 0\n"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_08(self):
        # Test case for input with non-numeric characters
        input_data = "hallo1 -2a 3asd 5"
        expected_output = "h 1 -2 3 5 0\n"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)
        
    def test_format_wcnf_09(self):
        # Test case for input with multiple comments
        input_data = "c comment1\nc comment2"
        expected_output = "c comment1\nc comment2"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_10(self):
        # Test case for input with only comments
        input_data = "c comment1\nc comment2\nc comment3"
        expected_output = "c comment1\nc comment2\nc comment3"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_11(self):
        # Test case for input with multiple clauses on separate lines
        input_data = "1 2 3 0\n4 5 6 0\n7 8 9 0"
        expected_output = "1 2 3 0\n4 5 6 0\n7 8 9 0\n"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_12(self):
        # Test case for input with large numbers
        input_data = "1000000 2000000 3000000 0"
        expected_output = "1000000 2000000 3000000 0\n"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_13(self):
        # Test case for input with duplicate clauses
        input_data = "1 2 3 0\n1 2 3 0\n1 2 3 0"
        expected_output = "1 2 3 0\n1 2 3 0\n1 2 3 0\n"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

    def test_format_wcnf_14(self):
        # Test case for empty hard clause
        input_data = "h 0"
        expected_output = "h 0\n"
        self.assertEqual(dimacs_formatter.format_wcnf(input_data), expected_output)

if __name__ == '__main__':
    unittest.main()