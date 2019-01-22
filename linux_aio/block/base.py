# coding: UTF-8

from abc import ABCMeta
from ctypes import addressof, py_object
from typing import Any, Optional, overload

from ..raw import IOCB, IOCBCMD, IOCBFlag, IOCBPriorityClass, IOCBRWFlag, IOPRIO_CLASS_SHIFT, gen_io_priority


class AIOBlock(metaclass=ABCMeta):
    """
    .. versionadded:: 0.2.0
    .. versionchanged:: 0.3.0
    """
    __slots__ = ('_iocb', '_py_obj', '_file_obj', '_deleted')

    def __init__(self, file: Any, cmd: IOCBCMD, rw_flags: IOCBRWFlag, priority_class: IOCBPriorityClass,
                 priority_value: int, buffer: int, length: int, offset: int, res_fd: int) -> None:
        try:
            fd = file.fileno()
            self._file_obj = file
        except AttributeError:
            raise

        priority = gen_io_priority(priority_class, priority_value)

        flags = 0  # type: IOCBFlag

        if priority is not 0:
            flags |= IOCBFlag.IOPRIO

        if res_fd is not 0:
            flags |= IOCBFlag.RESFD

        # to avoid garbage collection
        self._deleted = False
        self._py_obj = py_object(self)  # type: py_object
        self._iocb = IOCB(  # type: IOCB
                aio_data=addressof(self._py_obj),
                aio_rw_flags=rw_flags,
                aio_lio_opcode=cmd,
                aio_reqprio=priority,
                aio_fildes=fd,
                aio_buf=buffer,
                aio_nbytes=length,
                aio_offset=offset,
                aio_flags=flags,
                aio_resfd=res_fd
        )

    def __hash__(self) -> int:
        return addressof(self._iocb)

    @overload
    def change_cmd(self, new_cmd: IOCBCMD.POLL) -> 'PollBlock':
        ...

    @overload
    def change_cmd(self, new_cmd: IOCBCMD.FDSYNC) -> 'FDsyncBlock':
        ...

    @overload
    def change_cmd(self, new_cmd: IOCBCMD.FSYNC) -> 'FsyncBlock':
        ...

    @overload
    def change_cmd(self, new_cmd: IOCBCMD.PREAD) -> 'ReadBlock':
        ...

    @overload
    def change_cmd(self, new_cmd: IOCBCMD.PWRITE) -> 'WriteBlock':
        ...

    @overload
    def change_cmd(self, new_cmd: IOCBCMD.PREADV) -> 'ReadVBlock':
        ...

    @overload
    def change_cmd(self, new_cmd: IOCBCMD.PWRITEV) -> 'WriteVBlock':
        ...

    def change_cmd(self, new_cmd: IOCBCMD) -> 'AIOBlock':
        if new_cmd is self.cmd:
            return self

        if new_cmd is IOCBCMD.PWRITE:
            from .non_vector import WriteBlock
            block = WriteBlock.__new__(WriteBlock)
            if self.cmd is not IOCBCMD.PREAD:
                self._reset_buf()

        elif new_cmd is IOCBCMD.PREAD:
            from .non_vector import ReadBlock
            block = ReadBlock.__new__(ReadBlock)
            if self.cmd is not IOCBCMD.PWRITE:
                self._reset_buf()

        elif new_cmd is IOCBCMD.FSYNC:
            from .non_rw import FsyncBlock
            block = FsyncBlock.__new__(FsyncBlock)
            self._reset_for_non_rw()

        elif new_cmd is IOCBCMD.FDSYNC:
            from .non_rw import FDsyncBlock
            block = FDsyncBlock.__new__(FDsyncBlock)
            self._reset_for_non_rw()

        elif new_cmd is IOCBCMD.POLL:
            from .non_rw import PollBlock
            block = PollBlock.__new__(PollBlock)
            self._reset_for_non_rw()

        elif new_cmd is IOCBCMD.PWRITEV:
            from .vector import WriteVBlock
            block = WriteVBlock.__new__(WriteVBlock)
            if self.cmd is not IOCBCMD.PREADV:
                self._reset_buf()

        elif new_cmd is IOCBCMD.PREADV:
            from .vector import ReadVBlock
            block = ReadVBlock.__new__(ReadVBlock)
            if self.cmd is not IOCBCMD.PWRITEV:
                self._reset_buf()
        else:
            raise ValueError('Unknown command :{}'.format(new_cmd))

        block._py_obj = py_object(block)
        block._iocb = self._iocb
        block._iocb.aio_lio_opcode = new_cmd
        block._iocb.aio_data = addressof(block._py_obj)
        block._file_obj = self._file_obj
        block._deleted = False

        self._deleted = True

        return block

    def _reset_for_non_rw(self) -> None:
        self._iocb.aio_flags = 0
        self._iocb.aio_rw_flags = 0
        self._reset_buf()

    def _reset_buf(self) -> None:
        self._iocb.aio_buf = 0
        self._iocb.aio_nbytes = 0
        self._iocb.aio_offset = 0

    @property
    def file(self) -> Any:
        return self._file_obj

    @property
    def fileno(self) -> int:
        return self._file_obj.fileno()

    @property
    def cmd(self) -> IOCBCMD:
        return IOCBCMD(self._iocb.aio_lio_opcode)

    @property
    def fd(self) -> int:
        return self._iocb.aio_fildes

    @fd.setter
    def fd(self, new_fd: int) -> None:
        self._iocb.aio_fildes = new_fd

    @property
    def flag(self) -> int:
        return self._iocb.aio_flags

    @flag.setter
    def flag(self, new_flag: int) -> None:
        self._iocb.aio_flags = new_flag

    @property
    def res_fd(self) -> Optional[int]:
        res_fd = self._iocb.aio_resfd
        if res_fd is not 0:
            return res_fd
        else:
            return None

    @res_fd.setter
    def res_fd(self, fd: int) -> None:
        self.flag |= IOCBFlag.RESFD
        self._iocb.aio_resfd = fd

    @property
    def priority_class(self) -> int:
        return self._iocb.aio_reqprio >> IOPRIO_CLASS_SHIFT

    @priority_class.setter
    def priority_class(self, new_class: IOCBPriorityClass) -> None:
        self.flag |= IOCBFlag.IOPRIO
        self._iocb.aio_reqprio = new_class << IOPRIO_CLASS_SHIFT | self.priority_value

    @property
    def priority_value(self) -> int:
        return self._iocb.aio_reqprio & ((1 << IOPRIO_CLASS_SHIFT) - 1)

    @priority_value.setter
    def priority_value(self, value: int) -> None:
        self.flag |= IOCBFlag.IOPRIO
        self._iocb.aio_reqprio = self.priority_class << IOPRIO_CLASS_SHIFT | value

    def set_priority(self, io_class: IOCBPriorityClass, priority: int) -> None:
        self.flag |= IOCBFlag.IOPRIO
        self._iocb.aio_reqprio = gen_io_priority(io_class, priority)
