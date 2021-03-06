from .datatypes import *
from .spread_sheet_op import *
class BasicSpreadSheet(SpreadSheetOp):
    """
    Spread sheet implementation.
    See docstrings in SpreadSheetOp for information on each function.
    """
    _sheet_inst = None

    def __init__(self, formulas):
        self.formulas = formulas
        self.__class__._sheet_inst = self 

    def valueAt(position):
        formula = BasicSpreadSheet._sheet_inst.formulas[position[0]][position[1]]

        def eval_value(value):
            """
            Evaluates a value.
            value: a Value
            """
            if (isinstance(value.value, (int, float))):
                return value.value
            else:
                return BasicSpreadSheet.valueAt(value.value)

        val_total = eval_value(formula.value)

        while(formula.operation != None and formula.operation.op != Op.NONE):
            cur_op = formula.operation.op
            cur_value = eval_value(formula.operation.formulas.value)
            if (cur_op == Op.ADD):
                val_total = val_total + cur_value
            else:
                val_total = val_total * cur_value
            formula = formula.operation.formulas

        return val_total
    
    def replace(position, formula):
        BasicSpreadSheet._sheet_inst.formulas[position[0]][position[1]] = formula
