import unittest

import numpy as np

import torch

from pyvalid.validators import TensorValidator


class TensorValidatorTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.t = torch.Tensor([[0.0688, 0.0843, 0.0000],
                               [0.1810, 0.0000, 0.1470]])

    def test_tensor_type(self):
        """
        Verify tensor_type_checker() method.
        """
        validator = TensorValidator(tensor_type="torch.FloatTensor")
        self.assertTrue(validator(self.t).status)

        validator = TensorValidator(tensor_type="torch.IntTensor")
        self.assertFalse(validator(self.t).status)

    def test_dim(self):
        """
        Verify dimension_checker() method.
        """
        validator = TensorValidator(dim=2)
        self.assertTrue(validator(self.t).status)
        self.assertTrue(validator(torch.Tensor([[]])).status)

        validator = TensorValidator(dim=1)
        self.assertFalse(validator(self.t).status)
        self.assertFalse(validator(torch.Tensor([[]])).status)

    def test_empty_allowed(self):
        """
        Verify empty_checker() method.
        """
        validator = TensorValidator(empty_allowed=False)
        self.assertTrue(validator(self.t))
        self.assertFalse(validator(torch.Tensor([[]])).status)

        validator = TensorValidator(empty_allowed=True)
        self.assertTrue(validator(self.t))
        self.assertTrue(validator(torch.Tensor([[]])).status)
        self.assertTrue(validator(torch.Tensor([[]])).is_warning)

    def test_nans_allowed(self):
        """
        Verify nan_checker() method.
        """
        validator = TensorValidator(nans_allowed=False)
        self.assertTrue(validator(self.t))
        self.assertFalse(validator(torch.Tensor([np.NaN, 7.3459, 0.3454, np.NaN])).status)

        validator = TensorValidator(nans_allowed=True)
        self.assertTrue(validator(self.t))
        self.assertTrue(validator(torch.Tensor([np.NaN, 7.3459, 0.3454, np.NaN])).status)
        self.assertTrue(validator(torch.Tensor([np.NaN, 7.3459, 0.3454, np.NaN])).is_warning)

    def test_mixed(self):
        """
        Verify all the methods of TensorValidator.
        """
        validator = TensorValidator(
            tensor_type="torch.FloatTensor",
            dim=2,
            empty_allowed=False,
            nans_allowed=False
        )
        self.assertTrue(validator(self.t).status)
        self.assertFalse(validator([1, 2]).status)  # Non-tensor
        self.assertFalse(validator(None).status)


if __name__ == '__main__':
    unittest.main()
