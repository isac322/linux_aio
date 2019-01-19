# coding: UTF-8

import errno
import unittest

from linux_aio import AIOContext


class TestContext(unittest.TestCase):
    def test_ctx_setup_with_ctxmgr(self):
        with AIOContext(2) as ctx:
            pass

        self.assertTrue(ctx.closed)

    def test_double_close_with_ctxmgr(self):
        with AIOContext(2) as ctx:
            ctx.close()

        self.assertTrue(ctx.closed)

    def test_ctx_setup(self):
        ctx = AIOContext(2)
        ctx.close()

        self.assertTrue(ctx.closed)

    def test_double_close(self):
        ctx = AIOContext(2)
        ctx.close()
        ctx.close()

        self.assertTrue(ctx.closed)

    def test_exceed_max_nr(self):
        with open('/proc/sys/fs/aio-max-nr') as fp:
            max_nr = int(fp.read())

        with self.assertRaises(OSError) as assertion:
            with AIOContext(max_nr + 1) as ctx:
                pass

        self.assertEqual(errno.EAGAIN, assertion.exception.errno)

    def test_empty_submit(self):
        with AIOContext(2) as ctx:
            ret = ctx.submit()
            self.assertEqual(0, ret)

        self.assertTrue(ctx.closed)

    def test_empty_getevents(self):
        with AIOContext(2) as ctx:
            ret = ctx.get_events(0, 100)
            self.assertTupleEqual(tuple(), ret)

        self.assertTrue(ctx.closed)

    def test_empty_submit_n_getevents(self):
        with AIOContext(2) as ctx:
            submit_ret = ctx.submit()
            self.assertEqual(0, submit_ret)

            events_ret = ctx.get_events(0, 100)
            self.assertTupleEqual(tuple(), events_ret)

        self.assertTrue(ctx.closed)


if __name__ == '__main__':
    unittest.main()
