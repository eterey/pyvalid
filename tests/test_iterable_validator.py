import unittest
from pyvalid.validators import IterableValidator


class IterableValidatorTestCase(unittest.TestCase):

    def test_empty_allowed(self):
        """
        Verify empty_iterable_checker() method.
        """
        validator = IterableValidator(empty_allowed=False)
        self.assertTrue(validator([1, 3, 25, 14]))
        self.assertFalse(validator([]))

        validator = IterableValidator(empty_allowed=True)
        self.assertTrue(validator([1, 3, 25, 14]))
        self.assertTrue(validator([]))

    def test_elements_type(self):
        """
        Verify element_type_checker() method.
        """
        validator = IterableValidator(elements_type=int)
        self.assertTrue(validator([1, 3, 25, 14]))
        self.assertFalse(validator([3.56, 6.4532, 65.57, 5.546]))
        self.assertFalse(validator(['CPython', 'PyPy', 'Jython', 'Cython']))

        validator = IterableValidator(elements_type=float)
        self.assertFalse(validator([1, 3, 25, 14]))
        self.assertTrue(validator([3.56, 6.4532, 65.57, 5.546]))
        self.assertFalse(validator(['CPython', 'PyPy', 'Jython', 'Cython']))

        validator = IterableValidator(elements_type=str)
        self.assertFalse(validator([1, 3, 25, 14]))
        self.assertFalse(validator([3.56, 6.4532, 65.57, 5.546]))
        self.assertTrue(validator(['CPython', 'PyPy', 'Jython', 'Cython']))

    def test_sign(self):
        """
        Verify elements_sign_checker() method.
        """
        validator = IterableValidator(sign='positive')
        self.assertTrue(validator([1, 3, 25, 14]))
        self.assertFalse(validator([-1, -3, -25, -14]))

        validator = IterableValidator(sign='negative')
        self.assertTrue(validator([-1, -3, -25, -14]))
        self.assertFalse(validator([-1, 3, 25, -14]))

    def test_mixed(self):
        """
        Verify the validator for different types of iterables.
        """
        validator = IterableValidator(empty_allowed=False, elements_type=int, sign="positive")
        self.assertTrue(validator([1, 3, 25, 14]))  # List
        self.assertTrue(validator((1, 3, 25, 3)))  # Tuple
        self.assertTrue(validator({1: 'pyvalid', 2: 'cython'}))  # Dictionary
        self.assertTrue(validator((1, 3, 25, 14)))  # Set
        self.assertFalse(validator(8))  # Integer


if __name__ == '__main__':
    unittest.main()
