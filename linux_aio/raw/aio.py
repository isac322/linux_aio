# coding: UTF-8

from ctypes import CDLL, POINTER, Structure, c_int, c_int64, c_long, c_uint, c_uint64, c_ulong
from ctypes.util import find_library

from .iocb import IOCB
# noinspection PyUnresolvedReferences
from ._syscall import lib

__all__ = (
    'Timespec', 'IOEvent', 'aio_context_t', 'iocb_p', 'io_event_p',
    'io_setup', 'io_destroy', 'io_submit', 'io_getevents', 'io_cancel'
)

_libc = CDLL(find_library('c'), use_errno=True)
_syscall = _libc.syscall


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


aio_context_t = c_ulong
aio_context_t_p = POINTER(aio_context_t)
iocb_p = POINTER(IOCB)
iocb_pp = POINTER(iocb_p)
io_event_p = POINTER(IOEvent)
timespec_p = POINTER(Timespec)


def io_setup(max_jobs: c_uint, context_p: aio_context_t_p) -> c_int:
    return _syscall(lib.SYS_io_setup, max_jobs, context_p)


def io_destroy(context: aio_context_t) -> c_int:
    return _syscall(lib.SYS_io_destroy, context)


def io_submit(context: aio_context_t, num_jobs: c_long, iocb_p_list: iocb_pp) -> c_int:
    return _syscall(lib.SYS_io_submit, context, num_jobs, iocb_p_list)


def io_getevents(context: aio_context_t, min_jobs: c_long, max_jobs: c_long,
                 events: io_event_p, timeout: timespec_p) -> c_int:
    """
    return value can be less than min_jobs. because io_getevents can be interrupted by signal during processing
    (io_pgetevents does not, but not fully implemented)
    """
    return _syscall(lib.SYS_io_getevents, context, min_jobs, max_jobs, events, timeout)


def io_cancel(context: aio_context_t, iocb: iocb_p, result: io_event_p) -> c_int:
    return _syscall(lib.SYS_io_cancel, context, iocb, result)
