from enum import Enum

class tablePos:
    def __init__(self,col:int,row:chr):
        self.col = col
        self.row = row

    @staticmethod
    def toTableIndex(pos:str):
        pos = pos.upper()
        match pos:
            case "1A": return 0
            case "1B": return 1
            case "1C": return 2
            case "2A": return 3
            case "2B": return 4
            case "2C": return 5
            case "3A": return 6
            case "3B": return 7
            case "3C": return 8
            case _: raise Exception("Invalid Pos")


    @staticmethod
    def fromTableIndex(index:int):
        match index:
            case 0: return "1A"
            case 1: return "1B"
            case 2: return "1C"
            case 3: return "2A"
            case 4: return "2B"
            case 5: return "2C"
            case 6: return "3A"
            case 7: return "3B"
            case 8: return "3C"
            case _: raise Exception("Invalid Index")

class turnState(Enum):
    X = "X"
    O = "O"

