import functools
import logging
import threading
from collections.abc import Callable, Iterable
from typing import Any, Generic, ParamSpec, TypeVar

from typing_extensions import Self

log = logging.getLogger(__name__)
Param = TypeVar('Param')
Params = ParamSpec('Params')
Value = TypeVar('Value')


class Future(Generic[Value]):
    error_on_callbacks = False  # and errbacks

    def __init__(self) -> None:
        self.is_done = False
        self.value: Value = None
        self.exception: BaseException | None = None
        self._callbacks: list[Callable[..., None]] = []
        self._errbacks: list[Callable[..., None]] = []
        self._lock = threading.Lock()

    def succeeded(self) -> bool:
        return self.is_done and not bool(self.exception)

    def failed(self) -> bool:
        return self.is_done and bool(self.exception)

    def retriable(self) -> bool:
        try:
            return self.exception.retriable
        except AttributeError:
            return False

    def success(self, value: Value) -> Self:
        assert not self.is_done, 'Future is already complete'
        with self._lock:
            self.value = value
            self.is_done = True
        if self._callbacks:
            self._call_backs('callback', self._callbacks, self.value)
        return self

    def failure(self, e: BaseException) -> Self:
        assert not self.is_done, 'Future is already complete'
        exception = e if type(e) is not type else e()
        assert isinstance(exception, BaseException), (
            'future failed without an exception')
        with self._lock:
            self.exception = exception
            self.is_done = True
        self._call_backs('errback', self._errbacks, self.exception)
        return self

    def add_callback(self, f: Callable[Params, None], *args: Params.args, **kwargs: Params.kwargs) -> Self:
        if args or kwargs:
            f = functools.partial(f, *args, **kwargs)
        with self._lock:
            if not self.is_done:
                self._callbacks.append(f)
            elif self.succeeded():
                self._lock.release()
                self._call_backs('callback', [f], self.value)
                self._lock.acquire()
        return self

    def add_errback(self, f: Callable[Params, None], *args: Params.args, **kwargs: Params.kwargs) -> Self:
        if args or kwargs:
            f = functools.partial(f, *args, **kwargs)
        with self._lock:
            if not self.is_done:
                self._errbacks.append(f)
            elif self.failed():
                self._lock.release()
                self._call_backs('errback', [f], self.exception)
                self._lock.acquire()
        return self

    def add_both(self, f: Callable[Params, None], *args: Params.args, **kwargs: Params.kwargs) -> Self:
        self.add_callback(f, *args, **kwargs)
        self.add_errback(f, *args, **kwargs)
        return self

    def chain(self, future: 'Future') -> Self:
        self.add_callback(future.success)
        self.add_errback(future.failure)
        return self

    def _call_backs(self, back_type: str, backs: Iterable[Callable[[Param], None]], value: Param) -> None:
        for f in backs:
            try:
                f(value)
            except Exception as e:
                log.exception('Error processing %s', back_type)
                if self.error_on_callbacks:
                    raise e
