import unittest
from pyvalid import accepts, returns


class AcceptsDecorator(unittest.TestCase):

    def setUp(self):

        @accepts(int, (float, int, None, 'None'), (str, 10))
        def func1(arg1, arg2, arg3=3, arg4=4):
            return arg1, arg2, arg3, arg4

        self.func1 = func1

    def test_positional_args(self):
        args = int(), float(), str(), int()
        returns = self.func1(*args)
        self.assertEqual(args, returns)
        args = int(), int(), 10, 'another value'
        returns = self.func1(*args)
        self.assertEqual(args, returns)
        args = int(), None, str()
        returns = self.func1(*args)
        self.assertEqual(args + (4, ), returns)
        args = int(), int()
        returns = self.func1(*args)
        self.assertEqual(args + (3, 4), returns)

    def test_keyword_args(self):
        # With two last keyword params.
        returns = self.func1(int(), int(), arg3='3', arg4=4.0)
        expected_returns = int(), int(), '3', 4.0
        self.assertEqual(expected_returns, returns)
        # With all keyword params.
        returns = self.func1(arg4=11, arg3=10, arg2=9, arg1=8)
        expected_returns = 8, 9, 10, 11
        self.assertEqual(expected_returns, returns)



    @unittest.expectedFailure
    def test_invalid_value1(self):
        # First argument is invalid.
        args = str(), float(), str(), int()
        self.func1(*args)

    @unittest.expectedFailure
    def test_invalid_value2(self):
        # Second argument is invalid.
        args = int(), str(), str()
        self.func1(*args)

    @unittest.expectedFailure
    def test_invalid_value3(self):
        # Third argument is invalid.
        args = int(), None, None
        self.func1(*args)


class ReturnsDecorator(unittest.TestCase):

    def setUp(self):

        @returns(float, int)
        def func1(arg):
            return arg

        @returns(str, None, -1)
        def func2(arg):
            return arg

        self.func1 = func1
        self.func2 = func2

    def test_valid_returns(self):
        self.assertEqual(self.func1(int()), int())
        self.assertEqual(self.func1(float()), float())
        self.assertEqual(self.func2(str()), str())
        self.assertIsNone(self.func2(None))
        self.assertEqual(self.func2(-1), -1)

    @unittest.expectedFailure
    def test_invalid_returns1(self):
        self.func1(str())

    @unittest.expectedFailure
    def test_invalid_returns2(self):
        self.func1(None)

    @unittest.expectedFailure
    def test_invalid_returns4(self):
        self.func2(int())


if __name__ == '__main__':
    unittest.main()
