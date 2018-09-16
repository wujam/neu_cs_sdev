from enum import Enum

class Value:
    """
    Class to represent a value.
    Is either a constant or a reference to a valid position of another cell
    """
    def __init__(self, value):
        self.value = value

class Op:
    NOOP = 0
    ADD = 1
    MUL = 2

class Operation:
    """
    Class to represent an operation.
    Contains 2 fields, op and formulas
    """
    def __init__(self, operation, formulas):
        self.op = operation
        self.formulas = formulas

class Formulas:
    """
    Class to represent formulas
    """
    def __init__(self, value, operation):
        self.value = value
        self.operation = operation
