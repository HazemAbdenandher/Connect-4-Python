import numpy as np


class board:
    def __init__(self, row_count, column_count):
        self.ROW_COUNT = row_count
        self.COLUMN_COUNT = column_count
        self.GAME_OVER = False
        self.TURN = 0
        self.PIECES = self.ROW_COUNT * self.COLUMN_COUNT
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

    def column_count(self):
        return self.COLUMN_COUNT

    def row_count(self):
        return self.ROW_COUNT

    def board(self):
        return self.board

    def game_over(self):
        return self.GAME_OVER

    def set_game_over(self):
        self.GAME_OVER = True

    def turn(self):
        return self.TURN

    def set_turn(self, turn):
        self.TURN = turn

    def number_of_pieces(self):
        return self.PIECES

    def drop_piece(self, row, col, piece):
        self.PIECES -= 1
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT-1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(self.ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT-3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True

    def start_game(self):
        while not self.GAME_OVER:
            # Ask for Player 1 Input
            if self.TURN == 0:
                col = int(input("player 1 turn , select (0,6) : "))
                if self.is_valid_location(col):
                    row = self.get_next_open_row(col)
                    self.drop_piece(row, col, 1)

                    if self.winning_move(1):
                        self.GAME_OVER = True

            # # Ask for Player 2 Input
            else:
                col = int(input("player 2 turn , select (0,6) : "))
                if self.is_valid_location(col):
                    row = self.get_next_open_row(col)
                    self.drop_piece(row, col, 2)

                    if self.winning_move(2):
                        self.GAME_OVER = True

            self.print_board()
            self.TURN = (self.TURN+1) % 2
