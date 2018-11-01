from abc import ABC, abstractmethod
""" ObserverManager manages Observers """
class ObserverManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def add_observer(self, observer):
        """ Adds an observer.
        :param Observer observer: an Observer to be added
        """
        pass

    @abstractmethod
    def remove_all_observers(self):
        """ Removes all observers """
        pass

    @abstractmethod
    def notify_all(self, fun_name, *args, **kwargs):
        """ Notifies all observers by calling the given function
        on all observers. If an observer misbehaves they will be
        booted.
        :param String fun_name: name of function to call
        :param list args: arguments of function
        :param list kwargs: keyword arguments of function
        """
        pass
