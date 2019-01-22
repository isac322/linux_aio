# coding: UTF-8

from typing import Any, Union

from .rw import RWBlock
from ..raw import IOCBCMD, IOCBPriorityClass, IOCBRWFlag


class NonVectorBlock(RWBlock):
    """
    .. versionadded:: 0.3.0
    """

    BUF_TYPE = Union[bytearray, bytes]

    def __init__(self,
                 file: Any,
                 cmd: IOCBCMD,
                 buffer: BUF_TYPE,
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
    def buffer(self) -> BUF_TYPE:
        return self._buffer

    @buffer.setter
    def buffer(self, buffer: BUF_TYPE) -> None:
        self._buffer = buffer
        self._iocb.aio_buf = self._inner_buf_addr(buffer)

    @property
    def length(self) -> int:
        return self._iocb.aio_nbytes

    @length.setter
    def length(self, new_len: int) -> None:
        self._iocb.aio_nbytes = new_len


class ReadBlock(NonVectorBlock):
    """
    .. versionadded:: 0.3.0
    """

    def __init__(self,
                 file: Any,
                 buffer: Union[str, NonVectorBlock.BUF_TYPE],
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
    """
    .. versionadded:: 0.3.0
    """

    def __init__(self,
                 file: Any,
                 content: Union[str, NonVectorBlock.BUF_TYPE],
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
