import datatypes
import spread_sheet_op

class BasicSpreadSheet(SpreadSheetOp):
    """
    Spread sheet implementation.
    See docstrings in SpreadSheetOp for information on each function.
    """
    _sheet_inst = None

    def __init__(self, formulas):
        self.formulas = formulas
        _sheet_inst = self 

    def valueAt(position):
        formula = _sheet_inst.formulas[position[0]][position[1]]

        def eval_value(value):
            """
            Evaluates a value.
            value: a Value
            """
            if (isinstance(value.value, (int, long, float, complex))):
                return value.value
            else:
                return _sheet_inst.valueAt(*value.value)

        val_total = eval_value(formula.value)

        while(formula.operation != None and formula.operation.op != Op.NONE):
            cur_op = formula.operation.op
            cur_value = eval_value(formula.operation.formula.value)
            if (cur_op == Op.ADD):
                val_total = val_total + cur_value
            else:
                val_total = val_total * cur_value

        return val_total
    
    def replace(position, formula):
        _sheet_inst.formulas[position[0]][position[1]] = formula
