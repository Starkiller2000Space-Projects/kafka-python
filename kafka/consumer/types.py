import selectors
import ssl
from collections.abc import Callable
from typing import Any, Literal

import gssapi

from kafka.types import AuthParams

from ..coordinator.assignors.abstract import AbstractPartitionAssignor
from ..metrics.metrics_reporter import AbstractMetricsReporter
from ..sasl.oauth import AbstractTokenProvider


class KafkaConsumerParams(AuthParams, total=False):
    """Kafka consumer config params."""

    bootstrap_servers: str | list[str]
    client_id: str
    group_id: str | None
    group_instance_id: str
    key_deserializer: Callable[[bytes], Any]
    value_deserializer: Callable[[bytes], Any]
    enable_incremental_fetch_sessions: bool
    fetch_min_bytes: int
    fetch_max_wait_ms: int
    fetch_max_bytes: int
    max_partition_fetch_bytes: int
    request_timeout_ms: int
    retry_backoff_ms: int
    reconnect_backoff_ms: int
    reconnect_backoff_max_ms: int
    max_in_flight_requests_per_connection: int
    auto_offset_reset: Literal['earliest', 'latest']
    enable_auto_commit: bool
    auto_commit_interval_ms: int
    default_offset_commit_callback: Callable
    check_crcs: bool
    isolation_level: Literal['read_committed', 'read_uncommitted']
    allow_auto_create_topics: bool
    metadata_max_age_ms: int
    partition_assignment_strategy: list[AbstractPartitionAssignor]
    max_poll_records: int
    max_poll_interval_ms: int
    session_timeout_ms: int
    heartbeat_interval_ms: int
    receive_buffer_bytes: int
    send_buffer_bytes: int
    socket_options: list[int]
    consumer_timeout_ms: int
    connections_max_idle_ms: int
    metric_reporters: list[AbstractMetricsReporter]
    metrics_enabled: bool
    metrics_num_samples: int
    metrics_sample_window_ms: int
    exclude_internal_topics: bool
    kafka_client: Callable
