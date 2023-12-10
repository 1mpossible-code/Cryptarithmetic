# x9 - {1}
# x1, x2 - {1,2,3,4,5,6,7,8,9}
# x2,x3,x4,x6,x7,x8,x10,x11,x12,x13 - {0,1,2,3,4,5,6,7,8,9}
# all letters are distinct digits
from typing import Tuple


class BacktrackingSearch:
    pass

class IO:
    @staticmethod
    def read(filename: str) -> Tuple[Tuple[chr], Tuple[chr]]:
        res = []
        with open(filename, 'r') as f:
            for line in f.readlines():
               res.append(tuple(line.strip()))
        
        return tuple(res)
    
    

if __name__ == '__main__':
    data = IO.read('Input1.txt')
    print(data)