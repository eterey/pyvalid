import torch

from pyvalid import accepts
from pyvalid.validators import AbstractValidator, IsValid, StringValidator


class TensorValidator(AbstractValidator):
    """
    Performs certain checks to check if the given tensor is valid or not.

    Example:

    .. code-block:: python

        X = torch.Tensor([
            [0.0500, 0.0000, 0.0688, 0.0843, 0.0000, 0.0000, 0.1896, 0.0105],
            [0.0500, 0.0000, 0.0528, 0.1810, 0.0000, 0.0000, 0.1470, 0.0000]
        ])
        validator = TensorValidator(
            tensor_type="torch.FloatTensor", empty_check=True, nan_check=True, dim=2
        )

        @accepts(validator)
        def example(X):
            pass

    """
    @classmethod
    def tensor_type_checker(cls, val, tensor_type):
        """Checks the tensor types with CPU variants.

        Args:
            val (torch.Tensor):
                Tensor whose type is to be validated.
            tensor_type (str):
                Expected type of tensor.
                Ex: "torch.IntTensor", "torch.FloatTensor", "torch.ByteTensor".

        Returns (bool):
            True:
                If the type of given tensor matches the required type.
            False:
                If the type of given tensor does not match the required type.

        """
        IsValid.status = val.type() == tensor_type
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"expected type '{tensor_type}' but got '{type(val)}' instead."

        return IsValid

    @classmethod
    def dimension_checker(cls, val, dim):
        """Checks if given tensor is of dimension <dim>.

        Args:
            val (torch.Tensor):
                Tensor whose dimension is to be validated.
            dim (int):
                Expected dimension of the tensor.

        Returns (bool):
            True:
                If the given tensor is of required dimension.
            False:
                If the given tensor is not of required dimension.

        """
        IsValid.status = val.dim() == dim
        if not IsValid.status:
            IsValid.msg = f"In {IsValid.get_caller()}, " \
                          f"expected tensor of dimension '{dim}' but got '{val.dim()}' instead."

        return IsValid

    @classmethod
    def empty_checker(cls, val, empty_allowed):
        """Checks if the tensor is empty or not.

        Args:
            val (torch.Tensor):
                Tensor whose contents needs to be validated.
            empty_allowed (bool):
                If this flag is set to ``False``, this method raises exception and
                terminates the execution if the tensor is empty.
                If set to ``True``, it raises a warning and continues with
                the execution.

        Returns (bool):
            True:
                If the tensor is not empty.
            False:
                If the tensor is empty.

        """
        if not empty_allowed:
            IsValid.status = val.nelement() != 0
            if not IsValid.status:
                IsValid.msg = f"In {IsValid.get_caller()}, " \
                              f"expected non-empty tensor but got '{val}"
        else:
            IsValid.status = True
            IsValid.is_warning = True
            IsValid.msg = "In {IsValid.get_caller()}, tensor is empty."

        return IsValid

    @classmethod
    def nan_checker(cls, val, nans_allowed):
        """Checks if the tensor has np.NaN values or not.

        Args:
            val (torch.Tensor):
                Tensor to be validated.
            nans_allowed (bool):
                If this flag is set to ``False``, this method raises exception and
                terminates the execution if the tensor has NaNs.
                If set to ``True``, it raises a warning and continues with
                the execution.

        Returns (bool):
            True:
                If the given tensor is free of NaNs.
            False:
                If the given tensor contains NaNs.

        """
        if not nans_allowed:
            IsValid.status = torch.isnan(val).sum().item() == 0
            if not IsValid.status:
                IsValid.msg = f"In {IsValid.get_caller()}, " \
                              f"expected NaN free tensor but got '{val}"
        else:
            IsValid.status = True
            IsValid.is_warning = True
            IsValid.msg = "In {IsValid.get_caller()}, Tensor contains NaN values."

        return IsValid

    @property
    def checkers(self):
        return self.__checkers

    @accepts(object,
             tensor_type=StringValidator(in_range=[
                 "torch.CharTensor",
                 "torch.IntTensor",
                 "torch.ShortTensor",
                 "torch.LongTensor",
                 "torch.FloatTensor",
                 "torch.DoubleTensor",
                 "torch.ByteTensor",
                 "torch.BoolTensor",
                 "torch.HalfTensor"
             ]),
             dim=int,
             empty_check=bool,
             nan_check=bool)
    def __init__(self, **kwargs):
        self.__checkers = {
            TensorValidator.tensor_type_checker: [kwargs.get('tensor_type', None)],
            TensorValidator.dimension_checker: [kwargs.get('dim', None)],
            TensorValidator.empty_checker: [kwargs.get('empty_allowed', None)],
            TensorValidator.nan_checker: [kwargs.get('nans_allowed', None)],
        }
        AbstractValidator.__init__(self, allowed_types=torch.Tensor)
