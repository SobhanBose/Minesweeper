from dataclasses import dataclass, field
from typing import ClassVar

from .Tile import Tile
from random import random

@dataclass
class Board:
    prob: ClassVar[float] = 0.2
    __size: tuple
    __bombsList: list = field(default_factory=list)


    def __post_init__(self) -> None:
        self.setBoard()


    def handleFlagEvent(self, pos: tuple) -> None:
        self.getTile(pos[0], pos[1]).handleFlagEvent()
    

    def handleClickEvent(self, pos: tuple) -> None:
        self.getTile(pos[0], pos[1]).handleClickEvent()


    def setBoard(self) -> None:
        self.__board = []
        for col in range(self.__size[0]):
            self.__board.append([])
            for row in range(self.__size[1]):
                hasBomb = random()<Board.prob
                if hasBomb:
                    self.__bombsList.append((row, col))
                self.__board[col].append(Tile(hasBomb))
        self.setNeighbours()
    

    def setNeighbours(self) -> None:
        for col in range(self.__size[0]):
            for row in range(self.__size[1]):
                tile = self.getTile(row, col)
                neighboursData = self.getNeighboursData(row, col)
                tile.setNeighbours(neighboursData)
    

    def getNeighboursData(self, row: int, col: int) -> list:
        neighboursData = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if row + i < 0 or row + i >= self.__size[0] or col + j < 0 or col + j >= self.__size[1]:
                    continue
                else:
                    neighboursData.append(self.getTile(row + i, col + j))
        return neighboursData
    

    def showBombs(self) -> list:
        for bomb_pos in self.__bombsList:
            self.getTile(bomb_pos[0], bomb_pos[1]).setClicked()
        return self.__bombsList
    

    def getSize(self) -> tuple:
        return self.__size
    

    def getTile(self, row: int, col: int) -> Tile:
        return self.__board[row][col]
