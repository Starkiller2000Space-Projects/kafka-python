import abc
from collections.abc import Sequence
from io import BytesIO
from typing import Generic, Tuple, TypeVar

ValueType = TypeVar('ValueType')


class AbstractType(object, Generic[ValueType], metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def encode(self, value: ValueType) -> bytes:
        pass

    @abc.abstractmethod
    def decode(self, data: BytesIO) -> ValueType:
        pass

    def repr(self, value: ValueType) -> str:
        return repr(value)
