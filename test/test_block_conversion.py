# coding: UTF-8

import errno
import unittest

import os
import platform
from linux_aio_bind import IOCBCMD

from linux_aio import AIOContext, FDsyncBlock, FsyncBlock, ReadBlock, WriteBlock

_linux_ver = tuple(map(int, platform.uname().release.split('-')[0].split('.')))


class TestBlockConversion(unittest.TestCase):
    _CONTENTS = 'contents\n'

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        os.remove('test.txt')

    def setUp(self) -> None:
        super().setUp()

        with open('test.txt', 'w') as fp:
            fp.write(self._CONTENTS)

    def test_conversion_err_read_2_fsync(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a+') as fp, AIOContext(1) as ctx:
                block = ReadBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.FSYNC)

                ctx.submit(block)

    def test_conversion_err_read_2_fdsync(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a+') as fp, AIOContext(1) as ctx:
                block = ReadBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.FDSYNC)

                ctx.submit(block)

    def test_conversion_err_read_2_poll(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a+') as fp, AIOContext(1) as ctx:
                block = ReadBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.POLL)

                ctx.submit(block)

    def test_conversion_err_read_2_readv(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a+') as fp, AIOContext(1) as ctx:
                block = ReadBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.PREADV)

                ctx.submit(block)

    def test_conversion_err_read_2_write(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a+') as fp, AIOContext(1) as ctx:
                block = ReadBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.PWRITE)

                ctx.submit(block)

    def test_conversion_err_read_2_writev(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a+') as fp, AIOContext(1) as ctx:
                block = ReadBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.PWRITEV)

                ctx.submit(block)

    def test_conversion_err_write_2_fsync(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a') as fp, AIOContext(1) as ctx:
                block = WriteBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.FSYNC)

                ctx.submit(block)

    def test_conversion_err_write_2_fdsync(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a') as fp, AIOContext(1) as ctx:
                block = WriteBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.FDSYNC)

                ctx.submit(block)

    def test_conversion_err_write_2_poll(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a') as fp, AIOContext(1) as ctx:
                block = WriteBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.POLL)

                ctx.submit(block)

    def test_conversion_err_write_2_read(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a') as fp, AIOContext(1) as ctx:
                block = WriteBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.PREAD)

                ctx.submit(block)

    def test_conversion_err_write_2_readv(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a') as fp, AIOContext(1) as ctx:
                block = WriteBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.PREADV)

                ctx.submit(block)

    def test_conversion_err_write_2_writev(self):
        with self.assertRaises(ValueError):
            with open('test.txt', 'a') as fp, AIOContext(1) as ctx:
                block = WriteBlock(fp, bytes())

                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)

                block.change_cmd(IOCBCMD.PWRITEV)

                ctx.submit(block)

    def test_convert_to_same_type(self):
        with open('test.txt', 'a') as fp, AIOContext(1) as ctx:
            block = WriteBlock(fp, bytes())

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            get_event_ret = ctx.get_events(1, 1)
            self.assertEqual(1, len(get_event_ret))
            self.assertEqual(block, get_event_ret[0].aio_block)

            block.change_cmd(IOCBCMD.PWRITE)
            self.assertEqual(fp.fileno(), block.fileno)
            self.assertEqual(fp, block.file)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            get_event_ret = ctx.get_events(1, 1)
            self.assertEqual(1, len(get_event_ret))
            self.assertEqual(block, get_event_ret[0].aio_block)

    def test_conversion_fsync_2_fdsync(self):
        with open('test.txt', 'a') as fp, AIOContext(1) as ctx:
            block = FsyncBlock(fp)

            try:
                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)
            except OSError as err:
                if _linux_ver >= (4, 18):
                    raise
                else:
                    self.assertEqual(errno.EINVAL, err.errno)

            block = block.change_cmd(IOCBCMD.FDSYNC)
            self.assertEqual(fp.fileno(), block.fileno)
            self.assertEqual(fp, block.file)

            try:
                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)
            except OSError as err:
                if _linux_ver >= (4, 18):
                    raise
                else:
                    self.assertEqual(errno.EINVAL, err.errno)

    def test_conversion_fdsync_2_fsync(self):
        with open('test.txt', 'a') as fp, AIOContext(1) as ctx:
            block = FsyncBlock(fp)

            try:
                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)
            except OSError as err:
                if _linux_ver >= (4, 18):
                    raise
                else:
                    self.assertEqual(errno.EINVAL, err.errno)

            block = block.change_cmd(IOCBCMD.FSYNC)
            self.assertEqual(fp.fileno(), block.fileno)
            self.assertEqual(fp, block.file)

            try:
                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)
            except OSError as err:
                if _linux_ver >= (4, 18):
                    raise
                else:
                    self.assertEqual(errno.EINVAL, err.errno)

    def test_conversion_fdsync_2_read(self):
        with open('test.txt', 'a+') as fp, AIOContext(1) as ctx:
            block = FDsyncBlock(fp)

            try:
                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)
            except OSError as err:
                if _linux_ver >= (4, 18):
                    raise
                else:
                    self.assertEqual(errno.EINVAL, err.errno)

            block = block.change_cmd(IOCBCMD.PREAD)
            self.assertEqual(fp.fileno(), block.fileno)
            self.assertEqual(fp, block.file)
            buf = bytearray(64)
            block.buffer = buf

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            get_event_ret = ctx.get_events(1, 1)
            self.assertEqual(1, len(get_event_ret))
            self.assertEqual(block, get_event_ret[0].aio_block)
            fp.seek(0)
            self.assertEqual(fp.read(len(buf)), get_event_ret[0].stripped_buffer().decode())

    def test_conversion_fdsync_2_write(self):
        with open('test.txt', 'a+') as fp, AIOContext(1) as ctx:
            block = FDsyncBlock(fp)

            try:
                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                get_event_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(get_event_ret))
                self.assertEqual(block, get_event_ret[0].aio_block)
            except OSError as err:
                if _linux_ver >= (4, 18):
                    raise
                else:
                    self.assertEqual(errno.EINVAL, err.errno)

            block = block.change_cmd(IOCBCMD.PWRITE)
            self.assertEqual(fp.fileno(), block.fileno)
            self.assertEqual(fp, block.file)
            content = 'content2'.encode()
            block.buffer = content

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            get_event_ret = ctx.get_events(1, 1)
            self.assertEqual(1, len(get_event_ret))
            self.assertEqual(block, get_event_ret[0].aio_block)
            self.assertEqual(fp.read(len(content)), get_event_ret[0].stripped_buffer().decode())
