from kafka.metrics.measurable_stat import AbstractMeasurableStat


class Total(AbstractMeasurableStat):
    """An un-windowed cumulative total maintained over all time."""
    __slots__ = ('_total')

    def __init__(self, value=0.0) -> None:
        self._total = value

    def record(self, config, value, now) -> None:
        self._total += value

    def measure(self, config, now) -> None:
        return float(self._total)
