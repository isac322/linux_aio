# coding: UTF-8

import errno
import select
import unittest

import platform
import socket

from linux_aio import AIOContext, PollBlock

_linux_ver = tuple(map(int, platform.uname().release.split('-')[0].split('.')))


class TestAIOBlock(unittest.TestCase):
    def test_non_fileno_obj(self):
        with self.assertRaises(AttributeError) as assertion:
            PollBlock(assertion)

    def test_poll(self):
        with AIOContext(2) as ctx, \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            host_ip = socket.gethostbyname('www.google.com')
            sock.connect((host_ip, 80))
            sock.sendall('GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n'.encode())

            block = PollBlock(sock, select.EPOLLIN)

            try:
                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                events_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(events_ret))
                self.assertIsNone(events_ret[0].buffer)
                self.assertIsNone(events_ret[0].stripped_buffer())
                # TODO
                # self.assertTupleEqual(tuple(), events_ret)
            except OSError as err:
                if _linux_ver >= (4, 19):
                    raise
                else:
                    self.assertEqual(errno.EINVAL, err.errno)

        self.assertTrue(ctx.closed)

    def test_poll_wo_initial_masks(self):
        with AIOContext(2) as ctx, \
                socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            host_ip = socket.gethostbyname('www.google.com')
            sock.connect((host_ip, 80))
            sock.sendall('GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n'.encode())

            block = PollBlock(sock)

            try:
                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                events_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(events_ret))
                self.assertIsNone(events_ret[0].buffer)
                self.assertIsNone(events_ret[0].stripped_buffer())
                # TODO
                # self.assertTupleEqual(tuple(), events_ret)
            except OSError as err:
                if _linux_ver >= (4, 19):
                    raise
                else:
                    self.assertEqual(errno.EINVAL, err.errno)

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

            try:
                submit_ret = ctx.submit(block)
                self.assertEqual(1, submit_ret)

                events_ret = ctx.get_events(1, 1)
                self.assertEqual(1, len(events_ret))
                self.assertIsNone(events_ret[0].buffer)
                self.assertIsNone(events_ret[0].stripped_buffer())
                # TODO
                # self.assertTupleEqual(tuple(), events_ret)
            except OSError as err:
                if _linux_ver >= (4, 18):
                    raise
                else:
                    self.assertEqual(errno.EINVAL, err.errno)

        self.assertTrue(ctx.closed)
