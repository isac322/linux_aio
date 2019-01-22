# coding: UTF-8

from ctypes import get_errno
from errno import EAGAIN, EBADF, EFAULT, EINTR, EINVAL, ENOMEM, ENOSYS, errorcode
from os import strerror
from typing import Dict, Mapping

setup_err_map = {  # type: Dict[int, str]
    EAGAIN:
        'The specified max_jobs (given: {0}) exceeds the user\'s limit of available events,'
        ' as defined in /proc/sys/fs/aio-max-nr (limit: {1}).',
    EFAULT:
        'Report to library author with message: "An invalid pointer is passed for context_p ({0})".',
    EINVAL:
        'The specified max_jobs (given: {0}) exceeds internal limits. max_jobs should be greater than 0. '
        'If this error persists, report to library author with message: '
        '"context_p is not initialized ({2}), max_jobs: {0}".',
    ENOMEM:
        'Insufficient kernel resources are available.',
    ENOSYS:
        'AIO is not implemented on this architecture.'
}
"""
0: max_jobs,

1: content of `/proc/sys/fs/aio-max-nr`,

2: :const:`~linux_aio.raw.aio.aio_context_t`
"""

destroy_err_map = {  # type: Dict[int, str]
    EFAULT: 'Report to library author with message: "The context pointed to is invalid ({0})."',
    EINVAL: 'Report to library author with message: "The AIO context specified by ctx_id is invalid ({0})."',
    ENOSYS: setup_err_map[ENOSYS]
}
"""
0: :const:`~linux_aio.raw.aio.aio_context_t`,
"""

cancel_err_map = {  # type: Dict[int, str]
    EAGAIN: 'The iocb specified was not canceled.',
    EFAULT: 'One of the data structures points to invalid data.',
    EINVAL: destroy_err_map[EINVAL],
    ENOSYS: setup_err_map[ENOSYS]
}
"""
0: :const:`~linux_aio.raw.aio.aio_context_t`,
"""

get_events_err_map = {  # type: Dict[int, str]
    EFAULT: 'timeout_ns is invalid. If not, report to library author with message: "events or timespec is invalid"',
    EINTR: 'Interrupted by a signal handler; see signal(7).',
    EINVAL: 'min_jobs ({1}) is out of range or max_jobs ({2}) is out of range. If not both, ' + destroy_err_map[EINVAL],
    ENOSYS: setup_err_map[ENOSYS]
}
"""
0: :const:`~linux_aio.raw.aio.aio_context_t`,

1: min_jobs,

2: max_jobs
"""

submit_err_map = {  # type: Dict[int, str]
    EAGAIN: 'Insufficient resources are available to queue any `AIOBlock`s.',
    EBADF: 'The file descriptor specified in the first `AIOBlock` is invalid.',
    EFAULT: 'One of the data structures points to invalid data.',
    EINVAL: 'Report to library author with message: "The AIO context specified by ctx_id ({0}) is invalid. '
            'nr is less than 0. The iocb at *iocbpp[0] is not properly initialized, '
            'or the operation specified is invalid for the file descriptor in the iocb."',
    ENOSYS: setup_err_map[ENOSYS]
}
"""
0: :const:`~linux_aio.raw.aio.aio_context_t`
"""


def handle_error(error_map: Mapping[int, str], *args) -> None:
    """
    .. versionadded:: 0.1.0
    """
    err = get_errno()  # type: int

    def_msg = '{}, {}.'.format(errorcode[err], strerror(err))

    if err in error_map:
        raise OSError(err, def_msg, error_map[err].format(*args))
    else:
        raise OSError(err, def_msg, 'This error is not an AIO related error.')
