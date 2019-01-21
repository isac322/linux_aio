# coding: UTF-8

from .aio import IOEvent, Timespec, aio_context_t, io_cancel, io_destroy, io_getevents, io_setup, io_submit, iocb_p
from .iocb import IOCB, IOCBCMD, IOCBFlag, IOCBPriorityClass, IOCBRWFlag, IOPRIO_CLASS_SHIFT, IOVec, gen_io_priority


def create_c_array(c_type, elements, length: int = None):
    elements_tup = tuple(elements)
    if length is None:
        length = len(elements_tup)
    return (c_type * length)(*elements_tup)
