from dataclasses import dataclass, field

@dataclass
class Tile:
    __hasBomb: bool
    __isClicked: bool = False
    __isFlagged: bool = False
    __isDetonated: bool = False
    __neighbours: list = field(default_factory=list) 


    def handleFlagEvent(self) -> None:
        self.__isFlagged = not self.__isFlagged
    

    def handleClickEvent(self) -> None:
        if not self.__isClicked and not self.__isFlagged:
            self.__isClicked = True
            if self.__hasBomb:
                self.__isClicked = True
                self.__isDetonated = True
                print("You lost!")
            else:
                for neighbour in self.__neighbours:
                    if not neighbour.getHasBomb():
                        if neighbour.getValue() == 0:
                            neighbour.handleClickEvent()
                        else:
                            neighbour.setClicked()
                if self.__value == 0 and self.__hasBomb:
                    self.__isClicked = False
                    self.__isFlagged = False
                    self.getNeighbour().handleClickEvent()


    def setNeighbours(self, neighboursData: list) -> None:
        self.__neighbours = neighboursData
        self.setValue()
    

    def setValue(self) -> int:
        self.__value = 0
        for neighbour in self.__neighbours:
            if neighbour.getHasBomb() == True:
                self.__value += 1
    

    def setClicked(self) -> None:
        self.__isClicked = True
    

    def getValue(self) -> int:
        return self.__value


    def getHasBomb(self) -> bool:
        return self.__hasBomb
    

    def getIsClicked(self) -> bool:
        return self.__isClicked
    

    def getIsFlagged(self) -> bool:
        return self.__isFlagged


    def isDetonated(self) -> bool:
        return self.__isDetonated
    
    
    def getNeighbour(self):
        return self.__neighbours[0]