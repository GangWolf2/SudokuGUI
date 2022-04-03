from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
from sudokugui import SudokuGUI
from globalvar import *
from sudoku_game import SudokuGame

def parse_arguments():
    """
    Parses arguments of the form:
        sudoku.py <board name>
    Where `board name` must be in the `BOARD` list
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--board",
                            help="Desired board name",
                            type=str,
                            choices=BOARDS,
                            required=True)
    args = vars(arg_parser.parse_args())
    return args['board']


if __name__ == '__main__':
    board_name = parse_arguments()

    with open('%s.sudoku' % board_name, 'r') as boards_file:
        game = SudokuGame(boards_file)
        game.start()

        root = Tk()
        #game being passed to SudokuGUI has .puzzle list of lists already created, no need to create in GUI
        SudokuGUI(root, game)
        root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
        root.mainloop()

