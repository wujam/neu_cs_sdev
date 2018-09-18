import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

from spread import *

def main():
    formula1 = Formulas(Value(2), Operation(Op.ADD, Formulas(Value(3), Operation(Op.MUL, Formulas(Value(7), Operation(Op.NONE, None))))))
    formula2 = Formulas(Value((0,0)), Operation(Op.NONE, None))
    formula3 = Formulas(Value((0,1)), Operation(Op.ADD, Formulas(Value(9), Operation(Op.NONE, None))))
    spreadsheet = BasicSpreadSheet([[formula1,formula2], [formula3, formula2]])
    print(BasicSpreadSheet.valueAt((0,0)))
    print(BasicSpreadSheet.valueAt((0,1)))
    print(BasicSpreadSheet.valueAt((1,0)))
    print(BasicSpreadSheet.valueAt((1,1)))

if __name__ == "__main__":
    main()
