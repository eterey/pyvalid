import unittest
from pyvalid import accepts, ArgumentValidationError


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

        def func4_checker1(val):
            return val == 'val1'

        def func4_checker2(val):
            return val == 'val2'

        @accepts(func4_checker1, [func4_checker2, 'val3', bool])
        def func4(arg1, arg2):
            return arg1, arg2

        self.func4 = func4

        @accepts(arg1=[str, int], arg2=['val1', 'val2'])
        def func5(**kwargs):
            return kwargs

        self.func5 = func5

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
        # First argument is invalid.
        args = str(), float(), str(), int()
        self.assertRaises(ArgumentValidationError, self.func1, *args)
        # Second argument is invalid.
        args = int(), str(), str()
        self.assertRaises(ArgumentValidationError, self.func1, *args)
        # Third argument is invalid.
        args = int(), None, None
        self.assertRaises(ArgumentValidationError, self.func1, *args)

    def test_keyword_args(self):
        # With two last keyword params.
        result = self.func1(int(), int(), arg3='3', arg4=4.0)
        expected_result = int(), int(), '3', 4.0
        self.assertEqual(expected_result, result)
        # With all keyword params.
        result = self.func1(arg4=11, arg3=10, arg2=9, arg1=8)
        expected_result = 8, 9, 10, 11
        self.assertEqual(expected_result, result)
        # With invalid keyword parameter `arg1`.
        kwargs = {
            'arg1': str(),
            'arg2': 9,
            'arg3': 10,
            'arg4': 11
        }
        self.assertRaises(ArgumentValidationError, self.func1, **kwargs)

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
        # First argument is invalid.
        args = int(), int(), True, True
        self.assertRaises(ArgumentValidationError, self.func2, *args)
        # Last argument is invalid.
        args = str(), int(), True, int()
        self.assertRaises(ArgumentValidationError, self.func2, *args)

    def test_args_dict1(self):
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
        # First argument is invalid.
        self.assertRaises(
            ArgumentValidationError,
            self.func3,
            int(), arg2=int(), arg3=True, arg4=True
        )
        # Last argument is invalid.
        self.assertRaises(
            ArgumentValidationError,
            self.func3,
            str(), arg2=int(), arg3=True, arg4=int()
        )

    def test_args_dict2(self):
        # Send all keyword arguments.
        kwargs = {
            'arg1': str(),
            'arg2': 'val1'
        }
        result = self.func5(**kwargs)
        self.assertEqual(kwargs, result)
        # Don't send last argument.
        kwargs = {'arg1': int()}
        result = self.func5(**kwargs)
        self.assertEqual(kwargs, result)
        # Don't send any arguments.
        result = self.func5()
        self.assertEqual(result, dict())
        # First argument is invalid.
        self.assertRaises(
            ArgumentValidationError,
            self.func5,
            arg1=None, arg2='val2'
        )
        # Second argument is invalid.
        self.assertRaises(
            ArgumentValidationError,
            self.func5,
            arg1=str(), arg2=None
        )

    def test_validation_func(self):
        args = 'val1', 'val2'
        result = self.func4(*args)
        self.assertEqual(args, result)
        args = 'val1', 'val2'
        result = self.func4(*args)
        self.assertEqual(args, result)
        args = 'val1', True
        result = self.func4(*args)
        self.assertEqual(args, result)
        # First argument is invalid
        self.assertRaises(ArgumentValidationError, self.func4, 'val2', 'val2')
        # Second argument is invalid
        self.assertRaises(ArgumentValidationError, self.func4, 'val1', 'val1')
        # Both arguments are invalid
        self.assertRaises(ArgumentValidationError, self.func4, 'val0', 'val0')


if __name__ == '__main__':
    unittest.main()
