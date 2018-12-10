import importlib
import inspect
import importlib.util

def find_subclass_in_source(path, parent):
    """Finds a subclass of parent in a source file
    :param path: path to the source file
    :param Type parent: class to search for subclasses of
    :rtype Type or bool: the subclass or False
    """
    # a string module name is needed here but it is never needed again
    spec = importlib.util.spec_from_file_location("mod", path)
    # importlib returns None if the file isn't found
    if spec is None:
        return
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    found = inspect.getmembers(module,
                               predicate=lambda o: inspect.isclass(o) and \
                                                   issubclass(o, parent) and \
                                                   o != parent)
    # return the first matching class found
    if len(found) > 0:
        _, found_class = found[0]
        return found_class
    return False

