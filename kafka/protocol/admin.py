from abc import ABC
from enum import IntEnum
from typing import List, Set, Tuple, Type, TypedDict, TypeVar, Union, final

from typing_extensions import NotRequired

from kafka.protocol.api import Request, Response
from kafka.protocol.types import (Array, BitField, Boolean, Bytes, CompactArray, CompactString, Float64, Int8, Int16,
                                  Int32, Int64, Schema, String, TaggedFields)


class _CreateTopicsResponseTopicErrorDict(TypedDict):
    topic: str
    error_code: int
    error_message: NotRequired[str]  # added in v1


class _CreateTopicsResponseDict(TypedDict):
    topic_errors: List[_CreateTopicsResponseTopicErrorDict]
    throttle_time_ms: NotRequired[int]  # added in v2


class _CreateTopicsResponse(Response[_CreateTopicsResponseDict]):
    API_KEY = 19

    topic_errors: List[Union[
        Tuple[str, int],
        Tuple[str, int, str],  # api version >=1
    ]]
    throttle_time_ms: int  # added in v2


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


class _CreateTopicsRequestConfigDict(TypedDict):
    config_key: str
    config_value: str


class _CreateTopicsRequestReplicaAssignmentDict(TypedDict):
    partition_id: int
    replicas: List[int]


class _CreateTopicsRequestItemDict(TypedDict):
    topic: str
    num_partitions: int
    replication_factor: int
    replica_assignment: List[_CreateTopicsRequestReplicaAssignmentDict]
    configs: List[_CreateTopicsRequestConfigDict]


class _CreateTopicsRequestDict(TypedDict):
    create_topic_requests: List[_CreateTopicsRequestItemDict]
    timeout: int
    validate_only: NotRequired[bool]  # added in v1


_CreateTopicsResponseType = TypeVar('_CreateTopicsResponseType', bound=_CreateTopicsResponse)


class _CreateTopicsRequest(Request[_CreateTopicsResponseType, _CreateTopicsRequestDict]):
    API_KEY = 19

    create_topic_requests: List[Union[
        Tuple[str, int, int, List[Tuple[int, List[int]]], List[Tuple[str, str]]]
    ]]
    timeout: int
    validate_only: bool  # added in v1


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


class _DeleteTopicsResponseTopicErrorDict(TypedDict):
    topic: str
    error_code: int


class _DeleteTopicsResponseDict(TypedDict):
    topic_error_codes: List[_DeleteTopicsResponseTopicErrorDict]
    throttle_time_ms: NotRequired[int]  # added in v1


class _DeleteTopicsResponse(Response[_DeleteTopicsResponseDict]):
    API_KEY = 20

    topic_error_codes: List[Tuple[str, int]]
    throttle_time_ms: int  # added in v1


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


class _DeleteTopicsRequestDict(TypedDict):
    topics: List[str]
    timeout: int


_DeleteTopicsResponseType = TypeVar('_DeleteTopicsResponseType', bound=_DeleteTopicsResponse)


class _DeleteTopicsRequest(Request[_DeleteTopicsResponseType, _DeleteTopicsRequestDict]):
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


@final
class DeleteTopicsRequest_v2(_DeleteTopicsRequest[DeleteTopicsResponse_v2]):
    API_VERSION = 2
    RESPONSE_TYPE = DeleteTopicsResponse_v2


@final
class DeleteTopicsRequest_v3(_DeleteTopicsRequest[DeleteTopicsResponse_v3]):
    API_VERSION = 3
    RESPONSE_TYPE = DeleteTopicsResponse_v3


DeleteTopicsRequest: List[Type[_DeleteTopicsRequest]] = [
    DeleteTopicsRequest_v0, DeleteTopicsRequest_v1,
    DeleteTopicsRequest_v2, DeleteTopicsRequest_v3,
]
DeleteTopicsResponse: List[Type[_DeleteTopicsResponse]] = [
    DeleteTopicsResponse_v0, DeleteTopicsResponse_v1,
    DeleteTopicsResponse_v2, DeleteTopicsResponse_v3,
]


class _DeleteRecordsResponsePartitionDict(TypedDict):
    partition_index: int
    low_watermark: int
    error_code: int


class _DeleteRecordsResponseTopicDict(TypedDict):
    name: str
    partitions: List[_DeleteRecordsResponsePartitionDict]


class _DeleteRecordsResponseDict(TypedDict):
    throttle_time_ms: int
    topics: List[_DeleteRecordsResponseTopicDict]


class _DeleteRecordsResponse(Response[_DeleteRecordsResponseDict]):
    API_KEY = 21
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('topics', Array(
            ('name', String('utf-8')),
            ('partitions', Array(
                ('partition_index', Int32),
                ('low_watermark', Int64),
                ('error_code', Int16))))),
    )

    throttle_time_ms: int
    topics: List[Tuple[str, List[Tuple[int, int, int]]]]


@final
class DeleteRecordsResponse_v0(_DeleteRecordsResponse):
    API_VERSION = 0


class _DeleteRecordsRequestPartitionDict(TypedDict):
    partition_index: int
    offset: int


class _DeleteRecordsRequestTopicDict(TypedDict):
    name: str
    partitions: List[_DeleteRecordsRequestPartitionDict]


class _DeleteRecordsRequestDict(TypedDict):
    topics: List[_DeleteRecordsRequestTopicDict]
    timeout_ms: int


_DeleteRecordsResponseType = TypeVar('_DeleteRecordsResponseType', bound=_DeleteRecordsResponse)


class _DeleteRecordsRequest(Request[_DeleteRecordsResponseType, _DeleteRecordsRequestDict]):
    API_KEY = 21
    SCHEMA = Schema(
        ('topics', Array(
            ('name', String('utf-8')),
            ('partitions', Array(
                ('partition_index', Int32),
                ('offset', Int64))))),
        ('timeout_ms', Int32)
    )

    topics: List[Tuple[str, List[Tuple[int, int]]]]
    timeout_ms: int


@final
class DeleteRecordsRequest_v0(_DeleteRecordsRequest[DeleteRecordsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = DeleteRecordsResponse_v0


DeleteRecordsResponse: List[Type[_DeleteRecordsResponse]] = [DeleteRecordsResponse_v0]
DeleteRecordsRequest: List[Type[_DeleteRecordsRequest]] = [DeleteRecordsRequest_v0]


class _ListGroupsResponseGroupDict(TypedDict):
    group: str
    protocol_type: str


class _ListGroupsResponseDict(TypedDict):
    error_code: int
    groups: List[_ListGroupsResponseGroupDict]
    throttle_time_ms: NotRequired[int]  # added in v1


class _ListGroupsResponse(Response[_ListGroupsResponseDict]):
    API_KEY = 16

    error_code: int
    groups: List[Tuple[str, str]]
    throttle_time_ms: int  # added in v1


@final
class ListGroupsResponse_v0(_ListGroupsResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('error_code', Int16),
        ('groups', Array(
            ('group', String('utf-8')),
            ('protocol_type', String('utf-8'))))
    )


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


@final
class ListGroupsResponse_v2(_ListGroupsResponse):
    API_VERSION = 2
    SCHEMA = ListGroupsResponse_v1.SCHEMA


class _ListGroupsRequestDict(TypedDict):
    pass


_ListGroupResponseType = TypeVar('_ListGroupResponseType', bound=_ListGroupsResponse)


class _ListGroupsRequest(Request[_ListGroupResponseType, _ListGroupsRequestDict]):
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
    API_VERSION = 2
    RESPONSE_TYPE = ListGroupsResponse_v2


ListGroupsRequest: List[Type[_ListGroupsRequest]] = [
    ListGroupsRequest_v0, ListGroupsRequest_v1,
    ListGroupsRequest_v2,
]
ListGroupsResponse: List[Type[_ListGroupsResponse]] = [
    ListGroupsResponse_v0, ListGroupsResponse_v1,
    ListGroupsResponse_v2,
]


class _DescribeGroupsResponseMemberDict(TypedDict):
    member_id: str
    client_id: str
    client_host: str
    member_metadata: bytes
    member_assignment: bytes


class _DescribeGroupsResponseGroupDict(TypedDict):
    error_code: int
    group: str
    state: str
    protocol_type: str
    protocol: str
    members: List[_DescribeGroupsResponseMemberDict]
    authorized_operations: NotRequired[Set[int]]  # added in v3


class _DescribeGroupsResponseDict(TypedDict):
    throttle_time_ms: NotRequired[int]  # added in v1
    groups: List[_DescribeGroupsResponseGroupDict]


class _DescribeGroupsResponse(Response[_DescribeGroupsResponseDict]):
    API_KEY = 15

    throttle_time_ms: int  # added in v1
    groups: List[Union[
        Tuple[int, str, str, str, str, List[Tuple[str, str, str, bytes, bytes]]],  # v0-v2
        Tuple[int, str, str, str, str, List[Tuple[str, str, str, bytes, bytes]], Set[int]]  # v3
    ]]


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


@final
class DescribeGroupsResponse_v2(_DescribeGroupsResponse):
    API_VERSION = 2
    SCHEMA = DescribeGroupsResponse_v1.SCHEMA


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


class _DescribeGroupsRequestDict(TypedDict):
    groups: List[str]
    include_authorized_operations: NotRequired[bool]  # added in v3


_DescribeGroupsResponseType = TypeVar('_DescribeGroupsResponseType', bound=_DescribeGroupsResponse)


class _DescribeGroupsRequest(Request[_DescribeGroupsResponseType, _DescribeGroupsRequestDict]):
    API_KEY = 15
    SCHEMA = Schema(
        ('groups', Array(String('utf-8')))
    )

    groups: List[str]
    include_authorized_operations: bool  # added in v3


@final
class DescribeGroupsRequest_v0(_DescribeGroupsRequest[DescribeGroupsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = DescribeGroupsResponse_v0


@final
class DescribeGroupsRequest_v1(_DescribeGroupsRequest[DescribeGroupsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = DescribeGroupsResponse_v1


@final
class DescribeGroupsRequest_v2(_DescribeGroupsRequest[DescribeGroupsResponse_v2]):
    API_VERSION = 2
    RESPONSE_TYPE = DescribeGroupsResponse_v2


@final
class DescribeGroupsRequest_v3(_DescribeGroupsRequest[DescribeGroupsResponse_v3]):
    API_VERSION = 3
    RESPONSE_TYPE = DescribeGroupsResponse_v3
    SCHEMA = Schema(
        ('groups', Array(String('utf-8'))),
        ('include_authorized_operations', Boolean)
    )


DescribeGroupsRequest: List[Type[_DescribeGroupsRequest]] = [
    DescribeGroupsRequest_v0, DescribeGroupsRequest_v1,
    DescribeGroupsRequest_v2, DescribeGroupsRequest_v3,
]
DescribeGroupsResponse: List[Type[_DescribeGroupsResponse]] = [
    DescribeGroupsResponse_v0, DescribeGroupsResponse_v1,
    DescribeGroupsResponse_v2, DescribeGroupsResponse_v3,
]


class _DescribeAclsResponseAclDict(TypedDict):
    principal: str
    host: str
    operation: int
    permission_type: int


class _DescribeAclsResponseResourceV0Dict(TypedDict):
    resource_type: int
    resource_name: str
    acls: List[_DescribeAclsResponseAclDict]


class _DescribeAclsResponseResourceV1Dict(TypedDict):
    resource_type: int
    resource_name: str
    resource_pattern_type: int
    acls: List[_DescribeAclsResponseAclDict]


class _DescribeAclsResponseDict(TypedDict):
    throttle_time_ms: int
    error_code: int
    error_message: str
    resources: List[Union[_DescribeAclsResponseResourceV0Dict, _DescribeAclsResponseResourceV1Dict]]


class _DescribeAclsResponse(Response[_DescribeAclsResponseDict]):
    API_KEY = 29

    throttle_time_ms: int
    error_code: int
    error_message: str
    resources: List[Union[
        Tuple[int, str, List[Tuple[str, str, int, int]]],  # v0
        Tuple[int, str, int, List[Tuple[str, str, int, int]]]  # v1+
    ]]


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


@final
class DescribeAclsResponse_v2(_DescribeAclsResponse):
    API_VERSION = 2
    SCHEMA = DescribeAclsResponse_v1.SCHEMA


class _DescribeAclsRequestDict(TypedDict):
    resource_type: int
    resource_name: str
    principal: str
    host: str
    operation: int
    permission_type: int
    resource_pattern_type_filter: NotRequired[int]  # added in v1


_DescribeAclsResponseType = TypeVar('_DescribeAclsResponseType', bound=_DescribeAclsResponse)


class _DescribeAclsRequest(Request[_DescribeAclsResponseType, _DescribeAclsRequestDict]):
    API_KEY = 29

    resource_type: int
    resource_name: str
    principal: str
    host: str
    operation: int
    permission_type: int
    resource_pattern_type_filter: int  # added in v1


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


class _CreateAclsResponseCreationDict(TypedDict):
    error_code: int
    error_message: str


class _CreateAclsResponseDict(TypedDict):
    throttle_time_ms: int
    creation_responses: List[_CreateAclsResponseCreationDict]


class _CreateAclResponse(Response[_CreateAclsResponseDict]):
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


class _CreateAclsRequestCreationV0Dict(TypedDict):
    resource_type: int
    resource_name: str
    principal: str
    host: str
    operation: int
    permission_type: int


class _CreateAclsRequestCreationV1Dict(_CreateAclsRequestCreationV0Dict):
    resource_pattern_type: int


class _CreateAclsRequestDict(TypedDict):
    creations: List[Union[_CreateAclsRequestCreationV0Dict, _CreateAclsRequestCreationV1Dict]]


_CreateAclResponseType = TypeVar('_CreateAclResponseType', bound=_CreateAclResponse)


class _CreateAclRequest(Request[_CreateAclResponseType, _CreateAclsRequestDict]):
    API_KEY = 30

    creations: List[Union[
        Tuple[int, str, str, str, int, int],                     # v0
        Tuple[int, str, int, str, str, int, int]                 # v1
    ]]


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


class _DeleteAclsResponseMatchingAclV0Dict(TypedDict):
    error_code: int
    error_message: str
    resource_type: int
    resource_name: str
    principal: str
    host: str
    operation: int
    permission_type: int


class _DeleteAclsResponseMatchingAclV1Dict(_DeleteAclsResponseMatchingAclV0Dict):
    resource_pattern_type: int  # added in v1


class _DeleteAclsResponseFilterResponseDict(TypedDict):
    error_code: int
    error_message: str
    matching_acls: List[Union[_DeleteAclsResponseMatchingAclV0Dict, _DeleteAclsResponseMatchingAclV1Dict]]


class _DeleteAclsResponseDict(TypedDict):
    throttle_time_ms: int
    filter_responses: List[_DeleteAclsResponseFilterResponseDict]


class _DeleteAclsResponse(Response[_DeleteAclsResponseDict]):
    API_KEY = 31

    throttle_time_ms: int
    filter_responses: List[Union[
        Tuple[int, str, List[Tuple[int, str, int, str, str, str, int, int]]],                # v0
        Tuple[int, str, List[Tuple[int, str, int, str, int, str, str, int, int]]]             # v1
    ]]


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


class _DeleteAclsRequestFilterV0Dict(TypedDict):
    resource_type: int
    resource_name: str
    principal: str
    host: str
    operation: int
    permission_type: int


class _DeleteAclsRequestFilterV1Dict(_DeleteAclsRequestFilterV0Dict):
    resource_pattern_type_filter: int  # added in v1


class _DeleteAclsRequestDict(TypedDict):
    filters: List[Union[_DeleteAclsRequestFilterV0Dict, _DeleteAclsRequestFilterV1Dict]]


_DeleteAclsResponseType = TypeVar('_DeleteAclsResponseType', bound=_DeleteAclsResponse)


class _DeleteAclsRequest(Request[_DeleteAclsResponseType, _DeleteAclsRequestDict]):
    API_KEY = 31

    filters: List[Union[
        Tuple[int, str, str, str, int, int],               # v0
        Tuple[int, str, int, str, str, int, int]           # v1
    ]]


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


class _AlterConfigsResponseResourceDict(TypedDict):
    error_code: int
    error_message: str
    resource_type: int
    resource_name: str


class _AlterConfigsResponseDict(TypedDict):
    throttle_time_ms: int
    resources: List[_AlterConfigsResponseResourceDict]


class _AlterConfigsResponse(Response[_AlterConfigsResponseDict]):
    API_KEY = 33
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('resources', Array(
            ('error_code', Int16),
            ('error_message', String('utf-8')),
            ('resource_type', Int8),
            ('resource_name', String('utf-8'))))
    )

    throttle_time_ms: int
    resources: List[Tuple[int, str, int, str]]


@final
class AlterConfigsResponse_v0(_AlterConfigsResponse):
    API_VERSION = 0


@final
class AlterConfigsResponse_v1(_AlterConfigsResponse):
    API_VERSION = 1


class _AlterConfigsRequestConfigEntryDict(TypedDict):
    config_name: str
    config_value: str


class _AlterConfigsRequestResourceDict(TypedDict):
    resource_type: int
    resource_name: str
    config_entries: List[_AlterConfigsRequestConfigEntryDict]


class _AlterConfigsRequestDict(TypedDict):
    resources: List[_AlterConfigsRequestResourceDict]
    validate_only: bool


_AlterConfigsResponseType = TypeVar('_AlterConfigsResponseType', bound=_AlterConfigsResponse)


class _AlterConfigsRequest(Request[_AlterConfigsResponseType, _AlterConfigsRequestDict]):
    API_KEY = 33
    SCHEMA = Schema(
        ('resources', Array(
            ('resource_type', Int8),
            ('resource_name', String('utf-8')),
            ('config_entries', Array(
                ('config_name', String('utf-8')),
                ('config_value', String('utf-8')))))),
        ('validate_only', Boolean)
    )

    resources: List[Tuple[int, str, List[Tuple[str, str]]]]
    validate_only: bool


@final
class AlterConfigsRequest_v0(_AlterConfigsRequest[AlterConfigsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = AlterConfigsResponse_v0


@final
class AlterConfigsRequest_v1(_AlterConfigsRequest[AlterConfigsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = AlterConfigsResponse_v1


AlterConfigsRequest: List[Type[_AlterConfigsRequest]] = [AlterConfigsRequest_v0, AlterConfigsRequest_v1]
AlterConfigsResponse: List[Type[_AlterConfigsResponse]] = [AlterConfigsResponse_v0, AlterConfigsResponse_v1]


class _DescribeConfigsResponseConfigEntryV0Dict(TypedDict):
    config_names: str
    config_value: str
    read_only: bool
    is_default: bool
    is_sensitive: bool


class _DescribeConfigsResponseConfigEntryV1Dict(TypedDict):
    config_names: str
    config_value: str
    read_only: bool
    config_source: int
    is_sensitive: bool
    config_synonyms: List[Tuple[str, str, int]]


class _DescribeConfigsResponseResourceV0Dict(TypedDict):
    error_code: int
    error_message: str
    resource_type: int
    resource_name: str
    config_entries: List[_DescribeConfigsResponseConfigEntryV0Dict]


class _DescribeConfigsResponseResourceV1Dict(TypedDict):
    error_code: int
    error_message: str
    resource_type: int
    resource_name: str
    config_entries: List[_DescribeConfigsResponseConfigEntryV1Dict]


class _DescribeConfigsResponseDict(TypedDict):
    throttle_time_ms: int
    resources: List[Union[_DescribeConfigsResponseResourceV0Dict, _DescribeConfigsResponseResourceV1Dict]]


class _DescribeConfigsResponse(Response[_DescribeConfigsResponseDict]):
    API_KEY = 32

    throttle_time_ms: int
    resources: List[Union[
        Tuple[int, str, int, str, List[Tuple[str, str, bool, bool, bool]]],  # v0
        Tuple[int, str, int, str, List[Tuple[str, str, bool, int, bool, List[Tuple[str, str, int]]]]]  # v1+
    ]]


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


@final
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


@final
class DescribeConfigsResponse_v2(_DescribeConfigsResponse):
    API_VERSION = 2
    SCHEMA = DescribeConfigsResponse_v1.SCHEMA


class _DescribeConfigsRequestResourceDict(TypedDict):
    resource_type: int
    resource_name: str
    config_names: List[str]


class _DescribeConfigsRequestDict(TypedDict):
    resources: List[_DescribeConfigsRequestResourceDict]
    include_synonyms: NotRequired[bool]  # added in v1


_DescribeConfigsResponseType = TypeVar('_DescribeConfigsResponseType', bound=_DescribeConfigsResponse)


class _DescribeConfigsRequest(Request[_DescribeConfigsResponseType, _DescribeConfigsRequestDict]):
    API_KEY = 32

    resources: List[Tuple[int, str, List[str]]]
    include_synonyms: bool  # added in v1


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


class _DescribeLogDirsResponsePartitionDict(TypedDict):
    partition_index: int
    partition_size: int
    offset_lag: int
    is_future_key: bool


class _DescribeLogDirsResponseTopicDict(TypedDict):
    name: str
    partitions: List[_DescribeLogDirsResponsePartitionDict]


class _DescribeLogDirsResponseLogDirDict(TypedDict):
    error_code: int
    log_dir: str
    topics: List[_DescribeLogDirsResponseTopicDict]


class _DescribeLogDirsResponseDict(TypedDict):
    throttle_time_ms: int
    log_dirs: List[_DescribeLogDirsResponseLogDirDict]


class _DescribeLogDirsResponse(Response[_DescribeLogDirsResponseDict]):
    API_KEY = 35
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

    throttle_time_ms: int
    log_dirs: List[Tuple[int, str, List[Tuple[str, List[Tuple[int, int, int, bool]]]]]]


@final
class DescribeLogDirsResponse_v0(_DescribeLogDirsResponse):
    API_VERSION = 0


class _DescribeLogDirsRequestTopicDict(TypedDict):
    topic: str
    partitions: int


class _DescribeLogDirsRequestDict(TypedDict):
    topics: List[_DescribeLogDirsRequestTopicDict]


_DescribeLogDirsResponseType = TypeVar('_DescribeLogDirsResponseType', bound=_DescribeLogDirsResponse)


class _DescribeLogDirsRequest(Request[_DescribeLogDirsResponseType, _DescribeLogDirsRequestDict]):
    API_KEY = 35
    SCHEMA = Schema(
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Int32)
        ))
    )

    topics: List[Tuple[str, int]]


@final
class DescribeLogDirsRequest_v0(_DescribeLogDirsRequest[DescribeLogDirsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = DescribeLogDirsResponse_v0


DescribeLogDirsResponse: List[Type[_DescribeLogDirsResponse]] = [
    DescribeLogDirsResponse_v0,
]
DescribeLogDirsRequest: List[Type[_DescribeLogDirsRequest]] = [
    DescribeLogDirsRequest_v0,
]


class _SaslAuthenticateResponseDict(TypedDict):
    error_code: int
    error_message: str
    sasl_auth_bytes: bytes
    session_lifetime_ms: NotRequired[int]  # added in v1


class _SaslAuthenticateResponse(Response[_SaslAuthenticateResponseDict]):
    API_KEY = 36

    error_code: int
    error_message: str
    sasl_auth_bytes: bytes
    session_lifetime_ms: int  # added in v1


@final
class SaslAuthenticateResponse_v0(_SaslAuthenticateResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('error_code', Int16),
        ('error_message', String('utf-8')),
        ('sasl_auth_bytes', Bytes)
    )


@final
class SaslAuthenticateResponse_v1(_SaslAuthenticateResponse):
    API_VERSION = 1
    SCHEMA = Schema(
        ('error_code', Int16),
        ('error_message', String('utf-8')),
        ('sasl_auth_bytes', Bytes),
        ('session_lifetime_ms', Int64)
    )


class _SaslAuthenticateRequestDict(TypedDict):
    sasl_auth_bytes: bytes


_SaslAuthenticateResponseType = TypeVar('_SaslAuthenticateResponseType', bound=_SaslAuthenticateResponse)


class _SaslAuthenticateRequest(Request[_SaslAuthenticateResponseType, _SaslAuthenticateRequestDict]):
    API_KEY = 36
    SCHEMA = Schema(
        ('sasl_auth_bytes', Bytes)
    )

    sasl_auth_bytes: bytes


@final
class SaslAuthenticateRequest_v0(_SaslAuthenticateRequest[SaslAuthenticateResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = SaslAuthenticateResponse_v0


@final
class SaslAuthenticateRequest_v1(_SaslAuthenticateRequest[SaslAuthenticateResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = SaslAuthenticateResponse_v1


SaslAuthenticateRequest: List[Type[_SaslAuthenticateRequest]] = [
    SaslAuthenticateRequest_v0, SaslAuthenticateRequest_v1,
]
SaslAuthenticateResponse: List[Type[_SaslAuthenticateResponse]] = [
    SaslAuthenticateResponse_v0, SaslAuthenticateResponse_v1,
]


class _CreatePartitionsResponseTopicErrorDict(TypedDict):
    topic: str
    error_code: int
    error_message: str


class _CreatePartitionsResponseDict(TypedDict):
    throttle_time_ms: int
    topic_errors: List[_CreatePartitionsResponseTopicErrorDict]


class _CreatePartitionsResponse(Response[_CreatePartitionsResponseDict]):
    API_KEY = 37
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('topic_errors', Array(
            ('topic', String('utf-8')),
            ('error_code', Int16),
            ('error_message', String('utf-8'))))
    )

    throttle_time_ms: int
    topic_errors: List[Tuple[str, int, str]]


@final
class CreatePartitionsResponse_v0(_CreatePartitionsResponse):
    API_VERSION = 0


@final
class CreatePartitionsResponse_v1(_CreatePartitionsResponse):
    API_VERSION = 1


class _CreatePartitionsRequestNewPartitionsDict(TypedDict):
    count: int
    assignment: List[List[int]]


class _CreatePartitionsRequestTopicPartitionsDict(TypedDict):
    topic: str
    new_partitions: _CreatePartitionsRequestNewPartitionsDict


class _CreatePartitionsRequestDict(TypedDict):
    topic_partitions: List[_CreatePartitionsRequestTopicPartitionsDict]
    timeout: int
    validate_only: bool


_CreatePartitionsResponseType = TypeVar('_CreatePartitionsResponseType', bound=_CreatePartitionsResponse)


class _CreatePartitionsRequest(Request[_CreatePartitionsResponseType, _CreatePartitionsRequestDict]):
    API_KEY = 37
    SCHEMA = Schema(
        ('topic_partitions', Array(
            ('topic', String('utf-8')),
            ('new_partitions', Schema(
                ('count', Int32),
                ('assignment', Array(Array(Int32))))))),
        ('timeout', Int32),
        ('validate_only', Boolean)
    )

    topic_partitions: List[Tuple[str, Tuple[int, List[List[int]]]]]
    timeout: int
    validate_only: bool


@final
class CreatePartitionsRequest_v0(_CreatePartitionsRequest[CreatePartitionsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = CreatePartitionsResponse_v0


@final
class CreatePartitionsRequest_v1(_CreatePartitionsRequest[CreatePartitionsResponse_v1]):
    API_VERSION = 1
    RESPONSE_TYPE = CreatePartitionsResponse_v1


CreatePartitionsRequest: List[Type[_CreatePartitionsRequest]] = [
    CreatePartitionsRequest_v0, CreatePartitionsRequest_v1,
]
CreatePartitionsResponse: List[Type[_CreatePartitionsResponse]] = [
    CreatePartitionsResponse_v0, CreatePartitionsResponse_v1,
]


class _DeleteGroupsResponseResultDict(TypedDict):
    group_id: str
    error_code: int


class _DeleteGroupsResponseDict(TypedDict):
    throttle_time_ms: int
    results: List[_DeleteGroupsResponseResultDict]


class _DeleteGroupsResponse(Response[_DeleteGroupsResponseDict], ABC):
    SCHEMA = Schema(
        ("throttle_time_ms", Int32),
        ("results", Array(
            ("group_id", String("utf-8")),
            ("error_code", Int16)))
    )

    throttle_time_ms: int
    results: List[Tuple[str, int]]


@final
class DeleteGroupsResponse_v0(_DeleteGroupsResponse):
    API_KEY = 42
    API_VERSION = 0


@final
class DeleteGroupsResponse_v1(_DeleteGroupsResponse):
    API_KEY = 42
    API_VERSION = 1


class _DeleteGroupsRequestDict(TypedDict):
    groups_names: List[str]


_DeleteGroupsResponseType = TypeVar('_DeleteGroupsResponseType', bound=_DeleteGroupsResponse)


class _DeleteGroupsRequest(Request[_DeleteGroupsResponseType, _DeleteGroupsRequestDict], ABC):
    SCHEMA = Schema(
        ("groups_names", Array(String("utf-8")))
    )

    groups_names: List[str]


@final
class DeleteGroupsRequest_v0(_DeleteGroupsRequest[DeleteGroupsResponse_v0]):
    API_KEY = 42
    API_VERSION = 0
    RESPONSE_TYPE = DeleteGroupsResponse_v0


@final
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


class _DescribeClientQuotasResponseEntityDict(TypedDict):
    entity_type: str
    entity_name: str


class _DescribeClientQuotasResponseEntryValueDict(TypedDict):
    name: str
    value: float


class _DescribeClientQuotasResponseEntryDict(TypedDict):
    entity: List[_DescribeClientQuotasResponseEntityDict]
    values: List[_DescribeClientQuotasResponseEntryValueDict]


class _DescribeClientQuotasResponseDict(TypedDict):
    throttle_time_ms: int
    error_code: int
    error_message: str
    entries: List[_DescribeClientQuotasResponseEntryDict]


class _DescribeClientQuotasResponse(Response[_DescribeClientQuotasResponseDict]):
    API_KEY = 48
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

    throttle_time_ms: int
    error_code: int
    error_message: str
    entries: List[Tuple[List[Tuple[str, str]], List[Tuple[str, float]]]]


@final
class DescribeClientQuotasResponse_v0(_DescribeClientQuotasResponse):
    API_VERSION = 0


class _DescribeClientQuotasRequestComponentDict(TypedDict):
    entity_type: str
    match_type: int
    match: str


class _DescribeClientQuotasRequestDict(TypedDict):
    components: List[_DescribeClientQuotasRequestComponentDict]
    strict: bool


_DescribeClientQuotasResponseType = TypeVar('_DescribeClientQuotasResponseType', bound=_DescribeClientQuotasResponse)


class _DescribeClientQuotasRequest(Request[_DescribeClientQuotasResponseType, _DescribeClientQuotasRequestDict]):
    API_KEY = 48
    SCHEMA = Schema(
        ('components', Array(
            ('entity_type', String('utf-8')),
            ('match_type', Int8),
            ('match', String('utf-8')),
        )),
        ('strict', Boolean)
    )

    components: List[Tuple[str, int, str]]
    strict: bool


@final
class DescribeClientQuotasRequest_v0(_DescribeClientQuotasRequest[DescribeClientQuotasResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = DescribeClientQuotasResponse_v0


DescribeClientQuotasRequest: List[Type[_DescribeClientQuotasRequest]] = [
    DescribeClientQuotasRequest_v0,
]

DescribeClientQuotasResponse: List[Type[_DescribeClientQuotasResponse]] = [
    DescribeClientQuotasResponse_v0,
]


class _AlterPartitionReassignmentsResponsePartitionDict(TypedDict):
    partition_index: int
    error_code: int
    error_message: str


class _AlterPartitionReassignmentsResponseTopicDict(TypedDict):
    name: str
    partitions: List[_AlterPartitionReassignmentsResponsePartitionDict]


class _AlterPartitionReassignmentsResponseDict(TypedDict):
    throttle_time_ms: int
    error_code: int
    error_message: str
    responses: List[_AlterPartitionReassignmentsResponseTopicDict]


class _AlterPartitionReassignmentsResponse(Response[_AlterPartitionReassignmentsResponseDict]):
    API_KEY = 45
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

    throttle_time_ms: int
    error_code: int
    error_message: str
    responses: List[Tuple[str, List[Tuple[int, int, str]]]]


@final
class AlterPartitionReassignmentsResponse_v0(_AlterPartitionReassignmentsResponse):
    API_VERSION = 0


class _AlterPartitionReassignmentsRequestPartitionDict(TypedDict):
    partition_index: int
    replicas: List[int]


class _AlterPartitionReassignmentsRequestTopicDict(TypedDict):
    name: str
    partitions: List[_AlterPartitionReassignmentsRequestPartitionDict]


class _AlterPartitionReassignmentsRequestDict(TypedDict):
    timeout_ms: int
    topics: List[_AlterPartitionReassignmentsRequestTopicDict]


_AlterPartitionReassignmentsResponseType = TypeVar('_AlterPartitionReassignmentsResponseType', bound=_AlterPartitionReassignmentsResponse)


class _AlterPartitionReassignmentsRequest(Request[_AlterPartitionReassignmentsResponseType, _AlterPartitionReassignmentsRequestDict]):
    FLEXIBLE_VERSION = True
    API_KEY = 45
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

    timeout_ms: int
    topics: List[Tuple[str, List[Tuple[int, List[int]]]]]


@final
class AlterPartitionReassignmentsRequest_v0(_AlterPartitionReassignmentsRequest[AlterPartitionReassignmentsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = AlterPartitionReassignmentsResponse_v0


AlterPartitionReassignmentsRequest: List[Type[_AlterPartitionReassignmentsRequest]] = [
    AlterPartitionReassignmentsRequest_v0,
]

AlterPartitionReassignmentsResponse: List[Type[_AlterPartitionReassignmentsResponse]] = [
    AlterPartitionReassignmentsResponse_v0,
]


class _ListPartitionReassignmentsResponsePartitionDict(TypedDict):
    partition_index: int
    replicas: List[int]
    adding_replicas: List[int]
    removing_replicas: List[int]


class _ListPartitionReassignmentsResponseTopicDict(TypedDict):
    name: str
    partitions: List[_ListPartitionReassignmentsResponsePartitionDict]


class _ListPartitionReassignmentsResponseDict(TypedDict):
    throttle_time_ms: int
    error_code: int
    error_message: str
    topics: List[_ListPartitionReassignmentsResponseTopicDict]


class _ListPartitionReassignmentsResponse(Response[_ListPartitionReassignmentsResponseDict]):
    API_KEY = 46
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

    throttle_time_ms: int
    error_code: int
    error_message: str
    topics: List[Tuple[str, List[Tuple[int, List[int], List[int], List[int]]]]]


@final
class ListPartitionReassignmentsResponse_v0(_ListPartitionReassignmentsResponse):
    API_VERSION = 0


class _ListPartitionReassignmentsRequestTopicDict(TypedDict):
    name: str
    partition_index: List[int]


class _ListPartitionReassignmentsRequestDict(TypedDict):
    timeout_ms: int
    topics: List[_ListPartitionReassignmentsRequestTopicDict]


_ListPartitionReassignmentsResponseType = TypeVar('_ListPartitionReassignmentsResponseType', bound=_ListPartitionReassignmentsResponse)


class _ListPartitionReassignmentsRequest(Request[_ListPartitionReassignmentsResponseType, _ListPartitionReassignmentsRequestDict]):
    FLEXIBLE_VERSION = True
    API_KEY = 46
    SCHEMA = Schema(
        ("timeout_ms", Int32),
        ("topics", CompactArray(
            ("name", CompactString("utf-8")),
            ("partition_index", CompactArray(Int32)),
            ("tags", TaggedFields)
        )),
        ("tags", TaggedFields)
    )

    timeout_ms: int
    topics: List[Tuple[str, List[int]]]


@final
class ListPartitionReassignmentsRequest_v0(_ListPartitionReassignmentsRequest[ListPartitionReassignmentsResponse_v0]):
    API_VERSION = 0
    RESPONSE_TYPE = ListPartitionReassignmentsResponse_v0


ListPartitionReassignmentsRequest: List[Type[_ListPartitionReassignmentsRequest]] = [
    ListPartitionReassignmentsRequest_v0,
]

ListPartitionReassignmentsResponse: List[Type[_ListPartitionReassignmentsResponse]] = [
    ListPartitionReassignmentsResponse_v0,
]


class _ElectLeadersResponsePartitionResultDict(TypedDict):
    partition_id: int
    error_code: int
    error_message: str


class _ElectLeadersResponseReplicationElectionResultDict(TypedDict):
    topic: str
    partition_result: List[_ElectLeadersResponsePartitionResultDict]


class _ElectLeadersResponseDict(TypedDict):
    throttle_time_ms: int
    error_code: int
    replication_election_results: List[_ElectLeadersResponseReplicationElectionResultDict]


class _ElectLeadersResponse(Response[_ElectLeadersResponseDict]):
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


@final
class ElectLeadersResponse_v1(_ElectLeadersResponse):
    API_VERSION = 1


class _ElectLeadersRequestTopicPartitionsDict(TypedDict):
    topic: str
    partition_ids: List[int]


class _ElectLeadersRequestDict(TypedDict):
    election_type: int
    topic_partitions: List[_ElectLeadersRequestTopicPartitionsDict]
    timeout: int


_ElectLeadersResponseType = TypeVar('_ElectLeadersResponseType', bound=_ElectLeadersResponse)


class _ElectLeadersRequest(Request[_ElectLeadersResponseType, _ElectLeadersRequestDict]):
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


@final
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
