"""
Starter code for a Sudoku solver, adapted from UMass CS 220.

To run from the command line: python3 starter.py

This will run the unit tests at the end of the file.
"""
import unittest

class Board:
    """Board(board_dict) is a class that represents a Sudoku board, where:

    - board_dict is a dictionary from (row, col) to a list of available values.
      The rows and columns are integers in the range 0 .. 8 inclusive. Each
      available value is an integer in the range 1 .. 9 inclusive."""


    def __init__(self, board_dict):
        """board_dict should be a dictionary, as described in the definition of
        the Board class."""

        self.board_dict = board_dict


    def __str__(self):
        """Prints the board nicely, arranging board_dict like a Sudoku board."""
        rows = [ ]
        for row in range(0, 9):
            col_strs = [ ]
            for col in range(0, 9): 
                val_str = ''.join(str(x) for x in self.board_dict[(row, col)])
                # Pad with spaces for alignment.
                val_str = val_str + (' ' * (9 - len(val_str)))
                col_strs.append(val_str)
                # Horizontal bar to separate boxes
                if col == 2 or col == 5:
                    col_strs.append('|')
            rows.append(' '.join(col_strs))
            # Vertical bar to separate boxes
            if row == 2 or row == 5:
                rows.append(93 * '-')
        return '\n'.join(rows)


    def copy(self):
        """Creates a deep copy of this board. Use this method to create a copy
        of the board before modifying the available values in any cell."""
        new_dict = { }
        for (k, v) in self.board_dict.items():
            new_dict[k] = v.copy()
        return Board(new_dict)


    def value_at(self, row, col):
        """Returns the value at the cell with the given row and column (zero
        indexed). Produces None if the cell has more than one available
        value."""
        value = self.board_dict[(row,col)]
        if len(value) == 1:
            return value[0]
        else:
            return None 


    def place(self, row, col, value):
        """Places value at the given row and column.
        
        Eliminates value from the peers of (row, col) and recursively calls
        place on any cell that is constrained to exactly one value."""

        value = str(value)
        self.board_dict[(row, col)] = [value] 
        peersLst = peers(row, col)
        for i in peersLst:
            #print(i[0])
            peerValue = self.board_dict[i]
            if value in peerValue:
                peerValue.remove(value)
                if len(peerValue) == 1:
                    self.place(i[0], i[1], peerValue[0])
            

    def next_boards(board):
        """Returns a list of boards that have one cell filled.

        Selects a cell that is maximally constrained: i.e., has a minimum
        number of available values.
        """
        # find a cell with a minimal number of available values

        boardList = []

        minVal = 10 
        minCell = (0,0)
        # iterate through each cell to find the cell with least number of available values
        for cell in board.board_dict:
            if len(board.board_dict[cell]) < minVal and len(board.board_dict[cell]) > 1: 
                minCell = cell
                minVal = len(board.board_dict[cell]) #update minVal 

        # loop over each available value in minCell
        for i in board.board_dict[minCell]:
            newBoard = board.copy()
            newBoard.place(minCell[0], minCell[1], i)
            boardList.append(newBoard)

        return boardList


    def is_solved(self):
        """Returns True if the board is fully solved, and there are no choices
        to make at any cell."""
        for i in self.board_dict:
            if len(self.board_dict[i]) != 1:
                return False
        return True 
    

    def is_unsolvable(self):
        """Returns True if the board is unsolvable."""
        # a board is unsolvable if any cell is constrained to the empty set of values
        for i in self.board_dict:
            if self.board_dict[i] == []:
                return True
        return False


def parse(sudoku_string):
    """Parses a string of 81 digits and periods for empty cells into, produce
    a Board that represents the Sudoku board."""
    # create a full 9x9 board where each cell is filled with 
    # ["1","2","3","4","5","6","7","8","9"]

    boardDict = {}
            
    # fill each cell with all possible values
    for i in range(9):
        for j in range(9):
            boardDict[(i,j)] = [1,2,3,4,5,6,7,8,9]

    i = 0 
    for row in range(9):
        for col in range(9):
            value = sudoku_string[i]
            i = i+1
            if value != ".":
                value = int(value)
                boardDict[(row,col)] = [value]
                peersLst = peers(row, col)
                #print(peersLst)
                #assert len(peersLst)==20
            
                for peer in peersLst:
                    if value in boardDict[peer]:   
                        boardDict[peer].remove(value)

                        

    return Board(boardDict)


def peers(row, col):
    """Returns the peers of the given row and column, as a list of tuples."""
    # coordinate of the top left cell in a box is:
        
    topLeft = (row - row % 3, col - col % 3)
    tupList = []
                
    for i in range(9):
        for j in range(9):
            if (i == row and j != col) or (i != row and j == col):
                tupList.append((i,j))
            elif (i >= topLeft[0] and i < topLeft[0] + 3) and (j >= topLeft[1] and j < topLeft[1] + 3):
                if (i,j) != (row, col):
                    tupList.append((i,j))
   
    return tupList 


def solve(board):
    """Recursively solve the board."""
    if board.is_solved():
        return board
    if board.is_unsolvable():
        return None 

    boardLst = board.next_boards()
    # iterate through the list of next boards and recursively solve(board)
    for board in boardLst:
        result = solve(board)
        if result:
            return result 


class SudokuTests(unittest.TestCase):

    def test_easy1(self):
        s = "85....4.1......67...21....3..85....7...982...3....15..5....43...37......2.9....58"
        board = parse(s)
        #print(board)
        #board.place(0,0,2)
        #print(board.value_at(0,0))
        solution = solve(board)
        assert(solution is not None)

    def test_medium1(self):
        s = ".1.....2..3..9..1656..7...33.7..8..........89....6......6.254..9.5..1..7..3.....2"
        board = parse(s)
        solution = solve(board)
        assert(solution is not None)

    def test_medium2(self):
        s = "2...8.3...6..7..84.3.5..2.9...1.54.8.........4.27.6...3.1..7.4.72..4..6...4.1...3"
        board = parse(s)
        solution = solve(board)
        assert(solution is not None)


if __name__ == "__main__":
    unittest.main()    