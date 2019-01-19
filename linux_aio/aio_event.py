# coding: UTF-8

from ctypes import py_object

from .aio_block import AIOBlock
from .raw import IOEvent


class AIOEvent:
    __slots__ = ('_event',)

    def __init__(self, event: IOEvent) -> None:
        self._event = event  # type: IOEvent

    @property
    def aio_block(self) -> AIOBlock:
        return py_object.from_address(self._event.data).value

    @property
    def buffer(self) -> str or bytearray or bytes or None:
        return self.aio_block.buffer

    def stripped_buffer(self) -> str or bytearray or bytes or None:
        """`\0` pads removed buffer"""
        return self.buffer.rstrip(b'\0')

    @property
    def response(self) -> int:
        return self._event.res

    @property
    def response2(self) -> int:
        return self._event.res2
