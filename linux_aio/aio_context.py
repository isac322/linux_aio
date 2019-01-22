# coding: UTF-8

from ctypes import c_long, c_uint, pointer
from types import TracebackType
from typing import Optional, Tuple, Type

from .aio_event import AIOEvent
from .block import AIOBlock
from .raw import (
    IOEvent, Timespec, aio_context_t, create_c_array, io_cancel, io_destroy, io_getevents, io_setup, io_submit, iocb_p
)


class AIOContext:
    """
    .. versionadded:: 0.2.0
    """
    __slots__ = ('_ctx', '_max_jobs')

    def __init__(self, max_jobs: int) -> None:
        self._ctx = aio_context_t()  # type: aio_context_t
        self._max_jobs = max_jobs  # type: int

        io_setup(c_uint(max_jobs), pointer(self._ctx))

    def __del__(self) -> None:
        self.close()

    @property
    def closed(self) -> bool:
        return self._ctx.value is 0

    def close(self) -> None:
        """will block on the completion of all operations that could not be canceled"""
        if not self.closed:
            io_destroy(self._ctx)
            self._ctx = aio_context_t()

    # noinspection PyProtectedMember
    def cancel(self, block: AIOBlock) -> AIOEvent:
        if block._deleted:
            raise ValueError(
                    '{} can not be used because it has already been transformed into another AIOBlock.'.format(block))

        result = IOEvent()

        io_cancel(self._ctx, pointer(block._iocb), pointer(result))

        return AIOEvent(result)

    # noinspection PyProtectedMember
    def submit(self, *blocks: AIOBlock) -> int:
        for block in blocks:
            if block._deleted:
                raise ValueError(
                        '{} can not be used because it has already '
                        'been transformed into another AIOBlock.'.format(block))

        return io_submit(
                self._ctx,
                c_long(len(blocks)),
                create_c_array(iocb_p, (pointer(block._iocb) for block in blocks))
        )

    def get_events(self, min_jobs: int, max_jobs: int, timeout_ns: int = 0) -> Tuple[AIOEvent, ...]:
        event_buf = create_c_array(IOEvent, (), max_jobs)

        completed_jobs = io_getevents(
                self._ctx,
                c_long(min_jobs),
                c_long(max_jobs),
                event_buf,
                pointer(Timespec(*divmod(timeout_ns, 1000000000))) if timeout_ns > 0 else None
        )

        return tuple(AIOEvent(event) for event in event_buf[:completed_jobs])

    def __enter__(self) -> 'AIOContext':
        return self

    def __exit__(self, t: Optional[Type[BaseException]], value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> None:
        self.close()
