"""
This program solves Cryptarithmetic puzzles using Backtracking Search.
The program takes the input from the file and writes the output to the file as specified in the assignment.
The program uses Minimum Remaining Values Heuristics and Degree Heuristics to select the unassigned variable.
The program does not use Inference.
"""
from typing import Tuple, Dict, Callable, List


class CSP:
    """
    A class to represent a Constraint Satisfaction Problem.
    """

    def __init__(self, data: Tuple[str, ...]) -> None:
        # data is a tuple of 13 variables
        # The first 4 variables are the first row of the puzzle
        # The next 4 variables are the second row of the puzzle
        # The next 5 variables are the third row of the puzzle
        # The last 3 variables are the carry variables
        self.variables = set(data) | {"c1", "c2", "c3"}

        # domains is a dictionary of variables and their domains
        self.domains = {var: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] for var in data}
        self.domains[data[0]] = self.domains[data[4]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.domains[data[8]] = [1]
        self.domains.update({c: [0, 1] for c in ["c1", "c2", "c3"]})

        # constraints is a list of tuples of constraint functions and their variables
        self.constraints: List[Tuple[Callable[..., bool], Tuple[str, ...]]] = [
            (self.all_different, tuple(set(data))),
            (
                lambda x4, x8, x13, c1: x4 + x8 == x13 + 10 * c1,
                (data[3], data[7], data[12], "c1"),
            ),
            (
                lambda x3, x7, x12, c2, c1: x3 + x7 + c1 == x12 + 10 * c2,
                (data[2], data[6], data[11], "c2", "c1"),
            ),
            (
                lambda x2, x6, x11, c3, c2: x2 + x6 + c2 == x11 + 10 * c3,
                (data[1], data[5], data[10], "c3", "c2"),
            ),
            (
                lambda x1, x5, x10, x9, c3: x1 + x5 + c3 == x10 + 10 * x9,
                (data[0], data[4], data[9], data[8], "c3"),
            ),
        ]

    def get_constraints(
        self, var: str
    ) -> Tuple[Tuple[Callable[..., bool], Tuple[str, ...]], ...]:
        """
        Returns a tuple of tuples of constraint functions and their variables
        that involve the given variable.
        """
        return tuple(
            (constraint, variables)
            for constraint, variables in self.constraints
            if var in variables
        )

    @staticmethod
    def all_different(*args: str) -> bool:
        """
        Returns True if all the arguments are different, False otherwise.
        This is a constraint function.
        """
        return len(args) == len(set(args))


class BacktrackingSearch:
    """
    A class to represent a Backtracking Search algorithm.
    """

    @staticmethod
    def search(csp: CSP):
        """
        Returns an assignment that satisfies all the constraints of the CSP or None if no such assignment exists.
        """
        return BacktrackingSearch.backtrack(csp, {})

    @staticmethod
    def backtrack(csp: CSP, assignment: Dict[str, int]):
        # If assignment is complete, return assignment
        if len(assignment) == len(csp.variables):
            return assignment
        # Select an unassigned variable
        var = BacktrackingSearch.select_unassigned_variable(csp, assignment)
        # Try all values in the domain of the variable
        for value in BacktrackingSearch.order_domain_values(csp, var, assignment):
            # If value is consistent with assignment, add {var: value} to assignment
            if BacktrackingSearch.is_consistent(csp, var, value, assignment):
                assignment[var] = value
                # Backtrack the new assignment
                result = BacktrackingSearch.backtrack(csp, assignment)
                # If result is not failure, return result
                if result:
                    return result
                # Otherwise, remove {var: value} from assignment and try another value
                del assignment[var]
        # If no value is consistent with assignment, return failure
        return None

    @staticmethod
    def select_unassigned_variable(csp: CSP, assignment: Dict[str, int]) -> str:
        """
        Selects an unassigned variable using Minimum Remaining Values Heuristics and Degree Heuristics.
        """
        # Minimum Remaining Values Heuristics
        # If variable is not assigned
        # If variable has the minimum domain length
        # Add variable to the list of variables with minimum domain length and update minimum domain length
        # If there is only one variable with minimum domain length, return it
        mini = [[], float("inf")]
        for variable in csp.variables:
            if variable not in assignment:
                domain_length = len(csp.domains[variable])
                if domain_length < mini[1]:
                    mini[0], mini[1] = [variable], domain_length
                elif domain_length == mini[1]:
                    mini[0].append(variable)
        if len(mini[0]) == 1:
            return mini[0][0]

        # If there are multiple variables with minimum domain length, use Degree Heuristics

        # Degree Heuristics
        # For each variable with minimum domain length
        # Find the variable with the maximum number of constraints
        # Add variable to the list of variables with maximum number of constraints and update maximum number of constraints
        # If there is only one variable with maximum number of constraints, return it
        # If there are multiple variables with maximum number of constraints, return the first one
        vars = mini[0]
        maxi = [[], float("-inf")]
        for i in range(len(vars)):
            var = vars[i]
            l = len(csp.get_constraints(var))
            if l > maxi[1]:
                maxi[0], maxi[1] = var, l

        return maxi[0]

    @staticmethod
    def order_domain_values(csp: CSP, var: str, assignment: Dict[str, int]):
        """
        Since the domain of each variable is already ordered, this function returns the domain of the variable.
        """
        return csp.domains[var]

    @staticmethod
    def is_consistent(
        csp: CSP, var: str, value: int, assignment: Dict[str, int]
    ) -> bool:
        """
        Returns True if the value is consistent with the assignment, False otherwise.
        """
        # Add {var: value} to assignment
        # For each constraint function and its variables that involve the given variable
        # If all the variables have been assigned and the constraint function returns False, return False
        # Otherwise, return True
        temp_assignment = assignment.copy()
        temp_assignment[var] = value
        for constraint, variables in csp.get_constraints(var):
            values = [temp_assignment.get(variable, None) for variable in variables]
            if all(value is not None for value in values) and not constraint(*values):
                return False
        return True


class IO:
    """
    Service class to read and write data.
    """

    @staticmethod
    def read(filename: str) -> Tuple[str, ...]:
        """
        Reads the data from the file.
        """
        with open(filename, "r") as f:
            return tuple("".join([line.strip() for line in f.readlines()]))

    @staticmethod
    def write(data: Tuple[str, ...], assignment: Dict[str, int], filename: str):
        """
        Writes the assignment to the file.
        """
        with open(filename, "w") as f:
            for i in range(4):
                f.write(str(assignment[data[i]]))
            f.write("\n")
            for i in range(4, 8):
                f.write(str(assignment[data[i]]))
            f.write("\n")
            for i in range(8, 13):
                f.write(str(assignment[data[i]]))


if __name__ == "__main__":
    for input_file, output_file in [
        ("Input1.txt", "Output1.txt"),
        ("Input2.txt", "Output2.txt"),
    ]:
        data = IO.read(input_file)
        assignment = BacktrackingSearch.search(CSP(data))
        IO.write(data, assignment, output_file)
