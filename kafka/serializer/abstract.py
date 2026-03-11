import abc


class Serializer(object):
    __meta__ = abc.ABCMeta

    def __init__(self, **config) -> None:
        pass

    @abc.abstractmethod
    def serialize(self, topic, value) -> None:
        pass

    def close(self) -> None:
        pass


class Deserializer(object):
    __meta__ = abc.ABCMeta

    def __init__(self, **config) -> None:
        pass

    @abc.abstractmethod
    def deserialize(self, topic, bytes_) -> None:
        pass

    def close(self) -> None:
        pass
