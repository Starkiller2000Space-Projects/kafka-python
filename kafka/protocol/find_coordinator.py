from typing import List, Type, TypeVar, final

from kafka.protocol.api import Request, Response
from kafka.protocol.types import Int8, Int16, Int32, Schema, String


class _FindCoordinatorResponse(Response):
    API_KEY = 10

    error_code: int
    coordinator_id: int
    host: str
    port: int


@final
class FindCoordinatorResponse_v0(_FindCoordinatorResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('error_code', Int16),
        ('coordinator_id', Int32),
        ('host', String('utf-8')),
        ('port', Int32)
    )


@final
class FindCoordinatorResponse_v1(_FindCoordinatorResponse):
    API_VERSION = 1
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('error_code', Int16),
        ('error_message', String('utf-8')),
        ('coordinator_id', Int32),
        ('host', String('utf-8')),
        ('port', Int32)
    )


@final
class FindCoordinatorResponse_v2(_FindCoordinatorResponse):
    API_VERSION = 2
    SCHEMA = FindCoordinatorResponse_v1.SCHEMA


_FindCoordinatorResponseType = TypeVar('_FindCoordinatorResponseType', bound=_FindCoordinatorResponse)


class _FindCoordinatorRequest(Request[_FindCoordinatorResponseType]):
    API_KEY = 10

@final
class FindCoordinatorRequest_v0(_FindCoordinatorRequest[FindCoordinatorResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = FindCoordinatorResponse_v0
    SCHEMA = Schema(
        ('consumer_group', String('utf-8'))
    )


@final
class FindCoordinatorRequest_v1(_FindCoordinatorRequest[FindCoordinatorResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = FindCoordinatorResponse_v1
    SCHEMA = Schema(
        ('coordinator_key', String('utf-8')),
        ('coordinator_type', Int8) # 0: consumer, 1: transaction
    )


@final
class FindCoordinatorRequest_v2(_FindCoordinatorRequest[FindCoordinatorResponse_v2]):
    API_VERSION = 2
    RESPONSE_TYPE = FindCoordinatorResponse_v2
    SCHEMA = FindCoordinatorRequest_v1.SCHEMA


FindCoordinatorRequest: List[Type[_FindCoordinatorRequest]] = [FindCoordinatorRequest_v0, FindCoordinatorRequest_v1, FindCoordinatorRequest_v2]
FindCoordinatorResponse: List[Type[_FindCoordinatorResponse]] = [FindCoordinatorResponse_v0, FindCoordinatorResponse_v1, FindCoordinatorResponse_v2]
