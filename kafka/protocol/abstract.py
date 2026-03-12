import abc
from collections.abc import Sequence
from typing import Any, Tuple


class AbstractType(object, metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def encode(cls, value: Sequence[Any]) -> bytes: # pylint: disable=no-self-argument
        pass

    @classmethod
    @abc.abstractmethod
    def decode(cls, data: bytes) -> Tuple[Any, ...]: # pylint: disable=no-self-argument
        pass

    @classmethod
    def repr(cls, value) -> str:
        return repr(value)
