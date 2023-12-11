# x9 - {1}
# x1, x2 - {1,2,3,4,5,6,7,8,9}
# x3,x4,x6,x7,x8,x10,x11,x12,x13 - {0,1,2,3,4,5,6,7,8,9}
# all letters are distinct digits
from typing import Tuple


class CSP:
    def __init__(self, data: Tuple[chr]) -> None:
        self.variables = data

        self.domains = [
            [1,2,3,4,5,6,7,8,9],   # x1
            [0,1,2,3,4,5,6,7,8,9], # x2
            [0,1,2,3,4,5,6,7,8,9], # x3
            [0,1,2,3,4,5,6,7,8,9], # x4
            [1,2,3,4,5,6,7,8,9],   # x5
            [0,1,2,3,4,5,6,7,8,9], # x6
            [0,1,2,3,4,5,6,7,8,9], # x7
            [0,1,2,3,4,5,6,7,8,9], # x8
            [1],                   # x9
            [0,1,2,3,4,5,6,7,8,9], # x10
            [0,1,2,3,4,5,6,7,8,9], # x11
            [0,1,2,3,4,5,6,7,8,9], # x12
            [0,1,2,3,4,5,6,7,8,9], # x13
            [0, 1],                # c1
            [0, 1],                # c2
            [0, 1],                # c3
            [0, 1],                # c4
        ]

        def all_different(*args):
            return len(args) == len(set(args))

        self.constraints = [
            # x4 + x8 = x13 + 10*c1
            (lambda x4, x8, x13, c1: x4 + x8 == x13 + 10*c1, (data[3], data[7], data[12], 'c1')),
            # x3 + x7 = x12 + 10*c2
            (lambda x3, x7, x12, c2: x3 + x7 == x12 + 10*c2, (data[2], data[6], data[11], 'c2')),
            # x2 + x6 = x11 + 10*c3
            (lambda x2, x6, x11, c3: x2 + x6 == x11 + 10*c3, (data[1], data[5], data[10], 'c3')),
            # x1 + x5 = x10 + 10*c4
            (lambda x1, x5, x10, c4: x1 + x5 == x10 + 10*c4, (data[0], data[4], data[9], 'c4')),
            # c4 = x9
            (lambda c4, x9: c4 == x9, ('c4', data[8])),
            # x9 == 1 and x1, x5 != 0
            (lambda x9, x1, x5: x9 == 1 and x1 != 0 and x5 != 0, (data[8], data[0], data[4])),
            # all letters are distinct digits
            (lambda x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12: all_different(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12), (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11])),
        ]
        
            

class BacktrackingSearch:
    @staticmethod
    def search(csp):
        return BacktrackingSearch.backtrack(csp, {})

    @staticmethod
    def backtrack(csp, assignment):
        pass

class IO:
    @staticmethod
    def read(filename: str) -> Tuple[chr]:
        with open(filename, 'r') as f:
            return tuple(''.join([l.strip() for l in f.readlines()]))
        
    

if __name__ == '__main__':
    data = IO.read('Input1.txt')
    CSP(data)