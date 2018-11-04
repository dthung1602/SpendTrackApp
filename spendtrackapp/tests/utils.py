import inspect
import sys

from django.test.runner import DiscoverRunner


class NoDbTestRunner(DiscoverRunner):
    """ A test runner to test without database creation """

    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass


class UnbufferedStream(object):
    """
    A stream wrapper that disable buffering

    Ref: https://stackoverflow.com/questions/107705/disable-output-buffering
    """

    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, data):
        self.stream.writelines(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def get_class_that_defined_method(method):
    """
    Return the name of the class that defines given method

    Ref: https://stackoverflow.com/questions/3589311/get-defining-class-of-unbound-method-object-in-python-3/25959545#25959545
    """

    if inspect.ismethod(method):
        for cls in inspect.getmro(method.__self__.__class__):
            if cls.__dict__.get(method.__name__) is method:
                return cls.__name__
        method = method.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(method):
        cls = getattr(inspect.getmodule(method),
                      method.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
        if isinstance(cls, type):
            return cls.__name__
    return getattr(method, '__objclass__', None).__name__  # handle special descriptor objects


def data_provider(data_provider_function, verbose=True):
    """PHPUnit style data provider decorator"""

    def test_decorator(test_function):
        def new_test_function(self, *args):
            i = 0
            if verbose:
                print("\nTest class   : " + get_class_that_defined_method(test_function))
                print("Test function: " + test_function.__name__)
            for data_set in data_provider_function():
                try:
                    if verbose:
                        print("    #" + str(i).rjust(2, '0') + ": ", end='')
                    test_function(self, *data_set)
                    i += 1
                except AssertionError:
                    if verbose:
                        print("Failed with data set #%d: " % i, end='', file=sys.stderr)
                        print(data_set, file=sys.stderr)
                    raise
                else:
                    if verbose:
                        print("passed")
            if verbose:
                print("----------------------------\n")

        return new_test_function

    return test_decorator
