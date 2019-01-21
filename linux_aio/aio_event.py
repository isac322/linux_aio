# coding: UTF-8

from ctypes import py_object

from .block import AIOBlock, ReadBlock, ReadVBlock, WriteBlock, WriteVBlock
from .raw import IOEvent


class AIOEvent:
    __slots__ = ('_event', '_aio_block')

    def __init__(self, event: IOEvent) -> None:
        self._event = event  # type: IOEvent
        self._aio_block = py_object.from_address(self._event.data).value  # type: AIOBlock

    @property
    def aio_block(self) -> AIOBlock:
        return self._aio_block

    @property
    def buffer(self) -> bytearray or bytes or None or tuple:
        if isinstance(self._aio_block, (ReadBlock, WriteBlock, ReadVBlock, WriteVBlock)):
            return self._aio_block.buffer
        else:
            return None

    def stripped_buffer(self) -> bytearray or bytes or None or tuple:
        """`\0` pads removed buffer"""
        buffer = self.buffer

        if isinstance(buffer, (bytearray, bytes)):
            return buffer.rstrip(b'\0')
        elif isinstance(buffer, tuple):
            # TODO: implement me
            raise NotImplementedError('Stripping of buffer vector is not implemented yet.')
        else:
            return None

    @property
    def response(self) -> int:
        return self._event.res

    @property
    def response2(self) -> int:
        return self._event.res2
