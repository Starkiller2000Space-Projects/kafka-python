from io import BytesIO
from typing import List, Tuple, Type, TypeVar, final

from typing_extensions import NotRequired, TypedDict

from kafka.protocol.api import Request, Response
from kafka.protocol.types import Array, CompactArray, CompactString, Int16, Int32, Schema, TaggedFields


class _ApiVersionsResponseApiVersionDict(TypedDict):
    api_key: int
    min_version: int
    max_version: int


class _ApiVersionsResponseDict(TypedDict):
    error_code: int
    api_versions: List[_ApiVersionsResponseApiVersionDict]
    throttle_time_ms: NotRequired[int]  # added in v1


class _ApiVersionsResponse(Response[_ApiVersionsResponseDict]):
    API_KEY = 18

    error_code: int
    api_versions: List[Tuple[int, int, int]]
    throttle_time_ms: int  # added in v1


class BaseApiVersionsResponse(_ApiVersionsResponse):
    SCHEMA = Schema(
        ('error_code', Int16),
        ('api_versions', Array(
            ('api_key', Int16),
            ('min_version', Int16),
            ('max_version', Int16)))
    )

    @classmethod
    def decode(cls, data: BytesIO) -> bytes:
        if isinstance(data, bytes):
            data = BytesIO(data)
        # Check error_code, decode as v0 if any error
        curr = data.tell()
        err = Int16.decode(data)
        data.seek(curr)
        if err != 0:
            return ApiVersionsResponse_v0.decode(data)
        return super(BaseApiVersionsResponse, cls).decode(data)


@final
class ApiVersionsResponse_v0(_ApiVersionsResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('error_code', Int16),
        ('api_versions', Array(
            ('api_key', Int16),
            ('min_version', Int16),
            ('max_version', Int16)))
    )


@final
class ApiVersionsResponse_v1(BaseApiVersionsResponse):
    API_VERSION = 1
    SCHEMA = Schema(
        ('error_code', Int16),
        ('api_versions', Array(
            ('api_key', Int16),
            ('min_version', Int16),
            ('max_version', Int16))),
        ('throttle_time_ms', Int32)
    )


@final
class ApiVersionsResponse_v2(BaseApiVersionsResponse):
    API_VERSION = 2
    SCHEMA = ApiVersionsResponse_v1.SCHEMA


@final
class ApiVersionsResponse_v3(BaseApiVersionsResponse):
    API_VERSION = 3
    SCHEMA = Schema(
        ('error_code', Int16),
        ('api_versions', CompactArray(
            ('api_key', Int16),
            ('min_version', Int16),
            ('max_version', Int16),
            ('_tagged_fields', TaggedFields))),
        ('throttle_time_ms', Int32),
        ('_tagged_fields', TaggedFields)
    )
    # Note: ApiVersions Response does not send FLEXIBLE_VERSION header!


@final
class ApiVersionsResponse_v4(BaseApiVersionsResponse):
    API_VERSION = 4
    SCHEMA = ApiVersionsResponse_v3.SCHEMA


class _ApiVersionsRequestDict(TypedDict):
    client_software_name: NotRequired[str]  # added in v3
    client_software_version: NotRequired[str]  # added in v3


_ApiVersionsResponseType = TypeVar('_ApiVersionsResponseType', bound=_ApiVersionsResponse)


class _ApiVersionsRequest(Request[_ApiVersionsResponseType, _ApiVersionsRequestDict]):
    API_KEY = 18

    client_software_name: str  # added in v3
    client_software_version: str  # added in v3


@final
class ApiVersionsRequest_v0(_ApiVersionsRequest[ApiVersionsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = ApiVersionsResponse_v0
    SCHEMA = Schema()


@final
class ApiVersionsRequest_v1(_ApiVersionsRequest[ApiVersionsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = ApiVersionsResponse_v1
    SCHEMA = ApiVersionsRequest_v0.SCHEMA


@final
class ApiVersionsRequest_v2(_ApiVersionsRequest[ApiVersionsResponse_v2]):
    API_VERSION = 2
    RESPONSE_TYPE = ApiVersionsResponse_v2
    SCHEMA = ApiVersionsRequest_v1.SCHEMA


@final
class ApiVersionsRequest_v3(_ApiVersionsRequest[ApiVersionsResponse_v3]):
    API_VERSION = 3
    RESPONSE_TYPE = ApiVersionsResponse_v3
    SCHEMA = Schema(
        ('client_software_name', CompactString('utf-8')),
        ('client_software_version', CompactString('utf-8')),
        ('_tagged_fields', TaggedFields)
    )
    FLEXIBLE_VERSION = True


@final
class ApiVersionsRequest_v4(_ApiVersionsRequest[ApiVersionsResponse_v4]):
    API_VERSION = 4
    RESPONSE_TYPE = ApiVersionsResponse_v4
    SCHEMA = ApiVersionsRequest_v3.SCHEMA
    FLEXIBLE_VERSION = True


ApiVersionsRequest: List[Type[_ApiVersionsRequest]] = [
    ApiVersionsRequest_v0, ApiVersionsRequest_v1, ApiVersionsRequest_v2,
    ApiVersionsRequest_v3, ApiVersionsRequest_v4,
]
ApiVersionsResponse: List[Type[_ApiVersionsResponse]] = [
    ApiVersionsResponse_v0, ApiVersionsResponse_v1, ApiVersionsResponse_v2,
    ApiVersionsResponse_v3, ApiVersionsResponse_v4,
]
