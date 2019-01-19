# coding: UTF-8

import unittest

from linux_aio import AIOBlock, AIOContext, IOCBCMD


class TestRW(unittest.TestCase):
    _content_bytes = 'content\n'.encode()
    _TEST_FILE_NAME = 'test.txt'

    def test_01_write_bytes(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME, 'w') as fp:
            block = AIOBlock(fp.fileno(), IOCBCMD.PWRITE, self._content_bytes)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(self._content_bytes, event.buffer)
            self.assertEqual(block, event.aio_block)
            self.assertEqual(len(self._content_bytes), event.response)
            self.assertEqual(0, event.response2)

    def test_02_read(self):
        with AIOContext(1) as ctx, open(self._TEST_FILE_NAME) as fp:
            block = AIOBlock(fp.fileno(), IOCBCMD.PREAD, bytes(64))

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events = ctx.get_events(1, 1)
            self.assertEqual(1, len(events))

            event = events[0]
            self.assertEqual(event.buffer.rstrip(b'\0'), self._content_bytes)
            self.assertEqual(block, event.aio_block)
            self.assertEqual(len(self._content_bytes), event.response)
            self.assertEqual(0, event.response2)


if __name__ == '__main__':
    unittest.main()
