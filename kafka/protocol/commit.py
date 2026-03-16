from typing import List, Tuple, Type, TypedDict, TypeVar, Union, final

from typing_extensions import NotRequired

from kafka.protocol.api import Request, Response
from kafka.protocol.types import Array, Int16, Int32, Int64, Schema, String


class _OffsetCommitResponsePartitionDict(TypedDict):
    partition: int
    error_code: int


class _OffsetCommitResponseTopicDict(TypedDict):
    topic: str
    partitions: List[_OffsetCommitResponsePartitionDict]


class _OffsetCommitResponseDict(TypedDict):
    throttle_time_ms: NotRequired[int]  # added in v3
    topics: List[_OffsetCommitResponseTopicDict]


class _OffsetCommitResponse(Response[_OffsetCommitResponseDict]):
    API_KEY = 8

    throttle_time_ms: int  # added in v3
    topics: List[Tuple[str, List[Tuple[int, int]]]]


@final
class OffsetCommitResponse_v0(_OffsetCommitResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('error_code', Int16)))))
    )


@final
class OffsetCommitResponse_v1(_OffsetCommitResponse):
    API_VERSION = 1
    SCHEMA = OffsetCommitResponse_v0.SCHEMA


@final
class OffsetCommitResponse_v2(_OffsetCommitResponse):
    API_VERSION = 2
    SCHEMA = OffsetCommitResponse_v1.SCHEMA


@final
class OffsetCommitResponse_v3(_OffsetCommitResponse):
    API_VERSION = 3
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('error_code', Int16)))))
    )


@final
class OffsetCommitResponse_v4(_OffsetCommitResponse):
    API_VERSION = 4
    SCHEMA = OffsetCommitResponse_v3.SCHEMA


@final
class OffsetCommitResponse_v5(_OffsetCommitResponse):
    API_VERSION = 5
    SCHEMA = OffsetCommitResponse_v4.SCHEMA


@final
class OffsetCommitResponse_v6(_OffsetCommitResponse):
    API_VERSION = 6
    SCHEMA = OffsetCommitResponse_v5.SCHEMA


@final
class OffsetCommitResponse_v7(_OffsetCommitResponse):
    API_VERSION = 7
    SCHEMA = OffsetCommitResponse_v6.SCHEMA


class _OffsetCommitRequestPartitionV0Dict(TypedDict):
    partition: int
    offset: int
    metadata: str


class _OffsetCommitRequestPartitionV1Dict(_OffsetCommitRequestPartitionV0Dict):
    timestamp: int  # added in v1, dropped in v2


class _OffsetCommitRequestPartitionV2Dict(_OffsetCommitRequestPartitionV0Dict):
    pass


class _OffsetCommitRequestPartitionV6Dict(_OffsetCommitRequestPartitionV2Dict):
    leader_epoch: int  # added in v6


class _OffsetCommitRequestPartitionV7Dict(_OffsetCommitRequestPartitionV6Dict):
    pass


class _OffsetCommitRequestTopicV0Dict(TypedDict):
    topic: str
    partitions: List[_OffsetCommitRequestPartitionV0Dict]


class _OffsetCommitRequestTopicV1Dict(TypedDict):
    topic: str
    partitions: List[_OffsetCommitRequestPartitionV1Dict]


class _OffsetCommitRequestTopicV2Dict(TypedDict):
    topic: str
    partitions: List[_OffsetCommitRequestPartitionV2Dict]


class _OffsetCommitRequestTopicV6Dict(TypedDict):
    topic: str
    partitions: List[_OffsetCommitRequestPartitionV6Dict]


class _OffsetCommitRequestTopicV7Dict(TypedDict):
    topic: str
    partitions: List[_OffsetCommitRequestPartitionV7Dict]


class _OffsetCommitRequestDict(TypedDict):
    consumer_group: NotRequired[str]
    consumer_group_generation_id: NotRequired[int]  # added in v1, renamed in v7
    consumer_id: NotRequired[str]                    # added in v1, renamed in v7
    retention_time: NotRequired[int]                  # added in v2, dropped in v5
    group_id: NotRequired[str]                        # replaces consumer_group in v7
    generation_id: NotRequired[int]                   # replaces consumer_group_generation_id in v7
    member_id: NotRequired[str]                        # replaces consumer_id in v7
    group_instance_id: NotRequired[str]                # added in v7
    topics: List[Union[
        _OffsetCommitRequestTopicV0Dict,
        _OffsetCommitRequestTopicV1Dict,
        _OffsetCommitRequestTopicV2Dict,
        _OffsetCommitRequestTopicV6Dict,
        _OffsetCommitRequestTopicV7Dict,
    ]]


_OffsetCommitResponseType = TypeVar('_OffsetCommitResponseType', bound=_OffsetCommitResponse)


class _OffsetCommitRequest(Request[_OffsetCommitResponseType, _OffsetCommitRequestDict]):
    API_KEY = 8

    topics: List[Union[
        Tuple[str, List[Tuple[int, int, str]]],               # v0, v2-v5: (partition, offset, metadata)
        Tuple[str, List[Tuple[int, int, int, str]]],          # v1: (partition, offset, timestamp, metadata)
        Tuple[str, List[Tuple[int, int, int, str]]],          # v6: (partition, offset, leader_epoch, metadata)
        Tuple[str, List[Tuple[int, int, int, str]]],          # v7: same as v6 but top-level fields renamed
    ]]

    consumer_group: str
    consumer_group_generation_id: int        # added in v1, dropped in v7
    consumer_id: str                          # added in v1, dropped in v7
    retention_time: int                       # added in v2, dropped in v5 (default -1)
    group_id: str                              # replaces consumer_group in v7
    generation_id: int                         # replaces consumer_group_generation_id in v7
    member_id: str                              # replaces consumer_id in v7
    group_instance_id: str                      # added in v7


@final
class OffsetCommitRequest_v0(_OffsetCommitRequest[OffsetCommitResponse_v0]):
    API_VERSION = 0  # Zookeeper-backed storage
    RESPONSE_TYPE = OffsetCommitResponse_v0
    SCHEMA = Schema(
        ('consumer_group', String('utf-8')),
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('offset', Int64),
                ('metadata', String('utf-8'))))))
    )


@final
class OffsetCommitRequest_v1(_OffsetCommitRequest[OffsetCommitResponse_v1]):
    API_VERSION = 1  # Kafka-backed storage
    RESPONSE_TYPE = OffsetCommitResponse_v1
    SCHEMA = Schema(
        ('consumer_group', String('utf-8')),
        ('consumer_group_generation_id', Int32),
        ('consumer_id', String('utf-8')),
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('offset', Int64),
                ('timestamp', Int64),
                ('metadata', String('utf-8'))))))
    )


@final
class OffsetCommitRequest_v2(_OffsetCommitRequest[OffsetCommitResponse_v2]):
    API_VERSION = 2
    RESPONSE_TYPE = OffsetCommitResponse_v2
    SCHEMA = Schema(
        ('consumer_group', String('utf-8')),
        ('consumer_group_generation_id', Int32),
        ('consumer_id', String('utf-8')),
        ('retention_time', Int64),  # added retention_time, dropped timestamp
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('offset', Int64),
                ('metadata', String('utf-8'))))))
    )
    DEFAULT_RETENTION_TIME = -1


@final
class OffsetCommitRequest_v3(_OffsetCommitRequest[OffsetCommitResponse_v3]):
    API_VERSION = 3
    RESPONSE_TYPE = OffsetCommitResponse_v3
    SCHEMA = OffsetCommitRequest_v2.SCHEMA
    DEFAULT_RETENTION_TIME = -1


@final
class OffsetCommitRequest_v4(_OffsetCommitRequest[OffsetCommitResponse_v4]):
    API_VERSION = 4
    RESPONSE_TYPE = OffsetCommitResponse_v4
    SCHEMA = OffsetCommitRequest_v3.SCHEMA
    DEFAULT_RETENTION_TIME = -1


@final
class OffsetCommitRequest_v5(_OffsetCommitRequest[OffsetCommitResponse_v5]):
    API_VERSION = 5  # drops retention_time
    RESPONSE_TYPE = OffsetCommitResponse_v5
    SCHEMA = Schema(
        ('consumer_group', String('utf-8')),
        ('consumer_group_generation_id', Int32),
        ('consumer_id', String('utf-8')),
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('offset', Int64),
                ('metadata', String('utf-8'))))))
    )


@final
class OffsetCommitRequest_v6(_OffsetCommitRequest[OffsetCommitResponse_v6]):
    API_VERSION = 6
    RESPONSE_TYPE = OffsetCommitResponse_v6
    SCHEMA = Schema(
        ('consumer_group', String('utf-8')),
        ('consumer_group_generation_id', Int32),
        ('consumer_id', String('utf-8')),
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('offset', Int64),
                ('leader_epoch', Int32),  # added for fencing / kip-320. default -1
                ('metadata', String('utf-8'))))))
    )


@final
class OffsetCommitRequest_v7(_OffsetCommitRequest[OffsetCommitResponse_v7]):
    API_VERSION = 7
    RESPONSE_TYPE = OffsetCommitResponse_v7
    SCHEMA = Schema(
        ('group_id', String('utf-8')),
        ('generation_id', Int32),
        ('member_id', String('utf-8')),
        ('group_instance_id', String('utf-8')),  # added for static membership / kip-345
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('offset', Int64),
                ('leader_epoch', Int32),
                ('metadata', String('utf-8'))))))
    )


OffsetCommitRequest: List[Type[_OffsetCommitRequest]] = [
    OffsetCommitRequest_v0, OffsetCommitRequest_v1, OffsetCommitRequest_v2,
    OffsetCommitRequest_v3, OffsetCommitRequest_v4, OffsetCommitRequest_v5,
    OffsetCommitRequest_v6, OffsetCommitRequest_v7,
]
OffsetCommitResponse: List[Type[_OffsetCommitResponse]] = [
    OffsetCommitResponse_v0, OffsetCommitResponse_v1, OffsetCommitResponse_v2,
    OffsetCommitResponse_v3, OffsetCommitResponse_v4, OffsetCommitResponse_v5,
    OffsetCommitResponse_v6, OffsetCommitResponse_v7,
]


class _OffsetFetchResponsePartitionV0Dict(TypedDict):
    partition: int
    offset: int
    metadata: str
    error_code: int


class _OffsetFetchResponsePartitionV5Dict(_OffsetFetchResponsePartitionV0Dict):
    leader_epoch: int  # added in v5


class _OffsetFetchResponseTopicV0Dict(TypedDict):
    topic: str
    partitions: List[_OffsetFetchResponsePartitionV0Dict]


class _OffsetFetchResponseTopicV5Dict(TypedDict):
    topic: str
    partitions: List[_OffsetFetchResponsePartitionV5Dict]


class _OffsetFetchResponseDict(TypedDict):
    throttle_time_ms: NotRequired[int]  # added in v3
    error_code: NotRequired[int]        # added in v2
    topics: List[Union[_OffsetFetchResponseTopicV0Dict, _OffsetFetchResponseTopicV5Dict]]


class _OffsetFetchResponse(Response[_OffsetFetchResponseDict]):
    API_KEY = 9

    throttle_time_ms: int  # added in v3
    error_code: int        # added in v2
    topics: List[Union[
        Tuple[str, List[Tuple[int, int, str, int]]],               # v0-v4: (partition, offset, metadata, error_code)
        Tuple[str, List[Tuple[int, int, int, str, int]]]           # v5: (partition, offset, leader_epoch, metadata, error_code)
    ]]


@final
class OffsetFetchResponse_v0(_OffsetFetchResponse):
    API_VERSION = 0
    SCHEMA = Schema(
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('offset', Int64),
                ('metadata', String('utf-8')),
                ('error_code', Int16)))))
    )


@final
class OffsetFetchResponse_v1(_OffsetFetchResponse):
    API_VERSION = 1
    SCHEMA = OffsetFetchResponse_v0.SCHEMA


@final
class OffsetFetchResponse_v2(_OffsetFetchResponse):
    # Added in KIP-88: Allows passing null topics to return offsets for all partitions
    # that the consumer group has a stored offset for, even if no consumer in
    # the group is currently consuming that partition.
    API_VERSION = 2
    SCHEMA = Schema(
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('offset', Int64),
                ('metadata', String('utf-8')),
                ('error_code', Int16))))),
        ('error_code', Int16)
    )


@final
class OffsetFetchResponse_v3(_OffsetFetchResponse):
    API_VERSION = 3
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('offset', Int64),
                ('metadata', String('utf-8')),
                ('error_code', Int16))))),
        ('error_code', Int16)
    )


@final
class OffsetFetchResponse_v4(_OffsetFetchResponse):
    API_VERSION = 4
    SCHEMA = OffsetFetchResponse_v3.SCHEMA


@final
class OffsetFetchResponse_v5(_OffsetFetchResponse):
    API_VERSION = 5
    SCHEMA = Schema(
        ('throttle_time_ms', Int32),
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(
                ('partition', Int32),
                ('offset', Int64),
                ('leader_epoch', Int32),
                ('metadata', String('utf-8')),
                ('error_code', Int16))))),
        ('error_code', Int16)
    )


class _OffsetFetchRequestTopicDict(TypedDict):
    topic: str
    partitions: List[int]


class _OffsetFetchRequestDict(TypedDict):
    consumer_group: str
    topics: List[_OffsetFetchRequestTopicDict]


_OffsetFetchResponseType = TypeVar('_OffsetFetchResponseType', bound=_OffsetFetchResponse)


class _OffsetFetchRequest(Request[_OffsetFetchResponseType, _OffsetFetchRequestDict]):
    API_KEY = 9

    consumer_group: str
    topics: List[Tuple[str, List[int]]]


class OffsetFetchRequest_v0(_OffsetFetchRequest[OffsetFetchResponse_v0]):
    API_VERSION = 0  # zookeeper-backed storage
    RESPONSE_TYPE = OffsetFetchResponse_v0
    SCHEMA = Schema(
        ('consumer_group', String('utf-8')),
        ('topics', Array(
            ('topic', String('utf-8')),
            ('partitions', Array(Int32))))
    )


@final
class OffsetFetchRequest_v1(_OffsetFetchRequest[OffsetFetchResponse_v1]):
    API_VERSION = 1  # kafka-backed storage
    RESPONSE_TYPE = OffsetFetchResponse_v1
    SCHEMA = OffsetFetchRequest_v0.SCHEMA


@final
class OffsetFetchRequest_v2(_OffsetFetchRequest[OffsetFetchResponse_v2]):
    # KIP-88: Allows passing null topics to return offsets for all partitions
    # that the consumer group has a stored offset for, even if no consumer in
    # the group is currently consuming that partition.
    API_VERSION = 2
    RESPONSE_TYPE = OffsetFetchResponse_v2
    SCHEMA = OffsetFetchRequest_v1.SCHEMA


@final
class OffsetFetchRequest_v3(_OffsetFetchRequest[OffsetFetchResponse_v3]):
    API_VERSION = 3
    RESPONSE_TYPE = OffsetFetchResponse_v3
    SCHEMA = OffsetFetchRequest_v2.SCHEMA


@final
class OffsetFetchRequest_v4(_OffsetFetchRequest[OffsetFetchResponse_v4]):
    API_VERSION = 4
    RESPONSE_TYPE = OffsetFetchResponse_v4
    SCHEMA = OffsetFetchRequest_v3.SCHEMA


@final
class OffsetFetchRequest_v5(_OffsetFetchRequest[OffsetFetchResponse_v5]):
    API_VERSION = 5
    RESPONSE_TYPE = OffsetFetchResponse_v5
    SCHEMA = OffsetFetchRequest_v4.SCHEMA


OffsetFetchRequest: List[Type[_OffsetFetchRequest]] = [
    OffsetFetchRequest_v0, OffsetFetchRequest_v1,
    OffsetFetchRequest_v2, OffsetFetchRequest_v3,
    OffsetFetchRequest_v4, OffsetFetchRequest_v5,
]
OffsetFetchResponse: List[Type[_OffsetFetchResponse]] = [
    OffsetFetchResponse_v0, OffsetFetchResponse_v1,
    OffsetFetchResponse_v2, OffsetFetchResponse_v3,
    OffsetFetchResponse_v4, OffsetFetchResponse_v5,
]
