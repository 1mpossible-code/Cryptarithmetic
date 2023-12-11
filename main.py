from typing import Tuple, Dict, Callable, List
import time

class CSP:
    @staticmethod
    def all_different(*args: str) -> bool:
        """Check if all arguments are different."""
        return len(args) == len(set(args))

    def __init__(self, data: Tuple[str, ...]) -> None:
        self.variables = set(data) | {"c1", "c2", "c3"}
        self.domains = {var: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] for var in data}
        self.domains[data[0]] = self.domains[data[4]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.domains[data[8]] = [1]
        self.domains.update({c: [0, 1] for c in ["c1", "c2", "c3"]})

        self.constraints: List[Tuple[Callable[..., bool], Tuple[str, ...]]] = [
            (self.all_different, tuple(set(data))),
            (lambda x4, x8, x13, c1: x4 + x8 == x13 + 10 * c1, (data[3], data[7], data[12], "c1")),
            (lambda x3, x7, x12, c2, c1: x3 + x7 + c1 == x12 + 10 * c2, (data[2], data[6], data[11], "c2", "c1")),
            (lambda x2, x6, x11, c3, c2: x2 + x6 + c2 == x11 + 10 * c3, (data[1], data[5], data[10], "c3", "c2")),
            (lambda x1, x5, x10, x9, c3: x1 + x5 + c3 == x10 + 10 * x9, (data[0], data[4], data[9], data[8], "c3")),
        ]

    def get_constraints(self, var: str) -> Tuple[Tuple[Callable[..., bool], Tuple[str, ...]], ...]:
        return tuple((constraint, variables) for constraint, variables in self.constraints if var in variables)

class BacktrackingSearch:
    @staticmethod
    def search(csp: CSP):
        return BacktrackingSearch.backtrack(csp, {})

    @staticmethod
    def backtrack(csp: CSP, assignment: Dict[str, int]):
        if len(assignment) == len(csp.variables):
            return assignment
        var = BacktrackingSearch.select_unassigned_variable(csp, assignment)
        for value in BacktrackingSearch.order_domain_values(csp, var, assignment):
            if BacktrackingSearch.is_consistent(csp, var, value, assignment):
                assignment[var] = value
                result = BacktrackingSearch.backtrack(csp, assignment)
                if result:
                    return result
                del assignment[var]
        return None

    @staticmethod
    def select_unassigned_variable(csp: CSP, assignment: Dict[str, int]) -> str:
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

        # Degree Heuristics
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
        return csp.domains[var]

    @staticmethod
    def is_consistent(csp: CSP, var: str, value: int, assignment: Dict[str, int]) -> bool:
        temp_assignment = assignment.copy()
        temp_assignment[var] = value
        for constraint, variables in csp.get_constraints(var):
            values = [temp_assignment.get(variable, None) for variable in variables]
            if all(value is not None for value in values) and not constraint(*values):
                return False
        return True

class IO:
    @staticmethod
    def read(filename: str) -> Tuple[str, ...]:
        with open(filename, "r") as f:
            return tuple("".join([line.strip() for line in f.readlines()]))

    @staticmethod
    def write(data: Tuple[str, ...], assignment: Dict[str, int], filename: str):
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
    for input_file, output_file in [("Input1.txt", "Output1.txt"), ("Input2.txt", "Output2.txt")]:
        data = IO.read(input_file)
        assignment = BacktrackingSearch.search(CSP(data))
        IO.write(data, assignment, output_file)
