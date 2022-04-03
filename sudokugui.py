from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
from globalvar import *
from sudoku_game import SudokuGame

class SudokuGUI(Frame):
    #parent = '', game = SudokuGame object
    def __init__(self, parent, game):
        self.parent = parent
        #__init__ of SudokuGame creates
        self.game = game
        Frame.__init__(self, parent)

        self.row, self.col = 0,0
        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH, expand = 1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)

        self.canvas.pack(fill=BOTH, side=TOP)

        clear_button = Button(self, text="Clear Answers", command=self.__clear_answers)

        clear_button.pack(fill=BOTH, side=BOTTOM)

        solve_button = Button(self, text="Solve", command=self.__solve)

        solve_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        for i in range(10):
            color = "blue" if i%3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "green"
                    self.canvas.create_text(x, y, text=answer, tags="numbers", fill=color)

    def __clear_answers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.__draw_puzzle()

    def __cell_clicked(self,event):
        if self.game.game_over:
            return

        x, y = event.x, event.y
        #20 < x < 470 and 20 < y < 470
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()
            #row = (25-20)/50 col = (121 - 20) / 50 = .1,2 = (0,2)
            row, col = int((y - MARGIN) / SIDE), int((x - MARGIN) / SIDE)

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            #added comparison to orignal puzzle
            elif self.game.start_puzzle[row][col] == 0 or self.game.puzzle[row][col] == 0:
                self.row, self.col = row, col

        self.__draw_cursor()

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(x0, y0, x1, y1,outline="red", tags="cursor")

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()


    def __solve(self):
        curSquare = self.__findEmpty(self.game.puzzle)
        if not curSquare:
            print("The board has been solved")
            self.__draw_puzzle()
            return True

        else:
            self.row, self.col = curSquare
            print(f'Row: {self.row}')
            print(f'Col: {self.col}')

        for i in range(1,10):
            if self.game.check_row(self.row):
                if self.game.check_col(self.col):
                    if self.game.check_square(self.row, self.col):
                        self.game.puzzle[self.row][self.col] == i
                        self.__draw_puzzle()
                        if self.__solve():
                            print("Recursive solve call")
                            return True
        print("Board is unsolvable")
        return False

    def __findEmpty(self, board):
        for i in range(0, 9):
            for j in range(0, 9):
                if board[i][j] == 0:
                    print(f"Empty space found at {str(i)}, {str(j)}")
                    return (i, j)  # returns the row, column values where empty space found
        # if there are no empty spaces, return None
        return None
    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1, tags="victory", fill="dark orange", outline="orange")
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y, text="You win!", tags="winner", fill="white", font=("Arial", 32))
