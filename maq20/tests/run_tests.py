import unittest
import imp
import os
import sys


def main():
    try:
        imp.find_module("maq20")
        found = True
    except ImportError:
        found = False
    if not found:
        tests_dir_path = os.path.abspath(os.path.dirname(__file__))
        maq20_path = os.path.split(os.path.split(tests_dir_path)[0])[0]
        sys.path.extend([maq20_path])
    print("Running tests for maq20.utilities")
    unittest.main("maq20.tests.test_utilities", exit=False)
    print("Running tests for MAQ20 System")
    unittest.main("maq20.tests.test_maq20", exit=True)


if __name__ == "__main__":
    main()
