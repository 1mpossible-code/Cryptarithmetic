from typing import Tuple
import time


class CSP:
    @staticmethod
    def all_different(*args):
        return len(args) == len(set(args))

    def __init__(self, data: Tuple[chr]) -> None:
        self.variables = set(data)
        self.variables.add("c1")
        self.variables.add("c2")
        self.variables.add("c3")

        self.domains = {
            data[1]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # x2
            data[2]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # x3
            data[3]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # x4
            data[5]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # x6
            data[6]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # x7
            data[7]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # x8
            data[9]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # x10
            data[10]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # x11
            data[11]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # x12
            data[12]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  # x13
            data[0]: [1, 2, 3, 4, 5, 6, 7, 8, 9],  # x1
            data[4]: [1, 2, 3, 4, 5, 6, 7, 8, 9],  # x5
            data[8]: [1],  # x9
            "c1": [0, 1],  # c1
            "c2": [0, 1],  # c2
            "c3": [0, 1],  # c3
        }

        self.constraints = [
            # all letters are distinct digits
            (CSP.all_different, tuple(set(data))),
            # x4 + x8 = x13 + 10*c1
            (
                lambda x4, x8, x13, c1: x4 + x8 == x13 + 10 * c1,
                (data[3], data[7], data[12], "c1"),
            ),
            # x3 + x7 = x12 + 10*c2
            (
                lambda x3, x7, x12, c2, c1: x3 + x7 + c1 == x12 + 10 * c2,
                (data[2], data[6], data[11], "c2", "c1"),
            ),
            # x2 + x6 = x11 + 10*c3
            (
                lambda x2, x6, x11, c3, c2: x2 + x6 + c2 == x11 + 10 * c3,
                (data[1], data[5], data[10], "c3", "c2"),
            ),
            # x1 + x5 = x10 + 10*x9
            (
                lambda x1, x5, x10, x9, c3: x1 + x5 + c3 == x10 + 10 * x9,
                (data[0], data[4], data[9], data[8], "c3"),
            ),
        ]

    def get_constraints(self, var: chr):
        res = []
        for constraint, variables in self.constraints:
            if var in variables:
                res.append((constraint, variables))
        return tuple(res)


class BacktrackingSearch:
    @staticmethod
    def search(csp):
        return BacktrackingSearch.backtrack(csp, {})

    @staticmethod
    def backtrack(csp, assignment):
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
    def select_unassigned_variable(csp: CSP, assignment):
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
    def order_domain_values(csp: CSP, var, assignment):
        # Here the domains are sorted from lowest to highest, so we need just return the original domain instead of sorting it
        return csp.domains[var]

    @staticmethod
    def is_consistent(csp: "CSP", var, value, assignment):
        temp_assignment = assignment.copy()
        temp_assignment[var] = value
        for constraint, variables in csp.get_constraints(var):
            values = [temp_assignment.get(variable, None) for variable in variables]

            if all(value is not None for value in values):
                if not constraint(*values):
                    return False

        return True


class IO:
    @staticmethod
    def read(filename: str) -> Tuple[chr]:
        with open(filename, "r") as f:
            return tuple("".join([l.strip() for l in f.readlines()]))

    def write(data, assigment: dict, filename: str):
        with open(filename, "w") as f:
            res = ""
            for i in range(4):
                res += str(assigment[data[i]])
            res += "\n"
            for i in range(4, 8):
                res += str(assigment[data[i]])
            res += "\n"
            for i in range(8, 13):
                res += str(assigment[data[i]])


if __name__ == "__main__":
    data = IO.read("Input1.txt")
    assingment = BacktrackingSearch.search(CSP(data))
    IO.write(data, assingment, "Output1.txt")

    data = IO.read("Input2.txt")
    assingment = BacktrackingSearch.search(CSP(data))
    IO.write(data, assingment, "Output2.txt")
