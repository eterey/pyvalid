import unittest
from pyvalid import returns, InvalidReturnType
from pyvalid.validators import is_validator


class ReturnsDecoratorTestCase(unittest.TestCase):

    def setUp(self):

        @returns(float, int)
        def func1(arg):
            return arg

        self.func1 = func1

        @returns(str, None, -1)
        def func2(arg):
            return arg

        self.func2 = func2

        @is_validator
        def func3_checker(val):
            return val == 'val1'

        @returns(func3_checker, None, bool)
        def func3(arg):
            return arg

        self.func3 = func3

        @returns()
        def func_with_doc():
            """TEST_DOCSTRING"""
            pass

        self.func_with_doc = func_with_doc

    def test_valid_returns(self):
        # func1
        self.assertEqual(self.func1(int()), int())
        self.assertEqual(self.func1(float()), float())
        self.assertEqual(self.func2(str()), str())
        self.assertRaises(InvalidReturnType, self.func1, str())
        self.assertRaises(InvalidReturnType, self.func1, None)
        # func2
        self.assertIsNone(self.func2(None))
        self.assertEqual(self.func2(-1), -1)
        self.assertRaises(InvalidReturnType, self.func2, int())
        # func3
        self.assertEqual(self.func3('val1'), 'val1')
        self.assertIsNone(self.func3(None), 'val1')
        self.assertEqual(self.func3(True), True)
        self.assertRaises(InvalidReturnType, self.func3, int())

    def test_docstring(self):
        self.assertEqual(self.func_with_doc.__doc__, 'TEST_DOCSTRING')



if __name__ == '__main__':
    unittest.main()
