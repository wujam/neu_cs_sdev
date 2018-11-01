""" ObserverManager manages Observers """
class ObserverManager:
    def __init__(self, timeout=10):
        self._observers = []
        self._timeout = timeout

    def add_observer(self, observer):
        """ Adds an observer.
        :param Observer observer: an Observer to be added
        """
        self._observers.append(observer)

    def remove_all_observers(self):
        """ Removes all observers """
        self._observers = []

    def notify_all(self, fun_name, *args, **kwargs):
        """ Notifies all observers by calling the given function
        on all observers. If an observer misbehaves they will be
        booted.
        :param String fun_name: name of function to call
        :param list args: arguments of function
        :param list kwargs: keyword arguments of function
        """
        bad_observers = []
        for index, obs in enumerate(self._observers):
            try:
                with timeout(seconds = self._timeout):
                    getattr(obs, fun_name)(*args, **kwargs)
            except Exception:
                bad_observers.append(index)
        for bad_obs_index in reversed(bad_observers):
            del self._observers[bad_obs_index]
