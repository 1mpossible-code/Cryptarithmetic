# Cryptarithmetic Problem

**The project is part of the course work for the course "Artificial Intelligence" CS4613.**

Cryptarithmetic is a type of mathematical puzzle in which the digits are replaced by letters of the alphabet or other symbols. The goal is to find the numerical value of each letter. Each letter can be assigned a different digit from 0 to 9, but no two letters can be assigned to the same digit. The puzzle is solved when the letters are assigned to digits in such a way that the resulting mathematical equation is correct.

The full description of the problem can be found [here](./Crypta.pdf).

### Prerequisites

- Python must be installed on your system. The program is tested with Python 3.12.x.
- No additional libraries are required outside of the Python Standard Library.

### Program Files

- `main.py` - The main program file.
- `Input1.txt`, `Input2.txt` - The input files containing the cryptarithmetic problems.
- `Output1.txt`, `Output2.txt` - The output files containing the solutions to the cryptarithmetic problems.

### Running the Program

1. Place the `main.py` script and the input files in the same directory.
2. Open a terminal or command line interface.
3. Change the directory to where the script and input files are located with `cd path/to/directory`.
4. Execute the script by running the command: `python3 main.py`.

## Running custom files

1. To run your own puzzles, put them in the file and name it as you like.
2. Demonstration of the script is presented in the end of the source code in the block:

```python
if __name__ == "__main__":
    for input_file, output_file in [
        ("Input1.txt", "Output1.txt"),
        ("Input2.txt", "Output2.txt"),
    ]:
        data = IO.read(input_file)
        assignment = BacktrackingSearch.search(CSP(data))
        IO.write(data, assignment, output_file)
```

### Expected Output

- The program will read the data from the input files.
- It will process the data and solve the cryptarithmetic puzzles.
- The solutions will be written to the output files.
- The output files will be created in the same directory as the script.

### Solution Files

- `Output1.txt`
- `Output2.txt`

### Source Code

Please refer to the `main.py` file for the full source code. The code is commented for clarity and understanding of the logic used.

---

## Input
```
SEND
MORE
MONEY
```

## Output
```
9567
1085
10652
```

---

## Input
```
BASE
BALL
GAMES
```

## Output
```
7483
7455
14938
```