from Board import board
import math
import sys
import pygame


class game(board):
    colors = {"background": (0, 135, 169), "empty": (
        3, 40, 60), "red": (218, 8, 9), "yellow": (222, 196, 0)}

    def __init__(self, square_size, row_count, column_count):
        super().__init__(row_count, column_count)
        self.SQUARESIZE = square_size
        self.width = column_count * self.SQUARESIZE
        self.height = (row_count+1) * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.RADIUS = int(self.SQUARESIZE/2 - 5)
        self.firstTime = True
        pygame.init()
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound(
            './music/relax_background1.ogg')
        self.drop = pygame.mixer.Sound('./music/coin_drop.ogg')
        self.applause = pygame.mixer.Sound('./music/applause.ogg')

    def draw_board(self):
        if(self.firstTime):
            pygame.draw.rect(
                self.screen, game.colors["background"], (0, 0, self.width, self.SQUARESIZE))
            self.firstTime = False
        for c in range(super().column_count()):
            for r in range(super().row_count()):
                pygame.draw.rect(self.screen, game.colors["background"], (
                    c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, game.colors["empty"], (int(
                    c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        board = super().board()
        for c in range(super().column_count()):
            for r in range(super().row_count()):

                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, game.colors["red"], (int(
                        c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(self.screen, game.colors["yellow"], (int(
                        c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        pygame.display.update()

    def start_game(self):
        pygame.mixer.Sound.play(self.background_music)
        self.draw_board()
        pygame.display.update()
        myfont = pygame.font.SysFont("monospace", self.SQUARESIZE-25)
        while not super().game_over():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(
                        self.screen, game.colors["background"], (0, 0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    if super().turn() == 0:
                        pygame.draw.circle(
                            self.screen, game.colors["red"], (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                    else:
                        pygame.draw.circle(
                            self.screen, game.colors["yellow"], (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.Sound.play(self.drop)
                    pygame.draw.rect(
                        self.screen, game.colors["background"], (0, 0, self.width, self.SQUARESIZE))
                    # print(event.pos)
                    # Ask for Player 1 Input
                    if super().turn() == 0:
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.SQUARESIZE))

                        if super().is_valid_location(col):
                            row = super().get_next_open_row(col)
                            super().drop_piece(row, col, 1)

                            if super().winning_move(1):
                                label = myfont.render(
                                    "*Player 1 wins*", 1, game.colors["red"])
                                self.screen.blit(
                                    label, (0, 10))
                                super().set_game_over()

                    # # Ask for Player 2 Input
                    else:
                        posx = event.pos[0]
                        col = int(math.floor(posx/self.SQUARESIZE))

                        if super().is_valid_location(col):
                            row = super().get_next_open_row(col)
                            super().drop_piece(row, col, 2)

                            if super().winning_move(2):
                                label = myfont.render(
                                    "*Player 2 wins*", 1, game.colors["yellow"])
                                self.screen.blit(
                                    label, (0, 10))
                                super().set_game_over()

                    if(super().number_of_pieces() <= 0):
                        label = myfont.render(
                            "*TIE*", True, game.colors["yellow"])
                        self.screen.blit(label, (0, 10))
                        super().set_game_over()

                    super().print_board()
                    self.draw_board()

                    super().set_turn((super().turn() + 1) % 2)

                    if super().game_over():
                        pygame.mixer.Sound.play(self.applause)
                        pygame.time.wait(7000)


g = game(50, 6, 7)
g.start_game()
