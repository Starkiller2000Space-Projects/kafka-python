import abc
from io import BytesIO
from typing import Any

from typing_extensions import Self

from kafka.protocol.abstract import AbstractType
from kafka.protocol.types import Schema
from kafka.util import WeakMethod


class Struct(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def SCHEMA(self) -> Schema:
        """An instance of Schema() representing the structure"""
        ...

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if len(args) == len(self.SCHEMA):
            for i, name in enumerate(self.SCHEMA.names):
                setattr(self, name, args[i])
        elif len(args) > 0:
            raise ValueError('Args must be empty or mirror schema')
        else:
            for name in self.SCHEMA.names:
                setattr(self, name, kwargs.pop(name, None))
            if kwargs:
                raise ValueError('Keyword(s) not in schema %s: %s'
                                 % (list(self.SCHEMA.names),
                                    ', '.join(kwargs.keys())))

    def encode(self) -> None:
        return self.SCHEMA.encode(
            [getattr(self, name) for name in self.SCHEMA.names]
        )

    @classmethod
    def decode(cls, data) -> Self:
        if isinstance(data, bytes):
            data = BytesIO(data)
        return cls(*cls.SCHEMA.decode(data))

    def get_item(self, name: str) -> Any:
        if name not in self.SCHEMA.names:
            raise KeyError("%s is not in the schema" % name)
        return getattr(self, name)

    def __repr__(self) -> None:
        key_vals = []
        for name, field in zip(self.SCHEMA.names, self.SCHEMA.fields):
            key_vals.append('%s=%s' % (name, field.repr(getattr(self, name))))
        return self.__class__.__name__ + '(' + ', '.join(key_vals) + ')'

    def __hash__(self) -> None:
        return hash(self.encode())

    def __eq__(self, other) -> None:
        if self.SCHEMA != other.SCHEMA:
            return False
        for attr in self.SCHEMA.names:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True
