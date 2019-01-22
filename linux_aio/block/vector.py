# coding: UTF-8

from ctypes import addressof
from typing import Any, Iterable, Tuple, Union

from .rw import RWBlock, _NAT_BUF_TYPE
from ..raw import IOCBCMD, IOCBPriorityClass, IOCBRWFlag, IOVec, create_c_array


class VectorBlock(RWBlock):
    """
    .. versionadded:: 0.3.0
    """
    __slots__ = ('_io_vectors',)

    BUF_TYPE = Tuple[Union[bytearray, bytes], ...]

    def __init__(self,
                 file: Any,
                 cmd: IOCBCMD,
                 buffer: Iterable[_NAT_BUF_TYPE],
                 offset: int,
                 rw_flags: IOCBRWFlag,
                 priority_class: IOCBPriorityClass,
                 priority_value: int,
                 res_fd: int) -> None:
        self._buffer = tuple(buffer)
        self._io_vectors = self._create_io_vectors(self._buffer)

        super().__init__(file, cmd, addressof(self._io_vectors), len(self._buffer), offset,
                         rw_flags, priority_class, priority_value, res_fd)

    @classmethod
    def _create_io_vectors(cls, buffers: BUF_TYPE) -> Any:
        return create_c_array(
                IOVec,
                (IOVec(cls._inner_buf_pointer(buf), len(buf)) for buf in buffers)
        )

    @property
    def buffer(self) -> BUF_TYPE:
        return self._buffer

    @buffer.setter
    def buffer(self, buffer: Iterable[_NAT_BUF_TYPE]) -> None:
        self._buffer = tuple(buffer)
        self._io_vectors = self._create_io_vectors(self._buffer)
        self._iocb.aio_buf = addressof(self._io_vectors)
        self._iocb.aio_nbytes = len(self._buffer)


class ReadVBlock(VectorBlock):
    """
    .. versionadded:: 0.3.0
    """

    def __init__(self,
                 file: Any,
                 buffer_list: Iterable[_NAT_BUF_TYPE],
                 offset: int = 0,
                 rw_flags: IOCBRWFlag = 0,
                 priority_class: IOCBPriorityClass = IOCBPriorityClass.NONE,
                 priority_value: int = 0,
                 res_fd: int = 0) -> None:
        super().__init__(file, IOCBCMD.PREADV, buffer_list, offset, rw_flags, priority_class, priority_value, res_fd)


class WriteVBlock(VectorBlock):
    """
    .. versionadded:: 0.3.0
    """

    def __init__(self,
                 file: Any,
                 content_list: Iterable[_NAT_BUF_TYPE],
                 offset: int = 0,
                 rw_flags: IOCBRWFlag = 0,
                 priority_class: IOCBPriorityClass = IOCBPriorityClass.NONE,
                 priority_value: int = 0,
                 res_fd: int = 0) -> None:
        super().__init__(file, IOCBCMD.PWRITEV, content_list, offset, rw_flags, priority_class, priority_value, res_fd)
