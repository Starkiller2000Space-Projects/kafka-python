"""Type annotations for kafka producer."""

from collections.abc import Callable
from selectors import BaseSelector
from ssl import SSLContext
from typing import Any, Literal, TypedDict

from gssapi import Name

from kafka.metrics.metrics_reporter import AbstractMetricsReporter
from kafka.sasl.oauth import AbstractTokenProvider
from kafka.types import SASL_MECHANISM, SECURITY_PROTOCOLS


class KafkaProducerParams(TypedDict, total=False):
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
    security_protocol : SECURITY_PROTOCOLS
    ssl_context: SSLContext | None
    ssl_check_hostname: bool
    ssl_cafile: str | None
    ssl_certfile: str | None
    ssl_keyfile: str | None
    ssl_password: str | None
    ssl_crlfile: str | None
    ssl_ciphers: str
    api_version: tuple[int, int] | tuple[int, int, int] | None
    api_version_auto_timeout_ms: int
    metric_reporters: list[AbstractMetricsReporter]
    metrics_enabled: bool
    metrics_num_samples: int
    metrics_sample_window_ms: int
    selector: BaseSelector
    sasl_mechanism: SASL_MECHANISM
    sasl_plain_username: str
    sasl_plain_password: str
    sasl_kerberos_name: str | Name | None
    sasl_kerberos_service_name: str
    sasl_kerberos_domain_name: str
    sasl_oauth_token_provider: AbstractTokenProvider | None
    socks5_proxy: str | None
    kafka_client: Callable
