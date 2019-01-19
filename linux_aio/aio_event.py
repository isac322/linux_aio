# coding: UTF-8

from ctypes import py_object
from typing import Optional

from .aio_block import AIOBlock, BUF_TYPE
from .raw import IOEvent


class AIOEvent:
    _event: IOEvent

    def __init__(self, event: IOEvent) -> None:
        self._event = event

    @property
    def aio_block(self) -> AIOBlock:
        return py_object.from_address(self._event.data).value

    @property
    def buffer(self) -> Optional[BUF_TYPE]:
        return self.aio_block.buffer

    def stripped_buffer(self) -> Optional[BUF_TYPE]:
        """`\0` pads removed buffer"""
        return self.buffer.rstrip(b'\0')

    @property
    def response(self) -> int:
        return self._event.res

    @property
    def response2(self) -> int:
        return self._event.res2
