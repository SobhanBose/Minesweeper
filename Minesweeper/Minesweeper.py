from dataclasses import dataclass, field

import pygame
import os
from .Board import Board

@dataclass
class Minesweeper:
    __screenSize: tuple
    __boardSize: tuple
    __gameState: str = "playing"

    def __post_init__(self) -> None:
        self.__board = Board(self.__boardSize)
        self.loadImages()


    def loadImages(self) -> None:
        self.__images = {}
        for fileName in os.listdir("./Minesweeper/assets"):
            if fileName.endswith(".png"):
                self.__images[fileName[:-4]] = pygame.transform.scale(pygame.image.load("./Minesweeper/assets/" + fileName), (self.__screenSize[0] // self.__board.getSize()[1], self.__screenSize[1] // self.__board.getSize()[0]))

    
    def run(self) -> None:
        pygame.init()
        self.__screen = pygame.display.set_mode((self.__screenSize[0], self.__screenSize[1]))
        pygame.display.set_caption("Minesweeper")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.__gameState == "playing":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row = pos[1] // (self.__screenSize[0] // self.__board.getSize()[1])
                        col = pos[0] // (self.__screenSize[1] // self.__board.getSize()[0])
                        if event.button == 1:
                            self.__board.handleClickEvent((row, col))
                        elif event.button == 3:
                            self.__board.handleFlagEvent((row, col))
                    self.drawBoard()
            pygame.display.flip()
        pygame.quit()


    def drawBoard(self) -> None:
        topLeft = (0, 0)
        for row in range(self.__board.getSize()[0]):
            for col in range(self.__board.getSize()[1]):
                tile = self.__board.getTile(row, col)
                imageToBlit = self.getImageTOBlit(tile)
                self.__screen.blit(imageToBlit, topLeft)
                topLeft = (topLeft[0] + imageToBlit.get_width(), topLeft[1])
            topLeft = (0, topLeft[1] + imageToBlit.get_height())
    

    def showBombs(self) -> None:
        self._bombsList = self.__board.showBombs()
        for bomb in self._bombsList:
            self.__screen.blit(self.__images["bombrevealed"], (bomb[1] * (self.__screenSize[0] // self.__board.getSize()[1]), bomb[0] * (self.__screenSize[1] // self.__board.getSize()[0])))
        pygame.display.flip()


    def getImageTOBlit(self, tile) -> pygame.Surface:
        if tile.getIsFlagged():
            return self.__images["flagged"]
        elif tile.getIsClicked():
            if tile.isDetonated():
                self.showBombs()
                self.__gameState = "lost"
                return self.__images["bombdetonated"]
            else:
                return self.__images[f"open{tile.getValue()}"]
        else:
            return self.__images["unclicked"]