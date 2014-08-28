import unittest
from pyvalid import accepts, returns


class AcceptsDecorator(unittest.TestCase):

    def setUp(self):

        @accepts(int, (float, int, None, 'None'), (str, 10))
        def func1(arg1, arg2, arg3=3, arg4=4):
            return arg1, arg2, arg3, arg4

        self.func1 = func1

        @accepts(str, (float, int), bool, bool)
        def func2(arg1, *args):
            return arg1, args

        self.func2 = func2

        @accepts(str, arg2=(float, int), arg3=bool, arg4=bool)
        def func3(arg1, **kwargs):
            return arg1, kwargs

        self.func3 = func3

    def test_positional_args(self):
        args = int(), float(), str(), int()
        result = self.func1(*args)
        self.assertEqual(args, result)
        args = int(), int(), 10, 'another value'
        result = self.func1(*args)
        self.assertEqual(args, result)
        args = int(), None, str()
        result = self.func1(*args)
        self.assertEqual(args + (4, ), result)
        args = int(), int()
        result = self.func1(*args)
        self.assertEqual(args + (3, 4), result)

    def test_keyword_args(self):
        # With two last keyword params.
        result = self.func1(int(), int(), arg3='3', arg4=4.0)
        expected_result = int(), int(), '3', 4.0
        self.assertEqual(expected_result, result)
        # With all keyword params.
        result = self.func1(arg4=11, arg3=10, arg2=9, arg1=8)
        expected_result = 8, 9, 10, 11
        self.assertEqual(expected_result, result)

    def test_args_list(self):
        # Send all arguments.
        arg1, args = str(), (int(), True, True)
        result = self.func2(arg1, *args)
        self.assertEqual((arg1, args), result)
        # Don't send last argument.
        arg1, args = str(), (float(), False)
        result = self.func2(arg1, *args)
        self.assertEqual((arg1, args), result)
        # Send only first argument.
        result = self.func2(str())
        self.assertEqual((str(), tuple()), result)

    def test_args_dict(self):
        # Send all arguments.
        arg1 = str()
        kwargs = {
            'arg2': int(), 'arg3': True, 'arg4': True
        }
        result = self.func3(arg1, **kwargs)
        self.assertEqual((arg1, kwargs), result)
        # Don't send last argument.
        kwargs = {
            'arg2': float(), 'arg3': False,
        }
        result = self.func3(arg1, **kwargs)
        self.assertEqual((arg1, kwargs), result)
        # Send only first argument.
        result = self.func3(str())
        self.assertEqual((str(), dict()), result)

    @unittest.expectedFailure
    def test_invalid_value1(self):
        # First argument of `func1` is invalid.
        self.func1(str(), float(), str(), int())

    @unittest.expectedFailure
    def test_invalid_value2(self):
        # Second argument of `func1` is invalid.
        self.func1(int(), str(), str())

    @unittest.expectedFailure
    def test_invalid_value3(self):
        # Third argument of `func1` is invalid.
        self.func1(int(), None, None)

    @unittest.expectedFailure
    def test_invalid_value4(self):
        # First argument of `func2` is invalid.
        self.func2(int(), int(), True, True)

    @unittest.expectedFailure
    def test_invalid_value5(self):
        # Last argument of `func2` is invalid.
        self.func2(str(), int(), True, int())

    @unittest.expectedFailure
    def test_invalid_value6(self):
        # First argument of `func3` is invalid.
        self.func3(int(), arg2=int(), arg3=True, arg4=True)

    @unittest.expectedFailure
    def test_invalid_value7(self):
        # Last argument if `func3` is invalid.
        self.func3(str(), arg2=int(), arg3=True, arg4=int())


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
