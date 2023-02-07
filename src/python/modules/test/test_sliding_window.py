import unittest
from nrc.util.buffers import *


class TestSlidingWidow(unittest.TestCase):
    def test_window_init_and_empty(self):
        # Create a sliding window of size 5
        w = SlidingWindow(5)
        # Make sure the length is 0 after initialization
        self.assertEqual(0, w.len())

        # Add numbers 1 to 5 in the sliding window and
        # make sure the length of the window grows accordingly.
        # Note that we are adding integers in the window but
        # it could be really any kind of type that we add to the queue.
        for n in [1, 2, 3, 4, 5]:
            w.add_data(n)
            self.assertEqual(n, w.len())

        # Clear the window and make sure the length is 0.
        w.clear_contents()
        self.assertEqual(0, w.len())

        # Add the numbers 1 to 10 and make sure the sliding window's
        # size is still 5 at the end of it.
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            w.add_data(n)
        self.assertEqual(5, w.len())

        # Pull data from the sliding window.
        # The oldest bit of data should come out first (e.g. 6, 7, 8, 9, 10)
        for n in [6, 7, 8, 9, 10]:
            data = w.get_data()
            self.assertEqual(n, data)

        # Length of window should be 0 after we've pulled everything out from it.
        self.assertEqual(0, w.len())


if __name__ == '__main__':
    unittest.main()
