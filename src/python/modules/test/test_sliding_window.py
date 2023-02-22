import unittest
from nrc.util.window import *


class TestTrainTestWindow(unittest.TestCase):
    def test_window_sizes(self):
        def get_one_data_point(f1, f2, y):
            return ({'f1':f1, 'f2': f2}, y)

        train_window_size = 4
        test_window_size = 2
        ttw_size = train_window_size + test_window_size

        # Create a TrainTestWindow instance
        ttw = TrainTestWindow(train_window_size, test_window_size)

        # Add data a number of data points to the TrainTestWindow
        for i in [1, 2, 3, 4, 5, 6]:
            print(f'Adding data_point number {i}')
            # The TrainTestWindow should not be full until we are out of this loop
            self.assertFalse(ttw.is_filled)
            (x, y) = get_one_data_point(i, i+1, i+2)
            ttw.add_one_sample(x = x, y = y)

        # The TrainTestWindow should not be full
        self.assertTrue(ttw.is_filled)

        # Print the training data.. and the testing data
        print(ttw.train_samples)
        print(ttw.test_samples)

        # Make sure the sizes of the windows are what we expect
        self.assertEqual(train_window_size, ttw.train_sample_count)
        self.assertEqual(test_window_size, ttw.test_sample_count)

        # We should get an exception if we try to add more data than
        # the TrainTestWindow is configured for
        with self.assertRaises(Exception):
            (x, y) = get_one_data_point(10, 11, 12)
            ttw.add_one_sample(x = x, y = y)


    def test_event_handlers(self):
        train_window_size = 5
        test_window_size = 3
        ttw = TrainTestWindow(train_window_size, test_window_size)
        # variable to simulate pass by reference
        r_var = [0]

        def on_add_sample(*args, **kwargs):
            v = kwargs['mutable_var']
            v[0] = 1
            print(f'New sample : x : {kwargs["x"]}, y : {kwargs["y"]}')

        ttw.register_on_add_sample_handler(on_add_sample)

        ttw.add_one_sample(x={'f1':0.1, 'f2':1.0}, y=2.0, mutable_var=r_var)

        self.assertEqual(1, r_var[0])
        self.assertEqual(1, ttw.train_sample_count)
        self.assertEqual(0, ttw.test_sample_count)
        first_train_sample = ttw.train_samples[0]
        self.assertEqual(first_train_sample['f1'], 0.1)
        self.assertEqual(first_train_sample['y'], 2.0)


class TestSlidingWindow(unittest.TestCase):
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

        self.assertEqual([6, 7, 8, 9, 10], w.get_as_list())
        self.assertEqual(10, w.get_element_at(4))

        with self.assertRaises(Exception):
            w.get_element_at(43)

        # Pull data from the sliding window.
        # The oldest bit of data should come out first (e.g. 6, 7, 8, 9, 10)
        for n in [6, 7, 8, 9, 10]:
            data = w.pop()
            self.assertEqual(n, data)

        # Length of window should be 0 after we've pulled everything out from it.
        self.assertEqual(0, w.len())


if __name__ == '__main__':
    unittest.main()
