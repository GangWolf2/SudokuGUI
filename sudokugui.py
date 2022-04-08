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

        self.usedNums = {
            (0, 0): [],
            (0, 3): [],
            (0, 6): [],
            (3, 0): [],
            (3, 3): [],
            (3, 6): [],
            (6, 0): [],
            (6, 3): [],
            (6, 6): []
        }

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
        self.__initDict()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __initDict(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if self.game.puzzle[i][j] != 0:
                    # finds the closest top left corner of the current box
                    # top left corner of every box is consistent point every other cell in box can reach
                    k = i - (i % 3)
                    l = j - (j % 3)

                    # since each value of key is array, we can use built-in array methods to update dict value
                    self.usedNums[(k, l)].append(self.game.puzzle[i][j])
        print(f'self.usedNums[(0,0)] {self.usedNums[(0,0)]} \n'
              f'self.usedNums[(0,3)] {self.usedNums[(0,3)]} \n'
              f'self.usedNums[(0,6)] {self.usedNums[(0,6)]} \n'
              )
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
            if self.__checkRowCol(self.game.puzzle, self.row, self.col, i):
                        self.game.puzzle[self.row][self.col] = i
                        if self.__solve():
                            print("Recursive solve call")
                            return True
                        self.game.puzzle[self.row][self.col] = 0
                        r = self.row - (self.row % 3)
                        c = self.col - (self.col % 3)
                        print(f'r value: {r}, c value: {c}')
                        print(f'self.usedNums[(r,c)] {self.usedNums[(0, 6)]} \n')
                        self.usedNums[(r, c)].remove(i)
        print("Board is unsolvable")
        return False

    def __findEmpty(self, board):
        for i in range(0, 9):
            for j in range(0, 9):
                if board[i][j] == 0:
                    print(f"__findEmpty: Empty space found at {str(i)}, {str(j)}")
                    return (i, j)  # returns the row, column values where empty space found
        # if there are no empty spaces, return None
        return None

    def __checkRowCol(self, board, row, col, numChosen):
        # checks row if numChosen equal to any row values
        print(f'checkRowCol Row, Col: {row}, {col}')
        print(f'checkRowCol numChosen: {numChosen}')
        for i in range(0, 9):
            if board[row][i] == numChosen:
                #print(f' __checkRowCol Row,i value: {row,i}')
                #print("ILLEGAL: Same number in row")
                return False
        # checks column of current cell to see if numChosen = any current values in the column
        for j in range(0, 9):
            if board[j][col] == numChosen:
                #print("ILLEGAL: Same number in column")
                return False

        # checks box to make sure number has not already been chosen
        # finds the closest top left corner to the current box so it can check against keys in dictionary above
        row = row - (row % 3)
        col = col - (col % 3)
        #print('row, col altered')
        # checks if chosen number is in list of values mapped to current box and returns False if found
        if numChosen in self.usedNums[(row, col)]:
            print("ILLEGAL: Same number in box")
            return False
        # if the chosen number is not found in the list of values, then it is appended to the value list and returns True
        self.usedNums[(row, col)].append(numChosen)
        print(f'self.usedNums[(row, col)]: {self.usedNums[(row, col)]}')
        print("Returning true")
        return True

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
