"""Type annotations for kafka."""

from collections.abc import Callable
from selectors import BaseSelector
from ssl import SSLContext
from typing import List, Literal, Optional, Set, Tuple, Type, TypedDict, Union

import gssapi

from kafka.metrics import Metrics
from kafka.sasl.oauth import AbstractTokenProvider

SECURITY_PROTOCOLS = Literal['PLAINTEXT', 'SSL', 'SASL_PLAINTEXT', 'SASL_SSL']
SASL_MECHANISM = Literal['PLAIN', 'GSSAPI', 'OAUTHBEARER', 'SCRAM-SHA-256', 'SCRAM-SHA-512']


class AuthParams(TypedDict, total=False):
    """Kafka universal authorization parameters."""

    api_version: Union[Tuple[int, int], Tuple[int, int, int], None]
    api_version_auto_timeout_ms: int
    selector: Type[BaseSelector]
    security_protocol: SECURITY_PROTOCOLS
    ssl_context: Optional[SSLContext]
    ssl_check_hostname: bool
    ssl_cafile: Optional[str]
    ssl_certfile: Optional[str]
    ssl_keyfile: Optional[str]
    ssl_password: Union[Callable, str, bytes, bytearray, None]
    ssl_crlfile: Optional[str]
    ssl_ciphers: str
    sasl_mechanism: Optional[SASL_MECHANISM]
    sasl_plain_username: Optional[str]
    sasl_plain_password: Optional[str]
    sasl_kerberos_name: Union[str, gssapi.Name, None]
    sasl_kerberos_service_name: str
    sasl_kerberos_domain_name: Optional[str]
    sasl_oauth_token_provider: Optional[AbstractTokenProvider]
    socks5_proxy: Optional[str]


class BrockerConnectionParams(AuthParams):
    """Config params for brocker instance."""

    client_id: str
    client_software_name: str
    client_software_version: str
    reconnect_backoff_ms: int
    reconnect_backoff_max_ms: int
    request_timeout_ms: int
    max_in_flight_requests_per_connection: int
    receive_buffer_bytes: Optional[int]
    send_buffer_bytes: Optional[int]
    socket_options: List[Tuple[int, int, int]]
    state_change_callback: Callable
    metrics: Optional[Metrics]
    metric_group_prefix: str


class KafkaClientParams(AuthParams, total=False):
    """Kafka client initial parameters."""

    bootstrap_servers: Union[list[str], str]
    client_id: str
    reconnect_backoff_ms: int
    reconnect_backoff_max_ms: int
    request_timeout_ms: int
    connections_max_idle_ms: int
    retry_backoff_ms: int
    max_in_flight_requests_per_connection: int
    receive_buffer_bytes: Optional[int]
    send_buffer_bytes: Optional[int]
    socket_options: List[Tuple[int, int, int]]
    metadata_max_age_ms: int
    allow_auto_create_topics: bool
    metrics: Optional[Metrics]
    metric_group_prefix: str

    # additional fields
    bootstrap_topics_filter: Set[str]
    wakeup_timeout_ms: int
    sock_chunk_bytes: int
    sock_chunk_buffer_count: int
