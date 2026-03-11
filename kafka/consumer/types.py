import selectors
import ssl
from collections.abc import Callable
from typing import Any, Literal, TypedDict

import gssapi

from ..coordinator.assignors.abstract import AbstractPartitionAssignor
from ..metrics.metrics_reporter import AbstractMetricsReporter
from ..sasl.oauth import AbstractTokenProvider


class KafkaConsumerParams(TypedDict, total=False):
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
    security_protocol: Literal['PLAINTEXT', 'SSL', 'SASL_PLAINTEXT', 'SASL_SSL']
    ssl_context: ssl.SSLContext
    ssl_check_hostname: bool
    ssl_cafile: str
    ssl_certfile: str
    ssl_keyfile: str
    ssl_password: str
    ssl_crlfile: str
    ssl_ciphers: str
    api_version: tuple[int, int] | tuple[int, int, int]
    api_version_auto_timeout_ms: int
    connections_max_idle_ms: int
    metric_reporters: list[AbstractMetricsReporter]
    metrics_enabled: bool
    metrics_num_samples: int
    metrics_sample_window_ms: int
    selector: selectors.BaseSelector
    exclude_internal_topics: bool
    sasl_mechanism: Literal['PLAIN', 'GSSAPI', 'OAUTHBEARER', 'SCRAM-SHA-256', 'SCRAM-SHA-512']
    sasl_plain_username: str
    sasl_plain_password: str
    sasl_kerberos_name: str | gssapi.Name
    sasl_kerberos_service_name: str
    sasl_kerberos_domain_name: str
    sasl_oauth_token_provider: AbstractTokenProvider
    socks5_proxy: str
    kafka_client: Callable
