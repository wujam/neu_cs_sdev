import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

from spread import *

def main():
    print("Building spreadsheet")
    formula1 = Formulas(Value(2), Operation(Op.ADD, Formulas(Value(3), Operation(Op.MUL, Formulas(Value(7), Operation(Op.NONE, None))))))
    formula2 = Formulas(Value((0,0)), Operation(Op.NONE, None))
    formula3 = Formulas(Value((0,1)), Operation(Op.ADD, Formulas(Value(9), Operation(Op.NONE, None))))
    spreadsheet = BasicSpreadSheet([[formula1,formula2], [formula3, formula2]])
    print("Value at (0,0), expected: 35, actual: " + str(BasicSpreadSheet.valueAt((0,0))))
    print("Value at (0,1), expected: 35, actual: " + str(BasicSpreadSheet.valueAt((0,1))))
    print("Value at (1,0), expected: 44, actual: " + str(BasicSpreadSheet.valueAt((1,0))))
    print("Value at (1,1), expected: 35, actual: " + str(BasicSpreadSheet.valueAt((1,1))))

    print("Replacing formula at (1,1) with adding (0,0) to (0,0)")
    formula4 = Formulas(Value((0,0)), Operation(Op.ADD, Formulas(Value((0,0)), Operation(Op.NONE, None))))
    BasicSpreadSheet.replace((1,1), formula4)
    print("Value at (0,0), expected: 35, actual: " + str(BasicSpreadSheet.valueAt((0,0))))
    print("Value at (0,1), expected: 35, actual: " + str(BasicSpreadSheet.valueAt((0,1))))
    print("Value at (1,0), expected: 44, actual: " + str(BasicSpreadSheet.valueAt((1,0))))
    print("Value at (1,1), expected: 70, actual: " + str(BasicSpreadSheet.valueAt((1,1))))

if __name__ == "__main__":
    main()
