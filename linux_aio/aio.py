# coding: UTF-8

import os
import sys
from ctypes import (
    CDLL, POINTER, Structure, c_int, c_int16, c_int64, c_long, c_uint, c_uint16, c_uint32, c_uint64, c_ulong, sizeof
)
from ctypes.util import find_library
from enum import IntEnum

# syscall numbers FIXME: dynamic way

__NR_io_setup = 206
__NR_io_destroy = 207
__NR_io_getevents = 208
__NR_io_submit = 209
__NR_io_cancel = 210

_libc = CDLL(find_library('c'), use_errno=True)
_syscall = _libc.syscall


# Define the types we need.
class CtypesEnum(IntEnum):
    """A ctypes-compatible IntEnum superclass."""

    @classmethod
    def from_param(cls, obj) -> int:
        return int(obj)


class Timespec(Structure):
    _fields_ = (
        ('tv_sec', c_long),
        ('tv_nsec', c_long),
    )


class IOEvent(Structure):
    _fields_ = (
        ('data', c_uint64),
        ('obj', c_uint64),
        ('res', c_int64),
        ('res2', c_int64),
    )


PADDED = {
    (4, 'little'): lambda w, x, y: [(x, w), (y, c_uint)],
    (8, 'little'): lambda w, x, y: [(x, w), (y, w)],
    (8, 'big'): lambda w, x, y: [(y, c_uint), (x, w)],
    (4, 'big'): lambda w, x, y: [(y, c_uint), (x, w)],
}[(sizeof(c_ulong), sys.byteorder)]


class IOCB(Structure):
    _fields_ = (
        # internal fields used by the kernel
        ('aio_data', c_uint64),
        *PADDED(c_uint32, 'aio_key', 'aio_rw_flags'),

        # common fields
        ('aio_lio_opcode', c_uint16),
        ('aio_reqprio', c_int16),
        ('aio_fildes', c_uint32),

        ('aio_buf', c_uint64),
        ('aio_nbytes', c_uint64),
        ('aio_offset', c_int64),

        # extra parameters
        ('aio_reserved2', c_uint64),

        # flags for IOCB
        ('aio_flags', c_uint32),

        # if the IOCB_FLAG_RESFD flag of "aio_flags" is set, this is an eventfd to signal AIO readiness to
        ('aio_resfd', c_uint32),
    )


class IOCBCMD(CtypesEnum):
    PREAD = 0
    PWRITE = 1
    FSYNC = 2
    FDSYNC = 3
    # These two are experimental.
    # PREADX = 4
    POLL = 5
    NOOP = 6
    PREADV = 7
    PWRITEV = 8


class IOCBFlag(CtypesEnum):
    """ flags for :attr:`IOCB.aio_flags` """
    IOCB_FLAG_RESFD = 1 << 0
    IOCB_FLAG_IOPRIO = 1 << 1


class IOCBRWFlag(CtypesEnum):
    """ flags for :attr:`IOCB.aio_rw_flags` """
    RWF_HIPRI = 1 << 0 if sys.version_info < (3, 7) else os.RWF_HIPRI
    RWF_DSYNC = 1 << 1 if sys.version_info < (3, 7) else os.RWF_DSYNC
    RWF_SYNC = 1 << 2 if sys.version_info < (3, 7) else os.RWF_SYNC
    RWF_NOWAIT = 1 << 3 if sys.version_info < (3, 7) else os.RWF_NOWAIT
    RWF_APPEND = 1 << 4


aio_context_t = c_ulong
aio_context_t_p = POINTER(aio_context_t)
iocb_p = POINTER(IOCB)
iocb_pp = POINTER(iocb_p)
io_event_p = POINTER(IOEvent)
timespec_p = POINTER(Timespec)


def io_setup(max_jobs: c_uint, context_p: aio_context_t_p) -> c_int:
    return _syscall(__NR_io_setup, max_jobs, context_p)


def io_destroy(context: aio_context_t) -> c_int:
    return _syscall(__NR_io_destroy, context)


def io_submit(context: aio_context_t, num_jobs: c_long, iocb_p_list: iocb_pp) -> c_int:
    return _syscall(__NR_io_submit, context, num_jobs, iocb_p_list)


def io_getevents(context: aio_context_t, min_jobs: c_long, max_jobs: c_long,
                 events: io_event_p, timeout: timespec_p) -> c_int:
    return _syscall(__NR_io_getevents, context, min_jobs, max_jobs, events, timeout)


def io_cancel(context: aio_context_t, iocb: iocb_p, result: io_event_p) -> c_int:
    return _syscall(__NR_io_cancel, context, iocb, result)
