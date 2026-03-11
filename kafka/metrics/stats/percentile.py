class Percentile(object):
    __slots__ = ('_metric_name', '_percentile')

    def __init__(self, metric_name, percentile) -> None:
        self._metric_name = metric_name
        self._percentile = float(percentile)

    @property
    def name(self) -> None:
        return self._metric_name

    @property
    def percentile(self) -> None:
        return self._percentile
