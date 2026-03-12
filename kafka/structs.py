""" Other useful structs """

from collections import namedtuple
from typing import NamedTuple

from kafka.errors import KafkaError


class TopicPartition(NamedTuple):
    """A topic and partition tuple

    Keyword Arguments:
        topic (str): A topic name
        partition (int): A partition id
    """

    topic: str
    partition: int


class BrokerMetadata(NamedTuple):
    """A Kafka broker metadata used by admin tools.

    Keyword Arguments:
        nodeID (int): The Kafka broker id.
        host (str): The Kafka broker hostname.
        port (int): The Kafka broker port.
        rack (str): The rack of the broker, which is used to in rack aware
                    partition assignment for fault tolerance.
        Examples: `RACK1`, `us-east-1d`. Default: None
    """
    nodeId: int
    host: str
    port: int
    rack: str | None


class PartitionMetadata(NamedTuple):
    """A topic partition metadata describing the state in the MetadataResponse.

    Keyword Arguments:
        topic (str): The topic name of the partition this metadata relates to.
        partition (int): The id of the partition this metadata relates to.
        leader (int): The id of the broker that is the leader for the partition.
        replicas (List[int]): The ids of all brokers that contain replicas of the
                            partition.
        isr (List[int]): The ids of all brokers that contain in-sync replicas of
                        the partition.
        error (KafkaError): A KafkaError object associated with the request for
                            this partition metadata.
    """
    topic: str
    partition: int
    leader: int
    leader_epoch: int
    replicas: list[int]
    isr: list[int]
    offline_replicas: list[int]
    error: KafkaError


class OffsetAndMetadata(NamedTuple):
    """The Kafka offset commit API

    The Kafka offset commit API allows users to provide additional metadata
    (in the form of a string) when an offset is committed. This can be useful
    (for example) to store information about which node made the commit,
    what time the commit was made, etc.

    Keyword Arguments:
        offset (int): The offset to be committed
        metadata (str): Non-null metadata
        leader_epoch (int): The last known epoch from the leader / broker
    """
    offset: int
    metadata: str
    leader_epoch: int


class OffsetAndTimestamp(NamedTuple):
    """An offset and timestamp tuple

    Keyword Arguments:
        offset (int): An offset
        timestamp (int): The timestamp associated to the offset
        leader_epoch (int): The last known epoch from the leader / broker
    """
    offset: int
    timestamp: int
    leader_epoch: int


class MemberInformation(NamedTuple):
    member_id: int
    client_id: int
    client_host: str
    member_metadata: str
    member_assignment: str


class GroupInformation(NamedTuple):

    error_code: int
    group: str
    state: str
    protocol_type: str
    protocol: str
    members: str
    authorized_operations: str


class RetryOptions(NamedTuple): 
    """Define retry policy for async producer

    Keyword Arguments:
        Limit (int): Number of retries. limit >= 0, 0 means no retries
        backoff_ms (int): Milliseconds to backoff.
        retry_on_timeouts:
    """
    limit: int
    backoff_ms: int
    retry_on_timeouts: bool
