# coding: UTF-8

from ctypes import py_object
from typing import Tuple, Union

from .block import AIOBlock, NonVectorBlock, ReadBlock, ReadVBlock, VectorBlock, WriteBlock, WriteVBlock
from .raw import IOEvent


class AIOEvent:
    __slots__ = ('_event', '_aio_block')

    _event: IOEvent
    _aio_block: AIOBlock

    def __init__(self, event: IOEvent) -> None:
        self._event = event
        self._aio_block = py_object.from_address(self._event.data).value

    @property
    def aio_block(self) -> AIOBlock:
        return self._aio_block

    @property
    def buffer(self) -> Union[None, VectorBlock.BUF_TYPE, NonVectorBlock.BUF_TYPE]:
        if isinstance(self._aio_block, (ReadBlock, WriteBlock, ReadVBlock, WriteVBlock)):
            return self._aio_block.buffer
        else:
            return None

    def stripped_buffer(self) -> Union[None, VectorBlock.BUF_TYPE, NonVectorBlock.BUF_TYPE]:
        """`\0` pads removed buffer"""
        buffer = self.buffer

        if isinstance(buffer, (bytearray, bytes)):
            return buffer.rstrip(b'\0')
        elif isinstance(buffer, Tuple):
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
