from enum import Enum

class Value:
    """
    Class to represent a value.
    Is either a constant or a reference to a valid position of another cell
    """
    def __init__(self, value):
        """
        Constructs a Value object with the given value
        value: Number or a (Integer, Integer) representing row, column
        """
        self.value = value

class Op(Enum):
    NONE = 0
    ADD = 1
    MUL = 2

    @classmethod
    def is_op(cls, val):
        """
        Check if the given is in the enum.
        cls: Op class
        val: Value to check
        """
        return any(op.value == val for op in cls)

class Operation:
    """
    Class to represent an operation.
    Contains 2 fields, op and formulas
    """
    def __init__(self, operation, formulas):
        """
        Constructs a Operation object with an Op and a Formulas.
        operation: Op, the op to use
        formulas: Formulas, the formulas to use
        """
        self.op = operation
        self.formulas = formulas

class Formulas:
    """
    Class to represent formulas
    """
    def __init__(self, value, operation):
        """
        Constructs a Formulas object with a Value and an Operation
        value: Value, the value to use
        operation: Operation, the operation to use
        """
        self.value = value
        self.operation = operation
