"""Type annotations for kafka producer."""

from collections.abc import Callable
from typing import Any, List, Literal, Optional, Tuple, Union

from kafka.metrics.metrics_reporter import AbstractMetricsReporter
from kafka.types import AuthParams


class KafkaProducerParams(AuthParams, total=False):
    """Kafka producer initial parameters."""

    bootstrap_servers: Union[str, List[str]]
    client_id: str
    key_serializer: Optional[Callable[[Any], bytes]]
    value_serializer: Optional[Callable[[Any], bytes]]
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
