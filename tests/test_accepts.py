import unittest

from pyvalid import ArgumentValidationError, InvalidArgumentNumberError, \
    accepts
from pyvalid.validators import is_validator
from pyvalid.validators import IsValid


class AcceptsDecoratorTestCase(unittest.TestCase):

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

        @accepts(arg1=str, arg2=(float, int), arg3=bool, arg4=bool)
        def func4(arg1=str(), **kwargs):
            return arg1, kwargs

        self.func4 = func4

        @is_validator
        def func5_checker1(val):
            IsValid.status = val == 'val1'
            return IsValid

        @is_validator
        def func5_checker2(val):
            IsValid.status = val == 'val2'
            return IsValid

        @accepts(func5_checker1, [func5_checker2, 'val3', bool])
        def func5(arg1, arg2):
            return arg1, arg2

        self.func5 = func5

        @accepts(arg1=[str, int], arg2=['val1', 'val2'])
        def func6(**kwargs):
            return kwargs

        self.func6 = func6

        @accepts(arg2=float)
        def func7(arg1, arg2):
            return arg1, arg2

        self.func7 = func7

        @accepts(bool)
        def func_with_doc():
            """TEST_DOCSTRING"""
            pass

        self.func_with_doc = func_with_doc

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
        args = str(), float()
        result = self.func7(*args)
        self.assertEqual(args, result)
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
        # With invalid keyword parameter "arg1".
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
        result = self.func4(arg1, **kwargs)
        self.assertEqual((arg1, kwargs), result)
        # Don't send last argument.
        kwargs = {
            'arg2': float(), 'arg3': False,
        }
        result = self.func3(arg1, **kwargs)
        self.assertEqual((arg1, kwargs), result)
        result = self.func4(arg1, **kwargs)
        self.assertEqual((arg1, kwargs), result)
        # Send only first argument.
        result = self.func3(str())
        self.assertEqual((str(), dict()), result)
        result = self.func4(str())
        self.assertEqual((str(), dict()), result)
        # First argument is invalid.
        self.assertRaises(
            ArgumentValidationError,
            self.func3,
            int(), arg2=int(), arg3=True, arg4=True
        )
        self.assertRaises(
            ArgumentValidationError,
            self.func4,
            int(), arg2=int(), arg3=True, arg4=True
        )
        # Last argument is invalid.
        self.assertRaises(
            ArgumentValidationError,
            self.func3,
            str(), arg2=int(), arg3=True, arg4=int()
        )
        self.assertRaises(
            ArgumentValidationError,
            self.func4,
            str(), arg2=int(), arg3=True, arg4=int()
        )

    def test_args_dict2(self):
        # Send all keyword arguments.
        kwargs = {
            'arg1': str(),
            'arg2': 'val1'
        }
        result = self.func6(**kwargs)
        self.assertEqual(kwargs, result)
        # Don't send last argument.
        kwargs = {'arg1': int()}
        result = self.func6(**kwargs)
        self.assertEqual(kwargs, result)
        # Don't send any arguments.
        result = self.func6()
        self.assertEqual(result, dict())
        # First argument is invalid.
        self.assertRaises(
            ArgumentValidationError,
            self.func6,
            arg1=None, arg2='val2'
        )
        # Second argument is invalid.
        self.assertRaises(
            ArgumentValidationError,
            self.func6,
            arg1=str(), arg2=None
        )

    def test_validation_func(self):
        args = 'val1', 'val2'
        result = self.func5(*args)
        self.assertEqual(args, result)
        args = 'val1', 'val2'
        result = self.func5(*args)
        self.assertEqual(args, result)
        args = 'val1', True
        result = self.func5(*args)
        self.assertEqual(args, result)
        # First argument is invalid
        self.assertRaises(ArgumentValidationError, self.func5, 'val2', 'val2')
        # Second argument is invalid
        self.assertRaises(ArgumentValidationError, self.func5, 'val1', 'val1')
        # Both arguments are invalid
        self.assertRaises(ArgumentValidationError, self.func5, 'val0', 'val0')

    def test_docstring(self):
        self.assertEqual(self.func_with_doc.__doc__, 'TEST_DOCSTRING')

    def test_args_number_validation(self):
        # First two arguments are missing
        self.assertRaises(InvalidArgumentNumberError, self.func1)
        # The second argument is missing
        args = str()
        self.assertRaises(InvalidArgumentNumberError, self.func1, *args)
        # All arguments are optional there, so everything should be fine
        try:
            self.func4()
        except InvalidArgumentNumberError:
            self.fail(
                'func4() unexpectedly raised the InvalidArgumentNumberError!'
            )
        try:
            self.func6()
        except InvalidArgumentNumberError:
            self.fail(
                'func4() unexpectedly raised the InvalidArgumentNumberError!'
            )

    def test_ordinal(self):
        accepts_instance = accepts()
        ordinal_func = accepts_instance._Accepts__ordinal

        actual_result = ordinal_func(1)
        expected_result = '1st'
        self.assertEqual(actual_result, expected_result)

        actual_result = ordinal_func(2)
        expected_result = '2nd'
        self.assertEqual(actual_result, expected_result)

        actual_result = ordinal_func(3)
        expected_result = '3rd'
        self.assertEqual(actual_result, expected_result)

        actual_result = ordinal_func(5)
        expected_result = '5th'
        self.assertEqual(actual_result, expected_result)

        actual_result = ordinal_func(10)
        expected_result = '10th'
        self.assertEqual(actual_result, expected_result)

        actual_result = ordinal_func(12)
        expected_result = '12th'
        self.assertEqual(actual_result, expected_result)

        actual_result = ordinal_func(21)
        expected_result = '21st'
        self.assertEqual(actual_result, expected_result)

        actual_result = ordinal_func(22)
        expected_result = '22nd'
        self.assertEqual(actual_result, expected_result)

        actual_result = ordinal_func(23)
        expected_result = '23rd'
        self.assertEqual(actual_result, expected_result)

        actual_result = ordinal_func(25)
        expected_result = '25th'
        self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
