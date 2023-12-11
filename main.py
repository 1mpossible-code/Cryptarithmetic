# x9 - {1}
# x1, x2 - {1,2,3,4,5,6,7,8,9}
# x3,x4,x6,x7,x8,x10,x11,x12,x13 - {0,1,2,3,4,5,6,7,8,9}
# all letters are distinct digits
from typing import Tuple


class CSP:
    def __init__(self, data: Tuple[chr]) -> None:
        self.original = data


        self.variables = {}
        for i in range(len(data)):
            var = data[i]
            if var in self.variables:
                self.variables[var].append(i)
            else:
                self.variables[var] = [i]
            
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
        
        
            

class BacktrackingSearch:
    @staticmethod
    def search(csp):
        return BacktrackingSearch.backtrack(csp, {})

    @staticmethod
    def backtrack(csp, assignment):
        pass

    @staticmethod
    def all_different(*args):
        return len(args) == len(set(args))

class IO:
    @staticmethod
    def read(filename: str) -> Tuple[chr]:
        with open(filename, 'r') as f:
            return tuple(''.join([l.strip() for l in f.readlines()]))
        
    

if __name__ == '__main__':
    data = IO.read('Input1.txt')
    CSP(data)