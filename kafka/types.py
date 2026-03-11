"""Type annotations for kafka."""

from collections.abc import Callable
from selectors import BaseSelector
from ssl import SSLContext
from typing import Literal, TypedDict

import gssapi

from kafka.metrics import Metrics
from kafka.sasl.oauth import AbstractTokenProvider

SECURITY_PROTOCOLS = Literal['PLAINTEXT', 'SSL', 'SASL_PLAINTEXT', 'SASL_SSL']
SASL_MECHANISM = Literal['PLAIN', 'GSSAPI', 'OAUTHBEARER', 'SCRAM-SHA-256', 'SCRAM-SHA-512']


class BrockerConnectionParams(TypedDict):
    """Config params for brocker instance."""

    client_id: str
    client_software_name: str
    client_software_version: str
    reconnect_backoff_ms: int
    reconnect_backoff_max_ms: int
    request_timeout_ms: int
    max_in_flight_requests_per_connection: int
    receive_buffer_bytes: int | None
    send_buffer_bytes: int | None
    socket_options: list[tuple[int, int, int]]
    security_protocol: SECURITY_PROTOCOLS
    ssl_context: SSLContext | None
    ssl_check_hostname: bool
    ssl_cafile: str | None
    ssl_certfile: str | None
    ssl_keyfile: str | None
    ssl_password: Callable | str | bytes | bytearray | None
    ssl_crlfile: str | None
    ssl_ciphers: str
    api_version: tuple[int, int] | tuple[int, int, int] | None
    api_version_auto_timeout_ms: int
    selector: BaseSelector
    state_change_callback: Callable
    metrics: Metrics | None
    metric_group_prefix: str
    sasl_mechanism: SASL_MECHANISM
    sasl_plain_username: str
    sasl_plain_password: str
    sasl_kerberos_name: str | gssapi.Name | None
    sasl_kerberos_service_name: str
    sasl_kerberos_domain_name: str
    sasl_oauth_token_provider: AbstractTokenProvider | None
    socks5_proxy: str | None
