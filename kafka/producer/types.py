"""Type annotations for kafka producer."""

from collections.abc import Callable
from typing import List, Literal, Optional, Tuple, TypedDict, Union

from kafka.metrics import KafkaMetric
from kafka.metrics.metrics_reporter import AbstractMetricsReporter
from kafka.producer.transaction_manager import TransactionManager
from kafka.types import AuthParams


class KafkaProducerParams(AuthParams, total=False):
    """Kafka producer initial parameters."""

    bootstrap_servers: Union[str, List[str]]
    client_id: str
    key_serializer: Optional[Callable[[object], bytes]]
    value_serializer: Optional[Callable[[object], bytes]]
    transactional_id: Optional[str]
    enable_idempotence: bool
    delivery_timeout_ms: float
    acks: Literal[0, 1, 'all']
    compression_type: Optional[str]
    retries: float
    batch_size: int
    linger_ms: int
    partitioner: Callable
    connections_max_idle_ms: int
    max_block_ms: int
    max_request_size: int
    allow_auto_create_topics: bool
    metadata_max_age_ms: int
    retry_backoff_ms: int
    request_timeout_ms: int
    receive_buffer_bytes: Optional[int]
    send_buffer_bytes: Optional[int]
    socket_options: List[Tuple[int, int, int]]
    reconnect_backoff_ms: int
    reconnect_backoff_max_ms: int
    max_in_flight_requests_per_connection: int
    metric_reporters: List[AbstractMetricsReporter]
    metrics_enabled: bool
    metrics_num_samples: int
    metrics_sample_window_ms: int
    kafka_client: Callable


class SenderParams(TypedDict, total=False):
    max_request_size: int
    acks: int
    retries: float
    request_timeout_ms: int
    retry_backoff_ms: int
    metrics: Optional[KafkaMetric]
    guarantee_message_order: bool
    transaction_manager: Optional[TransactionManager]
    transactional_id: Optional[str]
    transaction_timeout_ms: int
    client_id: str


class RecordAccumulatorParams(TypedDict, total=False):
    batch_size: int
    compression_attrs: int
    linger_ms: int
    request_timeout_ms: int
    delivery_timeout_ms: int
    retry_backoff_ms: int
    transaction_manager: Optional[TransactionManager]
    message_version: int
