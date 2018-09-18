class InvalidFormulaException(Exception):
    """Exception raised for errors in the JSON formula"""
    def __init__(self):
        self.message = "Invalid formula."


class Spreadsheet:
    """
    Represents a spreadsheet. A rectangular, indexed arrangement 
    of formulas is stored as a dictionary in the field 'data'.
    """
    def __init__(self):
        self.data = {}

    def isJF(self, formula):
        """Validates a given formula for correct format

        :param formula: the string to be validated as a proper formula
        :return: whether or not formula is valid
        :raise: InvalidFormulaException if formula is invalid
        """
        operands = ['+', '*']
        if type(formula) is int:
            return True
        if type(formula) is not list or len(formula) != 3:
            return False
        if formula[0] == '>' and type(formula[1]) is int and type(formula[2]) is int:
            return True
        if self.isJF(formula[0]) and self.isJF(formula[2]) and formula[1] in operands:
            return True

    def load_spreadsheet(self, spreadsheet_array):
        """Validates and sets up spreadsheet data

        :param spreadsheet_array: a dictionary keyed by tuples of 2 non-negative integers to a string value
        :return: this Spreadsheet
        :raises: InvalidFormulaException if formula is invalid
        """
        for k in spreadsheet_array.keys():
            val = spreadsheet_array[k]
            if not self.isJF(val):
                raise InvalidFormulaException
        self.data = spreadsheet_array
        return self
    
    def evaluate_formula(self, formula):
        """Evaluate the given formula as a number

        :param formula: the formula to be evaluated
        :return: the formula's value
        """
        if formula !=0 and not formula:
            return None
        if type(formula) is int:
            return int(formula)
        if formula[0] == '>' and type(formula[1]) is int and type(formula[2]) is int:
            return self.get_value_at(formula[1], formula[2])
        if formula[1] == '+':
            return self.evaluate_formula(formula[0]) + self.evaluate_formula(formula[2])
        if formula[1] == '*':
            return self.evaluate_formula(formula[0]) * self.evaluate_formula(formula[2])
    
    def get_value_at(self, row, col):
        """Returns the value evaluated at a given cell
        
        :param row: a non-negative integer representing the row index
        :param col: a non-negative integer representing the column index
        :return: the value evaluated at the given cell, or None if the cell is blank
        """
        pos = (row, col)
        formula = self.data[pos]
        return self.evaluate_formula(formula)

    def set_formula_at(self, row, col, formula):
        """Sets the value at a given cell position with given formula string
        
        :param row: a non-negative integer representing the row index
        :param col: a non-negative integer representing the column index
        :param formula: a formula string
        :raises: InvalidFormulaException if formula is invalid
        """
        pos = (row, col)
        if self.isJF(formula):
            self.data[pos] = formula
        else:
            raise InvalidFormulaException
    
    