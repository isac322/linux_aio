# coding: UTF-8

from ctypes import Structure, c_int64, c_long, c_uint, c_uint64, c_ulong, pointer
from typing import Optional, Type, Union

from .iocb import IOCB

__all__ = (
    'Timespec', 'IOEvent', 'aio_context_t', 'iocb_p', 'io_setup', 'io_destroy', 'io_submit', 'io_getevents', 'io_cancel'
)


# noinspection PyMissingConstructor
class Timespec(Structure):
    tv_sec: Union[c_long, int]
    tv_nsec: Union[c_long, int]

    def __init__(self, tv_sev: Union[c_long, int] = 0, tv_nsec: Union[c_long, int] = 0) -> None: ...


# noinspection PyMissingConstructor
class IOEvent(Structure):
    data: Union[c_uint64, int]
    obj: Union[c_uint64, int]
    res: Union[c_int64, int]
    res2: Union[c_int64, int]

    def __init__(self, data: Union[c_uint64, int] = 0, obj: Union[c_uint64, int] = 0,
                 res: Union[c_int64, int] = 0, res2: Union[c_int64, int] = 0) -> None: ...


aio_context_t: Type[c_ulong] = ...
aio_context_t_p: Type[pointer[aio_context_t]] = ...
iocb_p: Type[pointer[IOCB]] = ...
iocb_pp: Type[pointer[iocb_p]] = ...
io_event_p: Type[pointer[IOEvent]] = ...
timespec_p: Type[pointer[Timespec]] = ...


def io_setup(max_jobs: c_uint, context_p: aio_context_t_p) -> None: ...


def io_destroy(context: aio_context_t) -> None: ...


def io_submit(context: aio_context_t, num_jobs: c_long, iocb_p_list: iocb_pp) -> int: ...


def io_getevents(context: aio_context_t, min_jobs: c_long, max_jobs: c_long,
                 events: io_event_p, timeout: Optional[timespec_p]) -> int: ...


def io_cancel(context: aio_context_t, iocb: iocb_p, result: io_event_p) -> None: ...
