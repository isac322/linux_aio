# coding: UTF-8

import unittest

import functools
import os

from linux_aio import AIOContext, ReadVBlock, WriteVBlock


class TestVectorRW(unittest.TestCase):
    _CONTENTS = 'content\n'
    _TEST_FILE_NAME = 'test.txt'

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        os.remove('test.txt')

    def setUp(self) -> None:
        super().setUp()

        with open(self._TEST_FILE_NAME, 'w') as fp:
            fp.write(self._CONTENTS)

    def test_readv(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME) as fp:
            buffers = (bytearray(4), bytearray(4))

            block = ReadVBlock(fp, buffers)
            new_buffers = (bytearray(4), bytearray(4))
            block.buffer = new_buffers
            self.assertTupleEqual(new_buffers, block.buffer)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._CONTENTS.encode(), functools.reduce(lambda a, b: a + b, event.buffer).rstrip(b'\0'))
            self.assertEqual(block, event.aio_block)
            self.assertEqual(len(self._CONTENTS), event.response)
            self.assertEqual(0, event.response2)

    def test_writev(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME, 'w+') as fp:
            buffers = ('cont'.encode(), 'ent\n'.encode())

            block = WriteVBlock(fp, buffers)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            fp.seek(0)
            self.assertEqual(self._CONTENTS, fp.read(sum(map(lambda x: len(x), buffers))))
            self.assertEqual(block, event.aio_block)
            self.assertEqual(sum(map(lambda x: len(x), buffers)), event.response)
            self.assertEqual(0, event.response2)
