# coding: UTF-8

from abc import abstractmethod
from ctypes import c_char, c_char_p, c_void_p, cast
from typing import Any, Tuple, TypeVar, Union

from .base import AIOBlock
from ..raw import IOCBCMD, IOCBPriorityClass, IOCBRWFlag

_NAT_BUF_TYPE = TypeVar('_NAT_BUF_TYPE', bytearray, bytes)


class RWBlock(AIOBlock):
    """
    .. versionadded:: 0.3.0
    """
    __slots__ = ('_buffer',)

    BUF_TYPE = Union[_NAT_BUF_TYPE, Tuple[_NAT_BUF_TYPE, ...]]

    def __init__(self,
                 file: Any,
                 cmd: IOCBCMD,
                 buffer: int,
                 length: int,
                 offset: int,
                 rw_flags: IOCBRWFlag,
                 priority_class: IOCBPriorityClass,
                 priority_value: int,
                 res_fd: int) -> None:

        super().__init__(file, cmd, rw_flags, priority_class, priority_value,
                         buffer, length, offset, res_fd)

    @classmethod
    def _inner_buf_pointer(cls, buffer: Union[bytes, bytearray]) -> c_void_p:
        if isinstance(buffer, bytes):
            ori_pointer = c_char_p(buffer)

        elif isinstance(buffer, bytearray):
            arr_t = c_char * len(buffer)
            ori_pointer = arr_t.from_buffer(buffer)

        else:
            raise NotImplementedError('Unknown buffer type: {}'.format(type(buffer)))

        return cast(ori_pointer, c_void_p)

    @classmethod
    def _inner_buf_addr(cls, buffer: Union[bytes, bytearray]) -> int:
        return cls._inner_buf_pointer(buffer).value

    @property
    @abstractmethod
    def buffer(self) -> BUF_TYPE:
        pass

    @buffer.setter
    @abstractmethod
    def buffer(self, buffer: BUF_TYPE) -> None:
        pass

    @property
    def offset(self) -> int:
        return self._iocb.aio_offset

    @offset.setter
    def offset(self, new_offset: int) -> None:
        self._iocb.aio_offset = new_offset

    @property
    def rw_flag(self) -> int:
        return self._iocb.aio_rw_flags

    @rw_flag.setter
    def rw_flag(self, new_flag: int) -> None:
        self._iocb.aio_rw_flags = new_flag
