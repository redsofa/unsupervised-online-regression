import unittest
from fluire.util.window import Window


class TestWindow(unittest.TestCase):

    def test_window_no_slide_init_and_empty(self):
        w = Window(max_len=5, slides=False)
        self.assertEqual(0, w.len)
        for n in [1, 2, 3, 4, 5]:
            w.add_data(n)
            self.assertEqual(n, w.len)

        # Try to get an element that is out of range. This should
        # fail with the proper exception.
        with self.assertRaises(Exception) as ex:
            w.get_element_at(43)

        self.assertEqual(
                'Element index out of range.',
                str(ex.exception)
        )

        # Try to add new data to a full and non-sliding window.
        # This should fail with the proper exception.
        with self.assertRaises(Exception) as ex:
            w.add_data(100)

        self.assertEqual(
                'End of Window reached. Not a sliding window.',
                str(ex.exception)
        )
        self.assertTrue(w.is_full)

        # Clear the window and make sure the length is 0.
        w.clear_contents()
        self.assertEqual(0, w.len)
        # Add one element and make sure the length of the window is
        # now 1
        w.add_data(100)
        self.assertEqual(1, w.len)

        # Make sure that the window is not full
        self.assertFalse(w.is_full)

    def test_sliding_window_init_and_empty(self):
        # Create a sliding window of size 5
        w = Window(max_len=5, slides=True)
        # Make sure the length is 0 after initialization
        self.assertEqual(0, w.len)

        # Add numbers 1 to 5 in the sliding window and
        # make sure the length of the window grows accordingly.
        # Note that we are adding integers in the window but
        # it could be really any kind of type that we add to the queue.
        for n in [1, 2, 3, 4, 5]:
            w.add_data(n)
            self.assertEqual(n, w.len)

        # Clear the window and make sure the length is 0.
        w.clear_contents()
        self.assertEqual(0, w.len)

        # Add the numbers 1 to 10 and make sure the sliding window's
        # size is still 5 at the end of it.
        for n in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            w.add_data(n)
        self.assertEqual(5, w.len)

        self.assertTrue(w.is_full)

        self.assertEqual([6, 7, 8, 9, 10], w.get_as_list())
        self.assertEqual(10, w.get_element_at(4))

        with self.assertRaises(Exception):
            w.get_element_at(43)

        # Pull data from the sliding window.
        # The oldest bit of data should come out first (e.g. 6, 7, 8, 9, 10)
        for n in [6, 7, 8, 9, 10]:
            data = w.get_and_remove_oldest()
            self.assertEqual(n, data)

        # Length of window should be 0 after we've pulled everything out from it.
        self.assertEqual(0, w.len)


if __name__ == '__main__':
    unittest.main()
