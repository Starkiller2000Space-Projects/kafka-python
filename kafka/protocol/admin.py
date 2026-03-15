from abc import ABC
from enum import IntEnum
from typing import List, Literal, Tuple, Type, TypedDict, TypeVar, final

from kafka.protocol.api import Request, Response
from kafka.protocol.types import (Array, BitField, Boolean, Bytes, CompactArray, CompactString, Float64, Int8, Int16,
                                  Int32, Int64, Schema, String, TaggedFields)


class _CreateTopicsResponse(Response):
    API_KEY = 19


@final
class CreateTopicsResponse_v0(_CreateTopicsResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('topic_errors', Array(
            ('topic', String('utf-8')),
            ('error_code', Int16)))
    )


@final
class CreateTopicsResponse_v1(_CreateTopicsResponse):
    API_VERSION = 1
    SCHEMA = Schema(
        ('topic_errors', Array(
            ('topic', String('utf-8')),
            ('error_code', Int16),
            ('error_message', String('utf-8'))))
    )


@final
class CreateTopicsResponse_v2(_CreateTopicsResponse):
    API_VERSION = 2
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('topic_errors', Array(
            ('topic', String('utf-8')),
            ('error_code', Int16),
            ('error_message', String('utf-8'))))
    )


@final
class CreateTopicsResponse_v3(_CreateTopicsResponse):
    API_VERSION = 3
    SCHEMA = CreateTopicsResponse_v2.SCHEMA


_CreateTopicsResponseType = TypeVar('_CreateTopicsResponseType', bound=_CreateTopicsResponse)


class _CreateTopicsRequest(Request[_CreateTopicsResponseType]):
    API_KEY = 19


@final
class CreateTopicsRequest_v0(_CreateTopicsRequest[CreateTopicsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = CreateTopicsResponse_v0
    SCHEMA = Schema(
        ('create_topic_requests', Array(
            ('topic', String('utf-8')),
            ('num_partitions', Int32),
            ('replication_factor', Int16),
            ('replica_assignment', Array(
                ('partition_id', Int32),
                ('replicas', Array(Int32)))),
            ('configs', Array(
                ('config_key', String('utf-8')),
                ('config_value', String('utf-8')))))),
        ('timeout', Int32)
    )


@final
class CreateTopicsRequest_v1(_CreateTopicsRequest[CreateTopicsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = CreateTopicsResponse_v1
    SCHEMA = Schema(
        ('create_topic_requests', Array(
            ('topic', String('utf-8')),
            ('num_partitions', Int32),
            ('replication_factor', Int16),
            ('replica_assignment', Array(
                ('partition_id', Int32),
                ('replicas', Array(Int32)))),
            ('configs', Array(
                ('config_key', String('utf-8')),
                ('config_value', String('utf-8')))))),
        ('timeout', Int32),
        ('validate_only', Boolean)
    )


@final
class CreateTopicsRequest_v2(_CreateTopicsRequest[CreateTopicsResponse_v2]):
    API_VERSION = 2
    RESPONSE_TYPE = CreateTopicsResponse_v2
    SCHEMA = CreateTopicsRequest_v1.SCHEMA


@final
class CreateTopicsRequest_v3(_CreateTopicsRequest[CreateTopicsResponse_v3]):
    API_VERSION = 3
    RESPONSE_TYPE = CreateTopicsResponse_v3
    SCHEMA = CreateTopicsRequest_v1.SCHEMA


CreateTopicsRequest: List[Type[_CreateTopicsRequest]] = [
    CreateTopicsRequest_v0, CreateTopicsRequest_v1,
    CreateTopicsRequest_v2, CreateTopicsRequest_v3,
]
CreateTopicsResponse: List[Type[_CreateTopicsResponse]] = [
    CreateTopicsResponse_v0, CreateTopicsResponse_v1,
    CreateTopicsResponse_v2, CreateTopicsResponse_v3,
]


class _DeleteTopicsResponse(Response):
    API_KEY = 20


@final
class DeleteTopicsResponse_v0(_DeleteTopicsResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('topic_error_codes', Array(
            ('topic', String('utf-8')),
            ('error_code', Int16)))
    )


@final
class DeleteTopicsResponse_v1(_DeleteTopicsResponse):
    API_VERSION = 1
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('topic_error_codes', Array(
            ('topic', String('utf-8')),
            ('error_code', Int16)))
    )


@final
class DeleteTopicsResponse_v2(_DeleteTopicsResponse):
    API_VERSION = 2
    SCHEMA = DeleteTopicsResponse_v1.SCHEMA


@final
class DeleteTopicsResponse_v3(_DeleteTopicsResponse):
    API_VERSION = 3
    SCHEMA = DeleteTopicsResponse_v1.SCHEMA


_DeleteTopicsResponseType = TypeVar('_DeleteTopicsResponseType', bound=_DeleteTopicsResponse)


class _DeleteTopicsRequest(Request[_DeleteTopicsResponseType]):
    API_KEY = 20
    SCHEMA = Schema(
        ('topics', Array(String('utf-8'))),
        ('timeout', Int32)
    )

    topics: List[str]
    timeout: int


@final
class DeleteTopicsRequest_v0(_DeleteTopicsRequest[DeleteTopicsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = DeleteTopicsResponse_v0


@final
class DeleteTopicsRequest_v1(_DeleteTopicsRequest[DeleteTopicsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = DeleteTopicsResponse_v1
    SCHEMA = DeleteTopicsRequest_v0.SCHEMA


@final
class DeleteTopicsRequest_v2(_DeleteTopicsRequest[DeleteTopicsResponse_v2]):
    API_VERSION = 2
    RESPONSE_TYPE = DeleteTopicsResponse_v2
    SCHEMA = DeleteTopicsRequest_v0.SCHEMA


@final
class DeleteTopicsRequest_v3(_DeleteTopicsRequest[DeleteTopicsResponse_v3]):
    API_VERSION = 3
    RESPONSE_TYPE = DeleteTopicsResponse_v3
    SCHEMA = DeleteTopicsRequest_v0.SCHEMA


DeleteTopicsRequest: List[Type[_DeleteTopicsRequest]] = [
    DeleteTopicsRequest_v0, DeleteTopicsRequest_v1,
    DeleteTopicsRequest_v2, DeleteTopicsRequest_v3,
]
DeleteTopicsResponse: List[Type[_DeleteTopicsResponse]] = [
    DeleteTopicsResponse_v0, DeleteTopicsResponse_v1,
    DeleteTopicsResponse_v2, DeleteTopicsResponse_v3,
]


class _DeleteRecordsResponsePartition(TypedDict):
    partition_index: int
    low_watermark: int
    error_code: int


class _DeleteRecordsResponseTopic(TypedDict):
    name: str
    partitions: List[_DeleteRecordsResponsePartition]


class _DeleteRecordsResponseDict(TypedDict):

    throttle_time_ms: int
    topics: List[_DeleteRecordsResponseTopic]


@final
class DeleteRecordsResponse_v0(Response[_DeleteRecordsResponseDict]):
    API_KEY = 21
    API_VERSION = 0
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('topics', Array(
            ('name', String('utf-8')),
            ('partitions', Array(
                ('partition_index', Int32),
                ('low_watermark', Int64),
                ('error_code', Int16))))),
    )


@final
class DeleteRecordsRequest_v0(Request[DeleteRecordsResponse_v0]):
    API_KEY = 21
    API_VERSION = 0
    RESPONSE_TYPE = DeleteRecordsResponse_v0
    SCHEMA = Schema(
        ('topics', Array(
            ('name', String('utf-8')),
            ('partitions', Array(
                ('partition_index', Int32),
                ('offset', Int64))))),
        ('timeout_ms', Int32)
    )


DeleteRecordsResponse: List[Type[DeleteRecordsResponse_v0]] = [DeleteRecordsResponse_v0]
DeleteRecordsRequest: List[Type[DeleteRecordsRequest_v0]] = [DeleteRecordsRequest_v0]


class _ListGroupsResponse(Response):
    API_KEY = 16
    SCHEMA = Schema(
        ('error_code', Int16),
        ('groups', Array(
            ('group', String('utf-8')),
            ('protocol_type', String('utf-8'))))
    )

    error_code: int
    groups: List[Tuple[str, str]]


@final
class ListGroupsResponse_v0(_ListGroupsResponse):
    API_VERSION = 0


@final
class ListGroupsResponse_v1(_ListGroupsResponse):
    API_VERSION = 1
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('error_code', Int16),
        ('groups', Array(
            ('group', String('utf-8')),
            ('protocol_type', String('utf-8'))))
    )

    throttle_time_ms: int


@final
class ListGroupsResponse_v2(_ListGroupsResponse):
    API_VERSION = 2
    SCHEMA = ListGroupsResponse_v1.SCHEMA

    throttle_time_ms: int


_ListGroupResponseType = TypeVar('_ListGroupResponseType', bound=_ListGroupsResponse)


class _ListGroupsRequest(Request[_ListGroupResponseType]):
    API_KEY = 16
    SCHEMA = Schema()


@final
class ListGroupsRequest_v0(_ListGroupsRequest[ListGroupsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = ListGroupsResponse_v0


@final
class ListGroupsRequest_v1(_ListGroupsRequest[ListGroupsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = ListGroupsResponse_v1


@final
class ListGroupsRequest_v2(_ListGroupsRequest[ListGroupsResponse_v2]):
    API_VERSION = 1
    RESPONSE_TYPE = ListGroupsResponse_v2


ListGroupsRequest: List[Type[_ListGroupsRequest]] = [
    ListGroupsRequest_v0, ListGroupsRequest_v1,
    ListGroupsRequest_v2,
]
ListGroupsResponse: List[Type[_ListGroupsResponse]] = [
    ListGroupsResponse_v0, ListGroupsResponse_v1,
    ListGroupsResponse_v2,
]


class _DescribeGroupsResponse(Response, ABC):
    API_KEY = 15

    groups: List[Tuple]


@final
class DescribeGroupsResponse_v0(_DescribeGroupsResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('groups', Array(
            ('error_code', Int16),
            ('group', String('utf-8')),
            ('state', String('utf-8')),
            ('protocol_type', String('utf-8')),
            ('protocol', String('utf-8')),
            ('members', Array(
                ('member_id', String('utf-8')),
                ('client_id', String('utf-8')),
                ('client_host', String('utf-8')),
                ('member_metadata', Bytes),
                ('member_assignment', Bytes)))))
    )

    groups: List[Tuple[int, str, str, str, str, List[Tuple[str, str, str, bytes, bytes]]]]


@final
class DescribeGroupsResponse_v1(_DescribeGroupsResponse):
    API_VERSION = 1
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('groups', Array(
            ('error_code', Int16),
            ('group', String('utf-8')),
            ('state', String('utf-8')),
            ('protocol_type', String('utf-8')),
            ('protocol', String('utf-8')),
            ('members', Array(
                ('member_id', String('utf-8')),
                ('client_id', String('utf-8')),
                ('client_host', String('utf-8')),
                ('member_metadata', Bytes),
                ('member_assignment', Bytes)))))
    )

    throttle_time_ms: int
    groups: List[Tuple[int, str, str, str, str, List[Tuple[str, str, str, bytes, bytes]]]]


@final
class DescribeGroupsResponse_v2(_DescribeGroupsResponse):
    API_VERSION = 2
    SCHEMA = DescribeGroupsResponse_v1.SCHEMA

    throttle_time_ms: int
    groups: List[Tuple[int, str, str, str, str, List[Tuple[str, str, str, bytes, bytes]]]]


@final
class DescribeGroupsResponse_v3(_DescribeGroupsResponse):
    API_VERSION = 3
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('groups', Array(
            ('error_code', Int16),
            ('group', String('utf-8')),
            ('state', String('utf-8')),
            ('protocol_type', String('utf-8')),
            ('protocol', String('utf-8')),
            ('members', Array(
                ('member_id', String('utf-8')),
                ('client_id', String('utf-8')),
                ('client_host', String('utf-8')),
                ('member_metadata', Bytes),
                ('member_assignment', Bytes))),
            ('authorized_operations', BitField)))
    )

    throttle_time_ms: int
    groups: List[Tuple[int, str, str, str, str, List[Tuple[str, str, str, bytes, bytes]], Set[int]]]


_DescribeGroupsResponseType = TypeVar('_DescribeGroupsResponseType', bound=_DescribeGroupsResponse)


class _DescribeGroupsRequest(Request[_DescribeGroupsResponseType], ABC):
    API_KEY = 15
    SCHEMA = Schema(
        ('groups', Array(String('utf-8')))
    )

    groups: List[str]


@final
class DescribeGroupsRequest_v0(_DescribeGroupsRequest[DescribeGroupsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = DescribeGroupsResponse_v0


@final
class DescribeGroupsRequest_v1(_DescribeGroupsRequest[DescribeGroupsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = DescribeGroupsResponse_v1
    SCHEMA = DescribeGroupsRequest_v0.SCHEMA


@final
class DescribeGroupsRequest_v2(_DescribeGroupsRequest[DescribeGroupsResponse_v2]):
    API_VERSION = 2
    RESPONSE_TYPE = DescribeGroupsResponse_v2
    SCHEMA = DescribeGroupsRequest_v0.SCHEMA


@final
class DescribeGroupsRequest_v3(_DescribeGroupsRequest[DescribeGroupsResponse_v3]):
    API_VERSION = 3
    RESPONSE_TYPE = DescribeGroupsResponse_v3
    SCHEMA = Schema(
        ('groups', Array(String('utf-8'))),
        ('include_authorized_operations', Boolean)
    )

    include_authorized_operations: bool


DescribeGroupsRequest: List[Type[_DescribeGroupsRequest]] = [
    DescribeGroupsRequest_v0, DescribeGroupsRequest_v1,
    DescribeGroupsRequest_v2, DescribeGroupsRequest_v3,
]
DescribeGroupsResponse: List[Type[_DescribeGroupsResponse]] = [
    DescribeGroupsResponse_v0, DescribeGroupsResponse_v1,
    DescribeGroupsResponse_v2, DescribeGroupsResponse_v3,
]


class _DescribeAclsResponse(Response):
    API_KEY = 29

    error_code: int
    resources: List[Tuple]

@final
class DescribeAclsResponse_v0(_DescribeAclsResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('error_code', Int16),
        ('error_message', String('utf-8')),
        ('resources', Array(
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('acls', Array(
                ('principal', String('utf-8')),
                ('host', String('utf-8')),
                ('operation', Int8),
                ('permission_type', Int8)))))
    )

    resources: List[Tuple[int, str, List[Tuple[str, str, int, int]]]]


@final
class DescribeAclsResponse_v1(_DescribeAclsResponse):
    API_VERSION = 1
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('error_code', Int16),
        ('error_message', String('utf-8')),
        ('resources', Array(
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('resource_pattern_type', Int8),
            ('acls', Array(
                ('principal', String('utf-8')),
                ('host', String('utf-8')),
                ('operation', Int8),
                ('permission_type', Int8)))))
    )

    resources: List[Tuple[int, str, int, List[Tuple[str, str, int, int]]]]


@final
class DescribeAclsResponse_v2(_DescribeAclsResponse):
    API_VERSION = 2
    SCHEMA = DescribeAclsResponse_v1.SCHEMA


_DescribeAclsResponseType = TypeVar('_DescribeAclsResponseType', bound=_DescribeAclsResponse)


class _DescribeAclsRequest(Request[_DescribeAclsResponseType], ABC):
    API_KEY = 29


@final
class DescribeAclsRequest_v0(_DescribeAclsRequest[DescribeAclsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = DescribeAclsResponse_v0
    SCHEMA = Schema(
        ('resource_type', Int8),
        ('resource_name', String('utf-8')),
        ('principal', String('utf-8')),
        ('host', String('utf-8')),
        ('operation', Int8),
        ('permission_type', Int8)
    )


@final
class DescribeAclsRequest_v1(_DescribeAclsRequest[DescribeAclsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = DescribeAclsResponse_v1
    SCHEMA = Schema(
        ('resource_type', Int8),
        ('resource_name', String('utf-8')),
        ('resource_pattern_type_filter', Int8),
        ('principal', String('utf-8')),
        ('host', String('utf-8')),
        ('operation', Int8),
        ('permission_type', Int8)
    )


@final
class DescribeAclsRequest_v2(_DescribeAclsRequest[DescribeAclsResponse_v2]):
    """
    Enable flexible version
    """
    API_VERSION = 2
    RESPONSE_TYPE = DescribeAclsResponse_v2
    SCHEMA = DescribeAclsRequest_v1.SCHEMA


DescribeAclsRequest: List[Type[_DescribeAclsRequest]] = [DescribeAclsRequest_v0, DescribeAclsRequest_v1, DescribeAclsRequest_v2]
DescribeAclsResponse: List[Type[_DescribeAclsResponse]] = [DescribeAclsResponse_v0, DescribeAclsResponse_v1, DescribeAclsResponse_v2]


class _CreateAclResponse(Response, ABC):
    API_KEY = 30
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('creation_responses', Array(
            ('error_code', Int16),
            ('error_message', String('utf-8'))))
    )

    throttle_time_ms: int
    creation_responses: List[Tuple[int, str]]


@final
class CreateAclsResponse_v0(_CreateAclResponse):
    API_VERSION = 0


@final
class CreateAclsResponse_v1(_CreateAclResponse):
    API_VERSION = 1


_CreateAclResponseType = TypeVar('_CreateAclResponseType', bound=_CreateAclResponse)


class _CreateAclRequest(Request[_CreateAclResponseType], ABC):
    API_KEY = 30


@final
class CreateAclsRequest_v0(_CreateAclRequest[CreateAclsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = CreateAclsResponse_v0
    SCHEMA = Schema(
        ('creations', Array(
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('principal', String('utf-8')),
            ('host', String('utf-8')),
            ('operation', Int8),
            ('permission_type', Int8)))
    )


@final
class CreateAclsRequest_v1(_CreateAclRequest[CreateAclsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = CreateAclsResponse_v1
    SCHEMA = Schema(
        ('creations', Array(
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('resource_pattern_type', Int8),
            ('principal', String('utf-8')),
            ('host', String('utf-8')),
            ('operation', Int8),
            ('permission_type', Int8)))
    )


CreateAclsRequest: List[Type[_CreateAclRequest]] = [CreateAclsRequest_v0, CreateAclsRequest_v1]
CreateAclsResponse: List[Type[_CreateAclResponse]] = [CreateAclsResponse_v0, CreateAclsResponse_v1]


class _DeleteAclsResponse(Response):
    API_KEY = 31

    throttle_time_ms: int
    filter_responses: List[Tuple[int, str, List[Tuple]]]

@final
class DeleteAclsResponse_v0(_DeleteAclsResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('filter_responses', Array(
            ('error_code', Int16),
            ('error_message', String('utf-8')),
            ('matching_acls', Array(
                ('error_code', Int16),
                ('error_message', String('utf-8')),
                ('resource_type', Int8),
                ('resource_name', String('utf-8')),
                ('principal', String('utf-8')),
                ('host', String('utf-8')),
                ('operation', Int8),
                ('permission_type', Int8)))))
    )

    filter_responses: List[Tuple[int, str, List[Tuple[int, str, int, str, str, str, int, int]]]]


@final
class DeleteAclsResponse_v1(_DeleteAclsResponse):
    API_VERSION = 1
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('filter_responses', Array(
            ('error_code', Int16),
            ('error_message', String('utf-8')),
            ('matching_acls', Array(
                ('error_code', Int16),
                ('error_message', String('utf-8')),
                ('resource_type', Int8),
                ('resource_name', String('utf-8')),
                ('resource_pattern_type', Int8),
                ('principal', String('utf-8')),
                ('host', String('utf-8')),
                ('operation', Int8),
                ('permission_type', Int8)))))
    )

    filter_responses: List[Tuple[int, str, List[Tuple[int, str, int, str, int, str, str, int, int]]]]


_DeleteAclsResponseType = TypeVar('_DeleteAclsResponseType', bound=_DeleteAclsResponse)


class _DeleteAclsRequest(Request[_DeleteAclsResponseType]):
    API_KEY = 31


@final
class DeleteAclsRequest_v0(_DeleteAclsRequest[DeleteAclsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = DeleteAclsResponse_v0
    SCHEMA = Schema(
        ('filters', Array(
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('principal', String('utf-8')),
            ('host', String('utf-8')),
            ('operation', Int8),
            ('permission_type', Int8)))
    )


@final
class DeleteAclsRequest_v1(_DeleteAclsRequest[DeleteAclsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = DeleteAclsResponse_v1
    SCHEMA = Schema(
        ('filters', Array(
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('resource_pattern_type_filter', Int8),
            ('principal', String('utf-8')),
            ('host', String('utf-8')),
            ('operation', Int8),
            ('permission_type', Int8)))
    )


DeleteAclsRequest: List[Type[_DeleteAclsRequest]] = [DeleteAclsRequest_v0, DeleteAclsRequest_v1]
DeleteAclsResponse: List[Type[_DeleteAclsResponse]] = [DeleteAclsResponse_v0, DeleteAclsResponse_v1]


class AlterConfigsResponse_v0(Response):
    API_KEY = 33
    API_VERSION = 0
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('resources', Array(
            ('error_code', Int16),
            ('error_message', String('utf-8')),
            ('resource_type', Int8),
            ('resource_name', String('utf-8'))))
    )


class AlterConfigsResponse_v1(Response):
    API_KEY = 33
    API_VERSION = 1
    SCHEMA = AlterConfigsResponse_v0.SCHEMA


class AlterConfigsRequest_v0(Request):
    API_KEY = 33
    API_VERSION = 0
    RESPONSE_TYPE = AlterConfigsResponse_v0
    SCHEMA = Schema(
        ('resources', Array(
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('config_entries', Array(
                ('config_name', String('utf-8')),
                ('config_value', String('utf-8')))))),
        ('validate_only', Boolean)
    )

class AlterConfigsRequest_v1(Request):
    API_KEY = 33
    API_VERSION = 1
    RESPONSE_TYPE = AlterConfigsResponse_v1
    SCHEMA = AlterConfigsRequest_v0.SCHEMA

AlterConfigsRequest = [AlterConfigsRequest_v0, AlterConfigsRequest_v1]
AlterConfigsResponse = [AlterConfigsResponse_v0, AlterConfigsRequest_v1]


class _DescribeConfigsResponse(Response):
    API_KEY = 32


@final
class DescribeConfigsResponse_v0(_DescribeConfigsResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('resources', Array(
            ('error_code', Int16),
            ('error_message', String('utf-8')),
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('config_entries', Array(
                ('config_names', String('utf-8')),
                ('config_value', String('utf-8')),
                ('read_only', Boolean),
                ('is_default', Boolean),
                ('is_sensitive', Boolean)))))
    )


class DescribeConfigsResponse_v1(_DescribeConfigsResponse):
    API_VERSION = 1
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('resources', Array(
            ('error_code', Int16),
            ('error_message', String('utf-8')),
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('config_entries', Array(
                ('config_names', String('utf-8')),
                ('config_value', String('utf-8')),
                ('read_only', Boolean),
                ('config_source', Int8),
                ('is_sensitive', Boolean),
                ('config_synonyms', Array(
                    ('config_name', String('utf-8')),
                    ('config_value', String('utf-8')),
                    ('config_source', Int8)))))))
    )


class DescribeConfigsResponse_v2(_DescribeConfigsResponse):
    API_VERSION = 2
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('resources', Array(
            ('error_code', Int16),
            ('error_message', String('utf-8')),
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('config_entries', Array(
                ('config_names', String('utf-8')),
                ('config_value', String('utf-8')),
                ('read_only', Boolean),
                ('config_source', Int8),
                ('is_sensitive', Boolean),
                ('config_synonyms', Array(
                    ('config_name', String('utf-8')),
                    ('config_value', String('utf-8')),
                    ('config_source', Int8)))))))
    )

_DescribeConfigsResponseType = TypeVar('_DescribeConfigsResponseType', bound=_DescribeConfigsResponse)


class _DescribeConfigsRequest(Request[_DescribeConfigsResponseType], ABC):
    API_KEY = 32


@final
class DescribeConfigsRequest_v0(_DescribeConfigsRequest[DescribeConfigsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = DescribeConfigsResponse_v0
    SCHEMA = Schema(
        ('resources', Array(
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('config_names', Array(String('utf-8')))))
    )


@final
class DescribeConfigsRequest_v1(_DescribeConfigsRequest[DescribeConfigsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = DescribeConfigsResponse_v1
    SCHEMA = Schema(
        ('resources', Array(
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('config_names', Array(String('utf-8'))))),
        ('include_synonyms', Boolean)
    )


@final
class DescribeConfigsRequest_v2(_DescribeConfigsRequest[DescribeConfigsResponse_v2]):
    API_VERSION = 2
    RESPONSE_TYPE = DescribeConfigsResponse_v2
    SCHEMA = DescribeConfigsRequest_v1.SCHEMA


DescribeConfigsRequest: List[Type[_DescribeConfigsRequest]] = [
    DescribeConfigsRequest_v0, DescribeConfigsRequest_v1,
    DescribeConfigsRequest_v2,
]
DescribeConfigsResponse: List[Type[_DescribeConfigsResponse]] = [
    DescribeConfigsResponse_v0, DescribeConfigsResponse_v1,
    DescribeConfigsResponse_v2,
]


class DescribeLogDirsResponse_v0(Response):
    API_KEY = 35
    API_VERSION = 0
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('log_dirs', Array(
            ('error_code', Int16),
            ('log_dir', String('utf-8')),
            ('topics', Array(
                ('name', String('utf-8')),
                ('partitions', Array(
                    ('partition_index', Int32),
                    ('partition_size', Int64),
                    ('offset_lag', Int64),
                    ('is_future_key', Boolean)
                ))
            ))
        ))
    )


class DescribeLogDirsRequest_v0(Request):
    API_KEY = 35
    API_VERSION = 0
    RESPONSE_TYPE = DescribeLogDirsResponse_v0
    SCHEMA = Schema(
                     ('topics', Array(
                         ('topic', String('utf-8')),
                         ('partitions', Int32)
                         ))
                 )


DescribeLogDirsResponse = [
    DescribeLogDirsResponse_v0,
]
DescribeLogDirsRequest = [
    DescribeLogDirsRequest_v0,
]


class SaslAuthenticateResponse_v0(Response):
    API_KEY = 36
    API_VERSION = 0
    SCHEMA = Schema(
        ('error_code', Int16),
        ('error_message', String('utf-8')),
        ('sasl_auth_bytes', Bytes)
    )


class SaslAuthenticateResponse_v1(Response):
    API_KEY = 36
    API_VERSION = 1
    SCHEMA = Schema(
        ('error_code', Int16),
        ('error_message', String('utf-8')),
        ('sasl_auth_bytes', Bytes),
        ('session_lifetime_ms', Int64)
    )


class SaslAuthenticateRequest_v0(Request):
    API_KEY = 36
    API_VERSION = 0
    RESPONSE_TYPE = SaslAuthenticateResponse_v0
    SCHEMA = Schema(
        ('sasl_auth_bytes', Bytes)
    )


class SaslAuthenticateRequest_v1(Request):
    API_KEY = 36
    API_VERSION = 1
    RESPONSE_TYPE = SaslAuthenticateResponse_v1
    SCHEMA = SaslAuthenticateRequest_v0.SCHEMA


SaslAuthenticateRequest = [
    SaslAuthenticateRequest_v0, SaslAuthenticateRequest_v1,
]
SaslAuthenticateResponse = [
    SaslAuthenticateResponse_v0, SaslAuthenticateResponse_v1,
]


class CreatePartitionsResponse_v0(Response):
    API_KEY = 37
    API_VERSION = 0
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('topic_errors', Array(
            ('topic', String('utf-8')),
            ('error_code', Int16),
            ('error_message', String('utf-8'))))
    )


class CreatePartitionsResponse_v1(Response):
    API_KEY = 37
    API_VERSION = 1
    SCHEMA = CreatePartitionsResponse_v0.SCHEMA


class CreatePartitionsRequest_v0(Request):
    API_KEY = 37
    API_VERSION = 0
    RESPONSE_TYPE = CreatePartitionsResponse_v0
    SCHEMA = Schema(
        ('topic_partitions', Array(
            ('topic', String('utf-8')),
            ('new_partitions', Schema(
                ('count', Int32),
                ('assignment', Array(Array(Int32))))))),
        ('timeout', Int32),
        ('validate_only', Boolean)
    )


class CreatePartitionsRequest_v1(Request):
    API_KEY = 37
    API_VERSION = 1
    SCHEMA = CreatePartitionsRequest_v0.SCHEMA
    RESPONSE_TYPE = CreatePartitionsResponse_v1


CreatePartitionsRequest = [
    CreatePartitionsRequest_v0, CreatePartitionsRequest_v1,
]
CreatePartitionsResponse = [
    CreatePartitionsResponse_v0, CreatePartitionsResponse_v1,
]


class _DeleteGroupsResponse(Response, ABC):

    SCHEMA = Schema(
        ("throttle_time_ms", Int32),
        ("results", Array(
            ("group_id", String("utf-8")),
            ("error_code", Int16)))
    )

    throttle_time_ms: int
    results: List[Tuple[str, int]]


class DeleteGroupsResponse_v0(_DeleteGroupsResponse):
    API_KEY = 42
    API_VERSION = 0


class DeleteGroupsResponse_v1(_DeleteGroupsResponse):
    API_KEY = 42
    API_VERSION = 1


_DeleteGroupsResponseType = TypeVar('_DeleteGroupsResponseType', bound=_DeleteGroupsResponse)


class _DeleteGroupsRequest(Request[_DeleteGroupsResponseType], ABC):
    SCHEMA = Schema(
        ("groups_names", Array(String("utf-8")))
    )

    groups_names: List[str]

class DeleteGroupsRequest_v0(_DeleteGroupsRequest[DeleteGroupsResponse_v0]):
    API_KEY = 42
    API_VERSION = 0
    RESPONSE_TYPE = DeleteGroupsResponse_v0


class DeleteGroupsRequest_v1(_DeleteGroupsRequest[DeleteGroupsResponse_v1]):
    API_KEY = 42
    API_VERSION = 1
    RESPONSE_TYPE = DeleteGroupsResponse_v1


DeleteGroupsRequest: List[Type[_DeleteGroupsRequest]] = [
    DeleteGroupsRequest_v0, DeleteGroupsRequest_v1
]

DeleteGroupsResponse: List[Type[_DeleteGroupsResponse]] = [
    DeleteGroupsResponse_v0, DeleteGroupsResponse_v1
]


class DescribeClientQuotasResponse_v0(Response):
    API_KEY = 48
    API_VERSION = 0
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('error_code', Int16),
        ('error_message', String('utf-8')),
        ('entries', Array(
            ('entity', Array(
                ('entity_type', String('utf-8')),
                ('entity_name', String('utf-8')))),
            ('values', Array(
                ('name', String('utf-8')),
                ('value', Float64))))),
    )


class DescribeClientQuotasRequest_v0(Request):
    API_KEY = 48
    API_VERSION = 0
    RESPONSE_TYPE = DescribeClientQuotasResponse_v0
    SCHEMA = Schema(
        ('components', Array(
            ('entity_type', String('utf-8')),
            ('match_type', Int8),
            ('match', String('utf-8')),
        )),
        ('strict', Boolean)
    )


DescribeClientQuotasRequest = [
    DescribeClientQuotasRequest_v0,
]

DescribeClientQuotasResponse = [
    DescribeClientQuotasResponse_v0,
]


class AlterPartitionReassignmentsResponse_v0(Response):
    API_KEY = 45
    API_VERSION = 0
    SCHEMA = Schema(
        ("throttle_time_ms", Int32),
        ("error_code", Int16),
        ("error_message", CompactString("utf-8")),
        ("responses", CompactArray(
            ("name", CompactString("utf-8")),
            ("partitions", CompactArray(
                ("partition_index", Int32),
                ("error_code", Int16),
                ("error_message", CompactString("utf-8")),
                ("tags", TaggedFields)
            )),
            ("tags", TaggedFields)
        )),
        ("tags", TaggedFields)
    )
    FLEXIBLE_VERSION = True


class AlterPartitionReassignmentsRequest_v0(Request):
    FLEXIBLE_VERSION = True
    API_KEY = 45
    API_VERSION = 0
    RESPONSE_TYPE = AlterPartitionReassignmentsResponse_v0
    SCHEMA = Schema(
        ("timeout_ms", Int32),
        ("topics", CompactArray(
            ("name", CompactString("utf-8")),
            ("partitions", CompactArray(
                ("partition_index", Int32),
                ("replicas", CompactArray(Int32)),
                ("tags", TaggedFields)
            )),
            ("tags", TaggedFields)
        )),
        ("tags", TaggedFields)
    )


AlterPartitionReassignmentsRequest = [AlterPartitionReassignmentsRequest_v0]

AlterPartitionReassignmentsResponse = [AlterPartitionReassignmentsResponse_v0]


class ListPartitionReassignmentsResponse_v0(Response):
    API_KEY = 46
    API_VERSION = 0
    SCHEMA = Schema(
        ("throttle_time_ms", Int32),
        ("error_code", Int16),
        ("error_message", CompactString("utf-8")),
        ("topics", CompactArray(
            ("name", CompactString("utf-8")),
            ("partitions", CompactArray(
                ("partition_index", Int32),
                ("replicas", CompactArray(Int32)),
                ("adding_replicas", CompactArray(Int32)),
                ("removing_replicas", CompactArray(Int32)),
                ("tags", TaggedFields)
            )),
            ("tags", TaggedFields)
        )),
        ("tags", TaggedFields)
    )
    FLEXIBLE_VERSION = True


class ListPartitionReassignmentsRequest_v0(Request):
    FLEXIBLE_VERSION = True
    API_KEY = 46
    API_VERSION = 0
    RESPONSE_TYPE = ListPartitionReassignmentsResponse_v0
    SCHEMA = Schema(
        ("timeout_ms", Int32),
        ("topics", CompactArray(
            ("name", CompactString("utf-8")),
            ("partition_index", CompactArray(Int32)),
            ("tags", TaggedFields)
        )),
        ("tags", TaggedFields)
    )


ListPartitionReassignmentsRequest = [ListPartitionReassignmentsRequest_v0]

ListPartitionReassignmentsResponse = [ListPartitionReassignmentsResponse_v0]


class _ElectLeadersResponse(Response):
    API_KEY = 43
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('error_code', Int16),
        ('replication_election_results', Array(
            ('topic', String('utf-8')),
            ('partition_result', Array(
                ('partition_id', Int32),
                ('error_code', Int16),
                ('error_message', String('utf-8'))
            ))
        ))
    )

    throttle_time_ms: int
    error_code: int
    replication_election_results: List[Tuple[str, List[Tuple[int, int, str]]]]


@final
class ElectLeadersResponse_v0(_ElectLeadersResponse):
    API_VERSION = 1


_ElectLeadersResponseType = TypeVar('_ElectLeadersResponseType', bound=_ElectLeadersResponse)


class _ElectLeadersRequest(Request[_ElectLeadersResponseType]):
    API_KEY = 43
    SCHEMA = Schema(
        ('election_type', Int8),
        ('topic_partitions', Array(
            ('topic', String('utf-8')),
            ('partition_ids', Array(Int32))
        )),
        ('timeout', Int32),
    )

    election_type: int
    topic_partitions: List[Tuple[str, List[int]]]
    timeout: int


@final
class ElectLeadersRequest_v0(_ElectLeadersRequest[ElectLeadersResponse_v0]):
    API_VERSION = 1
    RESPONSE_TYPE = ElectLeadersResponse_v0


class ElectLeadersResponse_v1(_ElectLeadersResponse):
    API_VERSION = 1


class ElectLeadersRequest_v1(_ElectLeadersRequest[ElectLeadersResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = ElectLeadersResponse_v1


class ElectionType(IntEnum):
    """ Leader election type
    """

    PREFERRED = 0,
    UNCLEAN = 1


ElectLeadersRequest: List[Type[_ElectLeadersRequest]] = [ElectLeadersRequest_v0, ElectLeadersRequest_v1]
ElectLeadersResponse: List[Type[_ElectLeadersResponse]] = [ElectLeadersResponse_v0, ElectLeadersResponse_v1]
