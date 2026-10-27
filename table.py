import pygame
from pygame import Surface, Rect


def drawX(surface:Surface,x:float,y:float,length:float,width:float):
    pygame.draw.line(surface,"blue",(x,y),(x+width,y+length),10)
    pygame.draw.line(surface, "blue", (x, y+length), (x+width,y),10)

def drawO(surface:Surface,x:float,y:float,length:float,width:float):
    pygame.draw.circle(surface,"red",(x+(width/2),y+(length/2)),width/2,10)

class Table:
    def __init__(self):
        self.table = [["blank","blank","blank"],
                      ["blank","blank","blank"],
                      ["blank","blank","blank"]]

        self.posRects = []

    def drawTable(self,screen:Surface):
        if screen.get_height() != screen.get_width():
            return False

        metric = 350/3
        pygame.draw.line(screen,"black",(metric+25,25),(metric+25,375),5)
        pygame.draw.line(screen, "black", ((2*metric)+25, 25), ((2*metric) + 25, 375), 5)
        pygame.draw.line(screen,"black",(25,metric+25),(375,metric+25),5)
        pygame.draw.line(screen, "black", (25, (2*metric) + 25), (375, (2*metric) + 25), 5)

        self.posRects = [Rect(31, 30, 100, 100), Rect(32.5 + metric, 30, 100, 100), Rect(33 + (metric * 2), 30, 100, 100),
                         Rect(31, 33 + metric, 100, 100), Rect(32.5 + metric, 33 + metric, 100, 100), Rect(33 + (metric * 2), 33 + metric, 100, 100),
                         Rect(31, 33 + (metric * 2), 100, 100), Rect(32.5 + metric, 33 + (metric * 2), 100, 100), Rect(33 + (metric * 2), 33 + (metric * 2), 100, 100)]

        for i in range(9):
            match self.table[i//3][i%3]:
                case "X":
                    drawX(screen,self.posRects[i].x,self.posRects[i].y,self.posRects[i].height,self.posRects[i].width)
                case "O":
                    drawO(screen,self.posRects[i].x,self.posRects[i].y,self.posRects[i].height,self.posRects[i].width)

    def markTable(self,symbol,pos):
        col,row = tuple(pos)
        if self.table[int(col)-1][ord(row)-ord("A")] == "blank": #successful mark
            self.table[int(col)-1][ord(row)-ord("A")] = symbol
            return True
        ##print("Unsuccessful",symbol,pos)
        return False #unsuccessful mark

    def isFull(self):
        for x in self.table:
            for y in x:
                if y == "blank":
                    return False
        return True

    def resetTable(self):
        self.table = [["blank", "blank", "blank"],
                      ["blank", "blank", "blank"],
                      ["blank", "blank", "blank"]]

    def winCheck(self):


        for symbol in ["X","O"]:
            #rows
            if symbol == self.table[0][0] == self.table[0][1] == self.table[0][2] or symbol == self.table[1][0] == self.table[1][1] == self.table[1][2] or symbol == self.table[2][0] == self.table[2][1] == self.table[2][2]:
                return symbol
            #columns
            elif symbol == self.table[0][0] == self.table[1][0] == self.table[2][0] or symbol == self.table[0][1] == self.table[1][1] == self.table[2][1] or symbol == self.table[0][2] == self.table[1][2] == self.table[2][2]:
                return symbol
            #crosses
            elif symbol == self.table[0][0] == self.table[1][1] == self.table[2][2] or symbol == self.table[0][2] == self.table[1][1] == self.table[2][0]:
                return symbol

        draw = True
        for x in self.table:
            for y in x:
                if y == "blank":
                    draw = False
                    break
            if not draw:
                break
        if draw:
            return "DRAW"

        return "unfinished"

    def get_obs(self):
        value_mapping = {"X": 1, "O": -1, "blank": 0}
        text_board = {"0": self.table[0][0], "1": self.table[0][1], "2": self.table[0][2],
                "3": self.table[1][0], "4": self.table[1][1], "5": self.table[1][2],
                "6": self.table[2][0], "7": self.table[2][1], "8": self.table[2][2]}
        numerical_board = tuple([value_mapping[text_board[str(i)]] for i in range(9)])
        return numerical_board








