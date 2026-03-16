import abc
from collections.abc import Mapping
from typing import Dict, Generic, Optional, Type, TypeVar, cast

from kafka.protocol.struct import Struct
from kafka.protocol.types import Array, Int16, Int32, Schema, String, TaggedFields


class RequestHeader(Struct):
    SCHEMA = Schema(
        ('api_key', Int16),
        ('api_version', Int16),
        ('correlation_id', Int32),
        ('client_id', String('utf-8'))
    )

    def __init__(self, request: 'Request', correlation_id: int = 0, client_id: str = 'kafka-python') -> None:
        super(RequestHeader, self).__init__(
            request.API_KEY, request.API_VERSION, correlation_id, client_id
        )


class RequestHeaderV2(Struct):
    # Flexible response / request headers end in field buffer
    SCHEMA = Schema(
        ('api_key', Int16),
        ('api_version', Int16),
        ('correlation_id', Int32),
        ('client_id', String('utf-8')),
        ('tags', TaggedFields),
    )

    def __init__(self, request: 'Request', correlation_id: int = 0, client_id: str = 'kafka-python', tags: Optional[Dict] = None) -> None:
        super(RequestHeaderV2, self).__init__(
            request.API_KEY, request.API_VERSION, correlation_id, client_id, tags or {}
        )


class ResponseHeader(Struct):
    SCHEMA = Schema(
        ('correlation_id', Int32),
    )


class ResponseHeaderV2(ResponseHeader):
    SCHEMA = Schema(
        ('correlation_id', Int32),
        ('tags', TaggedFields),
    )


ResponseType = TypeVar('ResponseType', bound='Response')
DictSchema = TypeVar('DictSchema', bound=Mapping[str, object])


class Request(Struct, Generic[ResponseType, DictSchema], metaclass=abc.ABCMeta):
    FLEXIBLE_VERSION = False

    @property
    @abc.abstractmethod
    def API_KEY(self) -> int:
        """Integer identifier for api request"""
        pass

    @property
    @abc.abstractmethod
    def API_VERSION(self) -> int:
        """Integer of api request version"""
        pass

    @property
    @abc.abstractmethod
    def RESPONSE_TYPE(self) -> Type[ResponseType]:
        """The Response class associated with the api request"""
        pass

    def expect_response(self) -> bool:
        """Override this method if an api request does not always generate a response"""
        return True

    def to_object(self) -> DictSchema:
        return cast(DictSchema, _to_object(self.SCHEMA, self))

    def build_header(self, correlation_id: int, client_id: str) -> RequestHeader:
        if self.FLEXIBLE_VERSION:
            return RequestHeaderV2(self, correlation_id=correlation_id, client_id=client_id)
        return RequestHeader(self, correlation_id=correlation_id, client_id=client_id)


class Response(Struct, Generic[DictSchema], metaclass=abc.ABCMeta):
    FLEXIBLE_VERSION = False

    @property
    @abc.abstractmethod
    def API_KEY(self) -> int:
        """Integer identifier for api request/response"""
        pass

    @property
    @abc.abstractmethod
    def API_VERSION(self) -> int:
        """Integer of api request/response version"""
        pass

    def to_object(self) -> DictSchema:
        return cast(DictSchema, _to_object(self.SCHEMA, self))

    @classmethod
    def parse_header(cls, read_buffer) -> None:
        if cls.FLEXIBLE_VERSION:
            return ResponseHeaderV2.decode(read_buffer)
        return ResponseHeader.decode(read_buffer)


def _to_object(schema: 'Schema', data: 'Struct') -> Dict[str, object]:
    obj: Dict[str, object] = {}
    for idx, (name, _type) in enumerate(zip(schema.names, schema.fields)):
        if isinstance(data, Struct):
            val = data.get_item(name)
        else:
            val = data[idx]

        if isinstance(_type, Schema):
            obj[name] = _to_object(_type, val)
        elif isinstance(_type, Array):
            if isinstance(_type.array_of, (Array, Schema)):
                obj[name] = [
                    _to_object(_type.array_of, x)
                    for x in val
                ]
            else:
                obj[name] = val
        else:
            obj[name] = val

    return obj
