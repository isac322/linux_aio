# coding: UTF-8

from ctypes import addressof, c_char, c_char_p, c_void_p, cast, py_object

from .raw import IOCB, IOCBCMD, IOCBFlag, IOCBPriorityClass, IOPRIO_CLASS_SHIFT, gen_io_priority


class AIOBlock:
    __slots__ = ('_iocb', '_buffer', '_py_obj')

    def __init__(self, fd: int, cmd: IOCBCMD, buffer: str or bytearray or bytes or None = None, offset: int = 0) \
            -> None:
        if isinstance(buffer, str):
            self._buffer = buffer.encode()  # type: str or bytearray or bytes or None
        else:
            self._buffer = buffer  # type: str or bytearray or bytes or None
        # to avoid garbage collection
        self._py_obj = py_object(self)  # type: py_object
        self._iocb = IOCB(  # type: IOCB
                aio_lio_opcode=cmd,
                aio_fildes=fd,
                aio_offset=offset,
                aio_nbytes=len(self._buffer),
                aio_buf=self._inner_addr_of(self._buffer),
                aio_data=addressof(self._py_obj)
        )

    def __hash__(self) -> int:
        return addressof(self._iocb)

    @classmethod
    def _inner_addr_of(cls, buffer: str or bytearray or bytes or None) -> int:
        if isinstance(buffer, bytearray):
            addr = addressof(c_char.from_buffer(buffer))
        elif isinstance(buffer, bytes):
            addr = cast(c_char_p(buffer), c_void_p).value
        elif buffer is None:
            addr = 0  # null pointer
        else:
            raise NotImplementedError('Unknown buffer type: {}'.format(type(buffer)))

        return addr

    @property
    def buffer(self) -> str or bytearray or bytes or None:
        return self._buffer

    @buffer.setter
    def buffer(self, buffer: str or bytearray or bytes or None) -> None:
        self._buffer = buffer
        self._iocb.aio_buf = self._inner_addr_of(buffer)

    @property
    def cmd(self) -> IOCBCMD:
        return IOCBCMD(self._iocb.aio_lio_opcode)

    # noinspection PyAttributeOutsideInit
    @cmd.setter
    def cmd(self, new_cmd: IOCBCMD) -> None:
        if new_cmd in (IOCBCMD.FDSYNC, IOCBCMD.FSYNC, IOCBCMD.NOOP, IOCBCMD.POLL):
            self.buffer = None
            self.offset = 0
            self.length = 0

        self._iocb.aio_lio_opcode = new_cmd

    @property
    def fd(self) -> int:
        return self._iocb.aio_fildes

    @fd.setter
    def fd(self, new_fd: int) -> None:
        self._iocb.aio_fildes = new_fd

    @property
    def offset(self) -> int:
        return self._iocb.aio_offset

    @offset.setter
    def offset(self, new_offset: int) -> None:
        self._iocb.aio_offset = new_offset

    @property
    def length(self) -> int:
        return self._iocb.aio_nbytes

    @length.setter
    def length(self, new_len: int) -> None:
        # TODO: check buffer length
        self._iocb.aio_nbytes = new_len

    @property
    def rw_flag(self) -> int:
        return self._iocb.aio_rw_flags

    @rw_flag.setter
    def rw_flag(self, new_flag: int) -> None:
        self._iocb.aio_rw_flags = new_flag

    @property
    def flag(self) -> int:
        return self._iocb.aio_flags

    @flag.setter
    def flag(self, new_flag: int) -> None:
        self._iocb.aio_flags = new_flag

    @property
    def res_fd(self) -> int or None:
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
