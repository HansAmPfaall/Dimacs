"""
This script is used to format CNF and WCNF files to the standard DIMACS format that is used in
the SAT Competition.
The script takes in a file or a folder as input and formats all the CNF and WCNF files in the
folder to the DIMACS format.
It was mainly created to be used in the Dimacs Formatter Visual Studio Code extension.
"""

import sys
import time
import os

def main():
    """
    Main function, entry point of the script.
    Tests are in the "dimacs_formatter_test.py" file.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 dimacs_formatter.py <input_file>")
        print("or: python3 dimacs_formatter.py <folder>")
        return

    input_file = sys.argv[1]

    if input_file.endswith('.cnf'):
        format_cnf_file(input_file)
        return

    if input_file.endswith('.wcnf'):
        format_wcnf_file(input_file)
        return

    # If the input is a folder, format all the CNF and WCNF files in the folder, should only
    #  be used with caution because the formatting is inplace.
    if os.path.isdir(input_file):
        for root, dirs, files in os.walk(input_file):
            for file in files:
                if file.endswith('.cnf'):
                    format_cnf_file(os.path.join(root, file))

                if file.endswith('.wcnf'):
                    format_wcnf_file(os.path.join(root, file))

number_of_clauses = 0
number_of_variables = 0
saw_pline = False
def format_cnf_file(input_file):
    """
    Formats a CNF file to DIMACS CNF (Conjunctive Normal Form) output.
    """
    formatted_lines = []
    global number_of_clauses
    number_of_clauses = 0
    global number_of_variables
    number_of_variables = 0
    global saw_pline
    saw_pline = False
    # Read the file.
    with open(input_file, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            formatted_line = format_cnf(line)
            if formatted_line is not None:
                formatted_lines.append(formatted_line)
        # If the file does not have a p line, add it. If it has a p line, update the number of
        #  variables and clauses.
        for i, line in enumerate(formatted_lines):
            if line.startswith('p cnf'):
                formatted_lines[i] = 'p cnf ' + str(number_of_variables) + ' ' + \
                str(number_of_clauses) + '\n'
                break
            if saw_pline is False and line.startswith('c') is False:
                formatted_lines.insert(i, 'p cnf ' + str(number_of_variables) + ' ' + \
                str(number_of_clauses) + '\n')
                saw_pline = True
                break
        # Write the formatted lines back to the file.
        f.seek(0)
        f.writelines(formatted_lines)
        f.truncate()


def format_cnf(line):
    """
    Formats a line to DIMACS CNF (Conjunctive Normal Form) output.

    Args:
        line (str): The line of CNF input to be formatted.

    Returns:
        str: The formatted line of CNF input.
        None: If the line is empty.

    Raises:
        None

    Examples:
        >>> format_cnf('1 2 -3 0\n')
        '1 2 -3 0\n'
    
    Tests can be found in the "dimacs_formatter_test.py" file.
    """
    global number_of_clauses
    global number_of_variables
    global saw_pline
    # If the line is a comment, return it as is.
    if line.startswith('c'):
        return line
    # If the line is the p line, set the flag to remember that one was seen already.
    if line.startswith('p cnf'):
        if saw_pline:
            return
        saw_pline = True
        return line
    # If the line starts with zero it is probalby an empty clause,so return an empty clause.
    if line.startswith('0') or line == '0\n':
        number_of_clauses += 1
        return '0\n'
    # Trim the line and add a newline character at the end.
    line = line.rstrip(' \n') + '\n'
    line = line.lstrip()
    # If the line is empty, return None.
    if line == '\n':
        return
    # If the line has more than 1 clause, split it and format each clause separately.
    if len(line.split(' 0')) > 2:
        line = line.split(' 0')
        new_line = ""
        for l in line:
            formatted_line = format_cnf(l)
            # Only add the formatted line if it is not None.
            if formatted_line is not None:
                new_line += formatted_line
        return new_line
    minus = False
    literals = []
    for literal in line.split():
        # Remove all non-numeric characters from the literal.
        # This way even gibbereish can be formatted to the DIMACS format.
        literal = ''.join(filter(lambda x: x.isdigit() or x == '-', literal))
        if not literal or literal == '0' or literal == '-0':
            continue
        # If a single arbitrary minus character is found, set the minus flag to True.
        if literal == '-':
            minus = True
            continue
        if minus:
            # add the minus sign to the literal if it is positive.
            # If the next literal is already negative, set the minus flag to False.
            if int(literal) > 0:
                literal = '-' + literal
            minus = False
        literals.append(literal)
        # search for the largest variable to make sure the p line is correct.
        if abs(int(literal)) > number_of_variables:
            number_of_variables = abs(int(literal))
    if literals:
        number_of_clauses += 1
        return ' '.join(literals) + ' 0\n'

def format_wcnf_file(input_file):
    """
    Formats a WCNF file to DIMACS WCNF (Weighted Conjunctive Normal Form) output.
    """
    formatted_lines = []
    # Read the file.
    with open(input_file, 'r+', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            formatted_line = format_wcnf(line)
            if formatted_line is not None:
                formatted_lines.append(formatted_line)
        # Write the formatted lines back to the file.
        f.seek(0)
        f.writelines(formatted_lines)
        f.truncate()

def format_wcnf(line):
    """
    Formats a line to DIMACS WCNF (Weighted Conjunctive Normal Form) output.

    Args:
        line (str): The line of WCNF input to be formatted.

    Returns:
        str: The formatted line of WCNF input.
        None: If the line is empty.

    Raises:
        None

    Examples:
        >>> format_wcnf('1 2 -3 0\n')
        '1 2 -3 0\n'
    
    Tests can be found in the "dimacs_formatter_test.py" file.
    """
    # If the line is a comment, return it as is.
    if line.startswith('c'):
        return line
    # Trim the line and add a newline character at the end.
    line = line.rstrip(' \n') + '\n'
    line = line.lstrip()
    # If the line is empty, return None.
    if line == '\n':
        return
    # If the line has more than 1 clause, split it and format each clause separately.
    if len(line.split(' 0')) > 2:
        line = line.split(' 0')
        new_line = ""
        for l in line:
            formatted_line = format_wcnf(l)
            # Only add the formatted line if it is not None.
            if formatted_line is not None:
                new_line += formatted_line
        return new_line
    literals = []
    # If the line starts with h it is a hard clause, so add an h to the literals list.
    if line.startswith('h'):
        literals.append('h')
    # Negative weights are not allowed, so remove the minus sign from the weight.
    if line.startswith('-'):
        line = line[1:]
    minus = False
    for literal in line.split():
        literal = ''.join(filter(lambda x: x.isdigit() or x == '-', literal))
        if not literal or literal == '0' or literal == '-0':
            continue
        # If a single arbitrary minus character is found, set the minus flag to True.
        if literal == '-':
            minus = True
            continue
        if minus:
            # add the minus sign to the literal if it is positive.
            # If the next literal is already negative, set the minus flag to False.
            if int(literal) > 0:
                literal = '-' + literal
            minus = False
        literals.append(literal)
    if literals:
        return ' '.join(literals) + ' 0\n'


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f"Time taken: {time.time() - start_time} seconds")
