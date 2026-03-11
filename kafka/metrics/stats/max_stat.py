from kafka.metrics.stats.sampled_stat import AbstractSampledStat


class Max(AbstractSampledStat):
    """An AbstractSampledStat that gives the max over its samples."""
    __slots__ = ('_initial_value', '_samples', '_current')

    def __init__(self) -> None:
        super(Max, self).__init__(float('-inf'))

    def update(self, sample, config, value, now) -> None:
        sample.value = max(sample.value, value)

    def combine(self, samples, config, now) -> None:
        if not samples:
            return float('-inf')
        return float(max(sample.value for sample in samples))
