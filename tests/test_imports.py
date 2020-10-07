import unittest


class TestImports(unittest.TestCase):

    def test_pyvalid_import(self):
        import pyvalid
        self.assertTrue(pyvalid)
        self.assertTrue(pyvalid.accepts)
        self.assertTrue(pyvalid.returns)
        self.assertTrue(pyvalid.switch)
        self.assertTrue(pyvalid.version)
        self.assertTrue(pyvalid.validators)
        self.assertTrue(pyvalid.validators.NumberValidator)
        self.assertTrue(pyvalid.validators.StringValidator)
        self.assertTrue(pyvalid.validators.is_validator)
        self.assertTrue(pyvalid.PyvalidError)
        self.assertTrue(pyvalid.ArgumentValidationError)
        self.assertTrue(pyvalid.InvalidArgumentNumberError)
        self.assertTrue(pyvalid.InvalidReturnTypeError)

    def test_validators_imports(self):
        from pyvalid import validators
        self.assertTrue(validators.is_validator)
        self.assertTrue(validators.Validator)
        self.assertTrue(validators.AbstractValidator)
        self.assertTrue(validators.IterableValidator)
        self.assertTrue(validators.NumberValidator)
        self.assertTrue(validators.StringValidator)


if __name__ == '__main__':
    unittest.main()
