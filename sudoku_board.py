class SudokuBoard(object):
    def __init__(self, board):
        self.board = self.__create_board(board)

    def __create_board(self, board_file):
        board = []
        for line in board_file:
            line = line.strip()

            if len(line) != 9:
                board = []
                raise SudokuError

            board.append([])

            for c in line:
                if not c.isdigit():
                    raise SudokuError

                board[-1].append(int(c))

        if len(board) != 9:
            raise SudokuError

        return board