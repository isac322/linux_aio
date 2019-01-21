# coding: UTF-8

from .rw import RWBlock
from ..raw import IOCBCMD, IOCBPriorityClass, IOCBRWFlag


class NonVectorBlock(RWBlock):
    def __init__(self,
                 file,
                 cmd: IOCBCMD,
                 buffer: bytes or bytearray,
                 length: int,
                 offset: int,
                 rw_flags: IOCBRWFlag,
                 priority_class: IOCBPriorityClass,
                 priority_value: int,
                 res_fd: int) -> None:
        self._buffer = buffer

        super().__init__(file, cmd, self._inner_buf_addr(self._buffer), length, offset,
                         rw_flags, priority_class, priority_value, res_fd)

    @property
    def buffer(self) -> bytes or bytearray:
        return self._buffer

    @buffer.setter
    def buffer(self, buffer: bytes or bytearray) -> None:
        self._buffer = buffer
        self._iocb.aio_buf = self._inner_buf_addr(buffer)

    @property
    def length(self) -> int:
        return self._iocb.aio_nbytes

    @length.setter
    def length(self, new_len: int) -> None:
        self._iocb.aio_nbytes = new_len


class ReadBlock(NonVectorBlock):
    def __init__(self,
                 file,
                 buffer: bytes or bytearray or str,
                 offset: int = 0,
                 length: int = None,
                 rw_flags: IOCBRWFlag = 0,
                 priority_class: IOCBPriorityClass = IOCBPriorityClass.NONE,
                 priority_value: int = 0,
                 res_fd: int = 0) -> None:
        if isinstance(buffer, str):
            buffer = buffer.encode()
        else:
            buffer = buffer

        if length is None:
            length = len(buffer)

        super().__init__(file, IOCBCMD.PREAD, buffer, length, offset, rw_flags, priority_class, priority_value, res_fd)


class WriteBlock(NonVectorBlock):
    def __init__(self,
                 file,
                 content: bytes or bytearray or str,
                 offset: int = 0,
                 length: int = None,
                 rw_flags: IOCBRWFlag = 0,
                 priority_class: IOCBPriorityClass = IOCBPriorityClass.NONE,
                 priority_value: int = 0,
                 res_fd: int = 0) -> None:
        if isinstance(content, str):
            content = content.encode()
        else:
            content = content

        if length is None:
            length = len(content)

        super().__init__(file, IOCBCMD.PWRITE, content, length, offset, rw_flags,
                         priority_class, priority_value, res_fd)
