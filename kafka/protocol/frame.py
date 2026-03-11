class KafkaBytes(bytearray):
    def __init__(self, size) -> None:
        super(KafkaBytes, self).__init__(size)
        self._idx = 0

    def read(self, nbytes=None) -> None:
        if nbytes is None:
            nbytes = len(self) - self._idx
        start = self._idx
        self._idx += nbytes
        if self._idx > len(self):
            self._idx = len(self)
        return bytes(self[start:self._idx])

    def write(self, data) -> None:
        start = self._idx
        self._idx += len(data)
        self[start:self._idx] = data

    def seek(self, idx) -> None:
        self._idx = idx

    def tell(self) -> None:
        return self._idx

    def __str__(self) -> None:
        return 'KafkaBytes(%d)' % len(self)

    def __repr__(self) -> None:
        return str(self)
