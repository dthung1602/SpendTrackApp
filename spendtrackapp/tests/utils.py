from django.test.runner import DiscoverRunner


class NoDbTestRunner(DiscoverRunner):
    """ A test runner to test without database creation """

    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass


def data_provider(data_provider_function):
    """PHPUnit style data provider decorator"""

    def test_decorator(test_function):
        def new_test_function(self, *args):
            i = 0
            print("\nTest function: " + test_function.__name__)
            for data_set in data_provider_function():
                try:
                    print("    #" + str(i) + ": ", end='')
                    test_function(self, *data_set)
                    i += 1
                except AssertionError:
                    print("failed with dataset:")
                    print(data_set)
                    raise
                else:
                    print("passed")
            print("----------------------------\n")

        return new_test_function

    return test_decorator
