"""Type annotations for kafka producer."""

from collections.abc import Callable
from selectors import BaseSelector
from ssl import SSLContext
from typing import Any, List, Literal

from gssapi import Name

from kafka.metrics.metrics_reporter import AbstractMetricsReporter
from kafka.sasl.oauth import AbstractTokenProvider
from kafka.types import SASL_MECHANISM, SECURITY_PROTOCOLS, AuthParams


class KafkaProducerParams(AuthParams, total=False):
    """Kafka producer initial parameters."""

    bootstrap_servers: str | list[str]
    client_id: str
    key_serializer: Callable[[Any], bytes] | None
    value_serializer: Callable[[Any], bytes] | None
    transactional_id: str | None
    enable_idempotence: bool
    delivery_timeout_ms: float
    acks: Literal[0, 1, 'all']
    compression_type: str | None
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
    receive_buffer_bytes: int | None
    send_buffer_bytes: int | None
    socket_options: list[tuple[int, int, int]]
    reconnect_backoff_ms: int
    reconnect_backoff_max_ms: int
    max_in_flight_requests_per_connection: int
    metric_reporters: List[AbstractMetricsReporter]
    metrics_enabled: bool
    metrics_num_samples: int
    metrics_sample_window_ms: int
    kafka_client: Callable
