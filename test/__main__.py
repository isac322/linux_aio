# coding: UTF-8

import unittest

# noinspection PyUnresolvedReferences
from .test_block import TestAIOBlock
# noinspection PyUnresolvedReferences
from .test_block_conversion import TestBlockConversion
# noinspection PyUnresolvedReferences
from .test_context import TestContext
# noinspection PyUnresolvedReferences
from .test_non_rw import TestNonRW
# noinspection PyUnresolvedReferences
from .test_non_vector_rw import TestRW
# noinspection PyUnresolvedReferences
from .test_vector_rw import TestVectorRW

if __name__ == '__main__':
    unittest.main()
