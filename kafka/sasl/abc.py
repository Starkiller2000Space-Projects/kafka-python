import abc


class SaslMechanism(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, **config) -> None:
        pass

    @abc.abstractmethod
    def auth_bytes(self) -> None:
        pass

    @abc.abstractmethod
    def receive(self, auth_bytes) -> None:
        pass

    @abc.abstractmethod
    def is_done(self) -> None:
        pass

    @abc.abstractmethod
    def is_authenticated(self) -> None:
        pass

    def auth_details(self) -> None:
        if not self.is_authenticated:
            raise RuntimeError('Not authenticated yet!')
        return 'Authenticated via SASL'
