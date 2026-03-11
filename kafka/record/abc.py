import abc
from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, List, Literal, Optional, Tuple

if TYPE_CHECKING:
    from kafka.record.default_records import DefaultRecordMetadata


class ABCRecord(object, metaclass=abc.ABCMeta):
    __slots__ = ()

    @abc.abstractproperty
    def size_in_bytes(self) -> int:
        """ Number of total bytes in record
        """

    @abc.abstractproperty
    def offset(self) -> int:
        """ Absolute offset of record
        """

    @abc.abstractproperty
    def timestamp(self) -> int:
        """ Epoch milliseconds
        """

    @abc.abstractproperty
    def timestamp_type(self) -> Literal[0, 1]:
        """ CREATE_TIME(0) or APPEND_TIME(1)
        """

    @abc.abstractproperty
    def key(self) -> bytes | None:
        """ Bytes key or None
        """

    @abc.abstractproperty
    def value(self) -> bytes | None:
        """ Bytes value or None
        """

    @abc.abstractproperty
    def checksum(self) -> None:
        """ Prior to v2 format CRC was contained in every message. This will
            be the checksum for v0 and v1 and None for v2 and above.
        """

    @abc.abstractmethod
    def validate_crc(self) -> bool:
        """ Return True if v0/v1 record matches checksum. noop/True for v2 records
        """

    @abc.abstractproperty
    def headers(self) -> list[tuple[str, bytes]]:
        """ If supported by version list of key-value tuples, or empty list if
            not supported by format.
        """


class ABCRecordBatchBuilder(object, metaclass=abc.ABCMeta):
    __slots__ = ()

    @abc.abstractmethod
    def append(self, offset: int, timestamp: Optional[int], key: Optional[bytes], value: Optional[bytes], headers: Optional[List[Tuple[str, bytes]]] = None) -> DefaultRecordMetadata:
        """ Writes record to internal buffer.

        Arguments:
            offset (int): Relative offset of record, starting from 0
            timestamp (int or None): Timestamp in milliseconds since beginning
                of the epoch (midnight Jan 1, 1970 (UTC)). If omitted, will be
                set to current time.
            key (bytes or None): Key of the record
            value (bytes or None): Value of the record
            headers (List[Tuple[str, bytes]]): Headers of the record. Header
                keys can not be ``None``.

        Returns:
            (bytes, int): Checksum of the written record (or None for v2 and
                above) and size of the written record.
        """

    @abc.abstractmethod
    def size_in_bytes(self, offset: int, timestamp: Optional[int], key: Optional[bytes], value: Optional[bytes], headers: Optional[List[Tuple[str, bytes]]]) -> int:
        """ Return the expected size change on buffer (uncompressed) if we add
            this message. This will account for varint size changes and give a
            reliable size.
        """

    @abc.abstractmethod
    def build(self) -> bytearray:
        """ Close for append, compress if needed, write size and header and
            return a ready to send buffer object.

            Return:
                bytearray: finished batch, ready to send.
        """


class ABCRecordBatch(object, metaclass=abc.ABCMeta):
    """ For v2 encapsulates a RecordBatch, for v0/v1 a single (maybe
        compressed) message.
    """
    __slots__ = ()

    @abc.abstractmethod
    def __iter__(self) -> Iterator[ABCRecord]:
        """ Return iterator over records (ABCRecord instances). Will decompress
            if needed.
        """

    @abc.abstractproperty
    def base_offset(self) -> int:
        """ Return base offset for batch
        """

    @abc.abstractproperty
    def size_in_bytes(self) -> int:
        """ Return size of batch in bytes (includes header overhead)
        """

    @abc.abstractproperty
    def magic(self) -> Literal[0, 1, 2]:
        """ Return magic value (0, 1, 2) for batch.
        """


class ABCRecords(object, metaclass=abc.ABCMeta):
    __slots__ = ()

    @abc.abstractmethod
    def __init__(self, buffer: Sequence[bytes]) -> None:
        """ Initialize with bytes-like object conforming to the buffer
            interface (ie. bytes, bytearray, memoryview etc.).
        """

    @abc.abstractmethod
    def size_in_bytes(self) -> None:
        """ Returns the size of inner buffer.
        """

    @abc.abstractmethod
    def next_batch(self) -> None:
        """ Return next batch of records (ABCRecordBatch instances).
        """

    @abc.abstractmethod
    def has_next(self) -> None:
        """ True if there are more batches to read, False otherwise.
        """
