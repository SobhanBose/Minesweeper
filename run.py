import Minesweeper

SCREENSIZE = (705, 705)
BOARDSIZE = (15,15)

if __name__ == "__main__":
    game = Minesweeper.Minesweeper(SCREENSIZE, BOARDSIZE)
    game.run()