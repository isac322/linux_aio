# coding: UTF-8

import select
import socket
import unittest

from linux_aio import AIOContext, FDsyncBlock, FsyncBlock, PollBlock


class TestNonRW(unittest.TestCase):
    def test_poll(self):
        with AIOContext(2) as ctx, \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            host_ip = socket.gethostbyname('www.google.com')
            sock.connect((host_ip, 80))
            sock.sendall('GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n'.encode())

            block = PollBlock(sock, select.EPOLLIN)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events_ret = ctx.get_events(1, 1)
            self.assertEqual(1, len(events_ret))
            self.assertIsNone(events_ret[0].buffer)
            self.assertIsNone(events_ret[0].stripped_buffer())
            # TODO
            # self.assertTupleEqual(tuple(), events_ret)

        self.assertTrue(ctx.closed)

    def test_poll_modify_masks(self):
        with AIOContext(2) as ctx, \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            host_ip = socket.gethostbyname('www.google.com')
            sock.connect((host_ip, 80))
            sock.sendall('GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n'.encode())

            block = PollBlock(sock, select.EPOLLIN)
            block.event_masks |= select.EPOLLOUT
            self.assertEqual(select.EPOLLOUT | select.EPOLLIN, block.event_masks)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events_ret = ctx.get_events(1, 1)
            self.assertEqual(1, len(events_ret))
            self.assertIsNone(events_ret[0].buffer)
            self.assertIsNone(events_ret[0].stripped_buffer())
            # TODO
            # self.assertTupleEqual(tuple(), events_ret)

        self.assertTrue(ctx.closed)

    def test_fsync(self):
        with AIOContext(2) as ctx, open('test.txt', 'w') as fp:
            fp.write('content\n')

            block = FsyncBlock(fp)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events_ret = ctx.get_events(1, 1)
            self.assertEqual(1, len(events_ret))
            self.assertIsNone(events_ret[0].buffer)
            self.assertIsNone(events_ret[0].stripped_buffer())
            self.assertEqual(0, events_ret[0].response)
            self.assertEqual(0, events_ret[0].response2)

    def test_fdsync(self):
        with AIOContext(2) as ctx, open('test.txt', 'w') as fp:
            fp.write('content\n')

            block = FDsyncBlock(fp)

            submit_ret = ctx.submit(block)
            self.assertEqual(1, submit_ret)

            events_ret = ctx.get_events(1, 1)
            self.assertEqual(1, len(events_ret))
            self.assertIsNone(events_ret[0].buffer)
            self.assertIsNone(events_ret[0].stripped_buffer())
            self.assertEqual(0, events_ret[0].response)
            self.assertEqual(0, events_ret[0].response2)


if __name__ == '__main__':
    unittest.main()
