import unittest

from pyvalid.validators import IterableValidator


class IterableValidatorTestCase(unittest.TestCase):

    def test_iterable_type(self):
        """
        Verify iterable_type_checker() method.
        """
        validator = IterableValidator(iterable_type=list)
        self.assertTrue(validator([1, 3, 25, 14]))
        self.assertFalse(validator({1: 'a', 2: 'b'}))

        validator = IterableValidator(iterable_type=tuple)
        self.assertTrue(validator((1, 3, 25, 14)))
        self.assertFalse(validator([1, 3, 25, 14]))

    def test_empty_allowed(self):
        """
        Verify empty_checker() method.
        """
        validator = IterableValidator(empty_allowed=False)
        self.assertTrue(validator([1, 3, 25, 14]))
        self.assertFalse(validator([]))
        self.assertFalse(None)

        validator = IterableValidator(empty_allowed=True)
        self.assertTrue(validator([1, 3, 25, 14]))
        self.assertTrue(validator([]))
        self.assertFalse(None)

    def test_elements_type(self):
        """
        Verify element_type_checker() method.
        """
        validator = IterableValidator(elements_type=int)
        self.assertTrue(validator([1, 3, 25, 14]))
        self.assertFalse(validator([3.56, 6.4532, 65.57, 5.546]))
        self.assertFalse(validator(['CPython', 'PyPy', 'Jython', 'Cython']))
        self.assertTrue(validator([]))  # Ignore empty
        self.assertFalse(None)

        validator = IterableValidator(elements_type=float)
        self.assertFalse(validator([1, 3, 25, 14]))
        self.assertTrue(validator([3.56, 6.4532, 65.57, 5.546]))
        self.assertFalse(validator(['CPython', 'PyPy', 'Jython', 'Cython']))
        self.assertFalse(None)

        validator = IterableValidator(elements_type=str)
        self.assertFalse(validator([1, 3, 25, 14]))
        self.assertFalse(validator([3.56, 6.4532, 65.57, 5.546]))
        self.assertTrue(validator(['CPython', 'PyPy', 'Jython', 'Cython']))
        self.assertFalse(None)

    def test_min_val(self):
        """
        Verify elements_min_val_checker() method.
        """
        validator = IterableValidator(min_val=0)
        self.assertTrue(validator([1, 3, 25, 14]))
        self.assertFalse(validator([-1, -3, -25, -14]))
        self.assertFalse(None)

        validator = IterableValidator(min_val=-50.3)
        self.assertTrue(validator([-1.6, 3.56, 25.53, -14.4]))
        self.assertFalse(validator([-72.67, 3.56, 25.53, -14.4]))
        self.assertFalse(None)

    def test_max_val(self):
        """
        Verify elements_max_val_checker() method.
        """
        validator = IterableValidator(max_val=100)
        self.assertTrue(validator([12, 96, 24, 100]))
        self.assertFalse(validator([104, 205, 835, 143]))
        self.assertFalse(None)

        validator = IterableValidator(max_val=150.25)
        self.assertTrue(validator([-154.6, 45.56, 125.53, -12.4]))
        self.assertFalse(validator([164.67, 33.56, 110.53, -140.4]))
        self.assertFalse(None)

    def test_range(self):
        """
        Verify elements_min_val_checker() and elements_max_val_checker()
        methods.
        """
        with self.assertRaises(ValueError):
            IterableValidator(min_val=100, max_val=50)

        validator = IterableValidator(min_val=50, max_val=100)
        self.assertTrue(validator([60, 80, 100]))
        self.assertTrue(validator([70, 60, 50]))
        self.assertTrue(validator([]))
        self.assertFalse(validator([101, 10, 10, 10]))
        self.assertFalse(validator([-50, -25, 0]))
        self.assertFalse(None)

    def test_mixed(self):
        """
        Verify the validator for different types of iterables.
        """
        validator = IterableValidator(
            empty_allowed=False, elements_type=int, min_val=-128, max_val=128
        )
        self.assertTrue(validator([1, 3, 25, 120]))  # List
        self.assertTrue(validator((1, 3, 25, 3)))  # Tuple
        self.assertTrue(validator({1: 'pyvalid', 2: 'cython'}))  # Dictionary
        self.assertTrue(validator({1, 3, 25, 120}))  # Set
        self.assertFalse(validator(8))  # Integer
        self.assertFalse(None)


if __name__ == '__main__':
    unittest.main()
