# coding: UTF-8

from cffi import FFI

__all__ = ()

_ffibuilder = FFI()

_ffibuilder.set_source(
        'linux_aio.raw._syscall',
        r'#include <sys/syscall.h>'
)

_ffibuilder.cdef(r'''
    #define SYS_io_setup ...
    #define SYS_io_destroy ...
    #define SYS_io_getevents ...
    #define SYS_io_submit ...
    #define SYS_io_cancel ...
    // #define SYS_io_pgetevents ...
''')
