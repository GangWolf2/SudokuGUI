from sudoku_board import SudokuBoard

class SudokuGame(object):

    def __init__(self, board_file):
        self.board_file = board_file
        #start_puzzle holds initial state of board file
        self.start_puzzle = SudokuBoard(board_file).board

        
    def start(self):
        self.game_over = False
        self.puzzle = []
        #nested for loop creates list of lists, first loop creates new list in parent list, second copies base board to new list
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])

    def check_win(self):
        for row in range(9):
            print(f"Row: {row}")
            if not self.check_row(row):
                return False
        for column in range(9):
            print(f"Column: {column}")
            if not self.check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.check_square(row, column):
                    return False
        self.game_over = True
        return True

    def check_block(self, block):
        return set(block) == set(range(1, 10))

    def check_row(self, row):
        return self.check_block(self.puzzle[row])

    def check_column(self, column):
        return self.check_block(
            [self.puzzle[row][column] for row in range(9)]
        )

    def __check_square(self, row, column):
        return self.check_block(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )