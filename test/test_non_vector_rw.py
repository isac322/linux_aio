# coding: UTF-8

import unittest

import os
from linux_aio_bind import IOCBPriorityClass, IOCBRWFlag

from linux_aio import AIOContext, ReadBlock, WriteBlock


class TestRW(unittest.TestCase):
    _content = 'content\n'
    _TEST_FILE_NAME = 'test.txt'

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        os.remove('test.txt')

    def test_01_write_bytes(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME, 'w') as fp:
            block = WriteBlock(fp, self._content.encode())

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._content.encode(), event.buffer)
            self.assertEqual(block, event.aio_block)
            self.assertEqual(len(self._content), event.response)
            self.assertEqual(0, event.response2)

    def test_02_read(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME) as fp:
            block = ReadBlock(fp, bytearray(64))

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._content.encode(), event.buffer.rstrip(b'\0'))
            self.assertEqual(self._content.encode(), event.stripped_buffer())
            self.assertEqual(block, event.aio_block)
            self.assertEqual(len(self._content), event.response)
            self.assertEqual(0, event.response2)

    def test_02_read_w_non_zero_offset(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME) as fp:
            block = ReadBlock(fp, bytearray(64))
            block.offset = 1
            self.assertEqual(1, block.offset)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._content.encode()[1:], event.buffer.rstrip(b'\0'))
            self.assertEqual(self._content.encode()[1:], event.stripped_buffer())
            self.assertEqual(block, event.aio_block)
            self.assertEqual(len(self._content) - 1, event.response)
            self.assertEqual(0, event.response2)

    def test_02_read_replace_file(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME) as fp:
            block = ReadBlock(fp, bytearray(64))
            block.file = fp.fileno()

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._content.encode(), event.buffer.rstrip(b'\0'))
            self.assertEqual(self._content.encode(), event.stripped_buffer())
            self.assertEqual(block, event.aio_block)
            self.assertEqual(len(self._content), event.response)
            self.assertEqual(0, event.response2)

    def test_02_read_w_rw_flags(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME) as fp:
            block = ReadBlock(fp, bytearray(64))
            block.rw_flag |= IOCBRWFlag.HIPRI

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._content.encode(), event.buffer.rstrip(b'\0'))
            self.assertEqual(self._content.encode(), event.stripped_buffer())
            self.assertEqual(block, event.aio_block)
            self.assertEqual(len(self._content), event.response)
            self.assertEqual(0, event.response2)

    def test_02_read_w_io_priority(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME) as fp:
            block = ReadBlock(fp, bytearray(64), priority_class=IOCBPriorityClass.RT, priority_value=1)
            self.assertEqual(IOCBPriorityClass.RT, block.priority_class)
            self.assertEqual(1, block.priority_value)
            block.set_priority(IOCBPriorityClass.IDLE, 2)
            self.assertEqual(IOCBPriorityClass.IDLE, block.priority_class)
            self.assertEqual(2, block.priority_value)
            block.priority_value = 3
            block.priority_class = IOCBPriorityClass.BE
            self.assertEqual(IOCBPriorityClass.BE, block.priority_class)
            self.assertEqual(3, block.priority_value)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._content.encode(), event.buffer.rstrip(b'\0'))
            self.assertEqual(self._content.encode(), event.stripped_buffer())
            self.assertEqual(block, event.aio_block)
            self.assertEqual(len(self._content), event.response)
            self.assertEqual(0, event.response2)

    def test_02_read_2_str(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME) as fp:
            buffer = 'buffer__'
            block = ReadBlock(fp, buffer)
            block.length = len(buffer)
            self.assertEqual(len(buffer), block.length)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._content.encode(), event.buffer.rstrip(b'\0'))
            self.assertEqual(self._content.encode(), event.stripped_buffer())
            self.assertEqual(block, event.aio_block)
            self.assertEqual(len(self._content), event.response)
            self.assertEqual(0, event.response2)

    def test_write_n_read(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME, 'w+') as fp:
            write_block = WriteBlock(fp, self._content)

            submit_ret = ctx.submit(write_block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._content.encode(), event.buffer)
            self.assertEqual(write_block, event.aio_block)
            self.assertEqual(len(self._content), event.response)
            self.assertEqual(0, event.response2)

            read_block = ReadBlock(fp, bytearray(64))

            submit_ret = ctx.submit(read_block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._content.encode(), event.buffer.rstrip(b'\0'))
            self.assertEqual(self._content.encode(), event.stripped_buffer())
            self.assertEqual(read_block, event.aio_block)
            self.assertEqual(len(self._content), event.response)
            self.assertEqual(0, event.response2)

    def test_2write_n_read(self):
        _SECOND_CONTENT = 'another\ninput'

        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME, 'w+') as fp:
            write_block1 = WriteBlock(fp, self._content)
            write_block2 = WriteBlock(fp, _SECOND_CONTENT)

            submit_ret = ctx.submit(write_block1, write_block2)
            self.assertEqual(2, submit_ret)

            events = ctx.get_events(2, 2)
            self.assertEqual(2, len(events))

            event = events[0]
            self.assertEqual(self._content.encode(), event.buffer)
            self.assertEqual(write_block1, event.aio_block)
            self.assertEqual(len(self._content), event.response)
            self.assertEqual(0, event.response2)

            read_block = ReadBlock(fp, bytearray(64))

            submit_ret = ctx.submit(read_block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(_SECOND_CONTENT.encode(), event.buffer.rstrip(b'\0'))
            self.assertEqual(_SECOND_CONTENT.encode(), event.stripped_buffer())
            self.assertEqual(read_block, event.aio_block)
            self.assertEqual(len(_SECOND_CONTENT), event.response)
            self.assertEqual(0, event.response2)
