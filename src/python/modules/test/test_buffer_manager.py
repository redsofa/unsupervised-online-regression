import unittest
from nrc.util.buffers import *

class TestBuffermanager(unittest.TestCase):
    def test_init_buffer_manager(self):
        bm = BufferManager(10, 5, 10)
        bm.add_one(10, 23)
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
