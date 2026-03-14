import time
from typing import Optional

from kafka.metrics.measurable import AbstractMeasurable
from kafka.metrics.metric_config import MetricConfig


class KafkaMetric(object):
    __slots__ = ('_metric_name', '_measurable', '_config')

    # NOTE java constructor takes a lock instance
    def __init__(self, metric_name: str, measurable: AbstractMeasurable, config: MetricConfig) -> None:
        if not metric_name:
            raise ValueError('metric_name must be non-empty')
        if not measurable:
            raise ValueError('measurable must be non-empty')
        self._metric_name = metric_name
        self._measurable = measurable
        self._config = config

    @property
    def metric_name(self) -> str:
        return self._metric_name

    @property
    def measurable(self) -> bool:
        return self._measurable

    @property
    def config(self) -> MetricConfig:
        return self._config

    @config.setter
    def config(self, config: MetricConfig) -> None:
        self._config = config

    def value(self, time_ms: Optional[int] = None) -> None:
        if time_ms is None:
            time_ms = time.time() * 1000
        return self._measurable.measure(self._config, time_ms)
