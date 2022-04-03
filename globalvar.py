import argparse
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM

BOARDS = ['debug', 'easy', 'error', 'hard']
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
#board is 490X490
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

class SudokuError(Exception):
    """
    An application specific error.
    """
    pass

