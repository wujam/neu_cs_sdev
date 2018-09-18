from abc import ABCMeta, abstractmethod

class SpreadSheetOp:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __init__(self, formulas):
        """
        Constructor for a SpreadSheetOp.
        formulas: [List of [List of Formulas]], will be stored internally
        return: a SpreadSheetOp
        """
        raise NotImplementedError
    
    @abstractmethod
    def valueAt(position):
        """
        Gets the value at the given position.
        position: (Integer, Integer), the first is the row, the second is the column.
        return: Number, the value evaluated at the given position
        """
        raise NotImplementedError

    @abstractmethod
    def replace(position, formula):
        """
        Replaces the value at the given position.
        position: (Integer, Integer), the first is the row, the second is the olumn.
        formula: Formulas, the formula to set at the given cell
        """
        raise NotImplementedError

