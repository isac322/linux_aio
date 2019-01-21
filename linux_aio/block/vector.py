# coding: UTF-8

from ctypes import addressof

from .rw import RWBlock
from ..raw import IOCBCMD, IOCBPriorityClass, IOCBRWFlag, IOVec, create_c_array


class VectorBlock(RWBlock):
    __slots__ = ('_io_vectors',)

    def __init__(self,
                 file,
                 cmd: IOCBCMD,
                 buffer,
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
    def _create_io_vectors(cls, buffers):
        return create_c_array(
                IOVec,
                (IOVec(cls._inner_buf_pointer(buf), len(buf)) for buf in buffers)
        )

    @property
    def buffer(self):
        return self._buffer

    @buffer.setter
    def buffer(self, buffer) -> None:
        self._buffer = tuple(buffer)
        self._io_vectors = self._create_io_vectors(self._buffer)
        self._iocb.aio_buf = addressof(self._io_vectors)
        self._iocb.aio_nbytes = len(self._buffer)


class ReadVBlock(VectorBlock):
    def __init__(self,
                 file,
                 buffer_list,
                 offset: int = 0,
                 rw_flags: IOCBRWFlag = 0,
                 priority_class: IOCBPriorityClass = IOCBPriorityClass.NONE,
                 priority_value: int = 0,
                 res_fd: int = 0) -> None:
        super().__init__(file, IOCBCMD.PREADV, buffer_list, offset, rw_flags, priority_class, priority_value, res_fd)


class WriteVBlock(VectorBlock):
    def __init__(self,
                 file,
                 content_list,
                 offset: int = 0,
                 rw_flags: IOCBRWFlag = 0,
                 priority_class: IOCBPriorityClass = IOCBPriorityClass.NONE,
                 priority_value: int = 0,
                 res_fd: int = 0) -> None:
        super().__init__(file, IOCBCMD.PWRITEV, content_list, offset, rw_flags, priority_class, priority_value, res_fd)
