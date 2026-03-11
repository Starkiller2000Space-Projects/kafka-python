"""Type annotations for kafka admin client."""

from typing import List, Optional, Protocol, Tuple, Union

from typing_extensions import Unpack

from kafka.client_async import KafkaClient
from kafka.metrics import Metrics
from kafka.types import AuthParams, KafkaClientParams


class KafkaClientCallable(Protocol):
    """Protocol that describes callable used to retrieve kafka client."""

    def __call__(self, **kwargs: Unpack[KafkaClientParams]) -> KafkaClient: ...


class KafkaAdminClientParams(AuthParams, total=False):
    """Initial parameters for kafka admin client."""

    bootstrap_servers: Union[str, List[str]]
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
    metrics: Optional[Metrics]
    metric_group_prefix: str
    kafka_client: KafkaClientCallable
    # "metric_reporters", "metrics_num_samples", "metrics_sample_window_ms"
    sock_chunk_bytes: int  # undocumented experimental option
    sock_chunk_buffer_count: int  # undocumented experimental option

    # metrics configs
    metric_reporters: List
    metrics_num_samples: int
    metrics_sample_window_ms: int
