import sys
import unittest
from nrc.util.window import *
from nrc.metrics.regression import *
from nrc.util.transformers import ListToScikitLearnTransformer
import os
from common_test_utils import get_test_data_stream
import numpy as np
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score


# TODO : Test values properly and verify that metrics get added properly
class TestRegressionMetricsWindow(unittest.TestCase):
    def test_window_sizes(self):
        # Create a RegressionMetricsWinow
        rmw = RegressionMetricsWindow(2)
        # Create the regression metrics object
        m = RegressionMetrics()
        # Add a few y_true and y_pred values
        m.add_one_prediction(2,23)
        m.add_one_prediction(4,2)

        # Add metrics to the metrics window
        rmw.add_one_metric(m)

        m2 = RegressionMetrics()
        # Add a few y_true and y_pred values
        m2.add_one_prediction(2,23)
        m2.add_one_prediction(4,2)
        rmw.add_one_metric(m2)

        m3 = RegressionMetrics()
        # Add a few y_true and y_pred values
        m3.add_one_prediction(2,23)
        m3.add_one_prediction(4,2)
        rmw.add_one_metric(m3)

        self.assertEqual(2, rmw.len())


class TestTrainTestWindow(unittest.TestCase):
    def test_window_sizes(self):
        # Utility function to generate a River-like datapoint.
        def get_one_data_point(f1, f2, y):
            return ({'f1':f1, 'f2': f2}, y)

        # Window size configuration
        train_window_size = 4
        test_window_size = 2
        ttw_size = train_window_size + test_window_size

        # Create a TrainTestWindow instance
        ttw = TrainTestWindow(train_window_size, test_window_size)

        # Create and register event handler for when the TrainTestWindow is filled
        def on_window_filled():
            print('Window Filled')

        ttw.register_on_window_filled_handler(on_window_filled)

        # Add data a number of data points to the TrainTestWindow
        for i in [1, 2, 3, 4, 5, 6]:
            # The TrainTestWindow should not be full until we are out of this loop
            self.assertFalse(ttw.is_filled)
            (x, y) = get_one_data_point(i, i+1, i+2)
            ttw.add_one_sample(x, y)

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

    def test_train_regression_model(self):
        # Configure window size
        window_size = 10
        train_size = round(window_size * 0.8)
        test_size = round(window_size * 0.2)

        print(f'window_size : {window_size}')
        print(f'train_size : {train_size}')
        print(f'test_size : {test_size}')

        # Configure a CSV stream instance of testing data
        data_stream = get_test_data_stream()
        # Create instance of list data transformer
        transformer = ListToScikitLearnTransformer()
        # Configure a TrainTest_Window instance
        ttw = TrainTestWindow(train_size, test_size)
        # Pull data from stream until the TrainTestWindow is full
        for x, y  in data_stream:
            ttw.add_one_sample(x, y)
            if ttw.is_filled:
                break

        # Transform train samples
        transformer.set_samples(ttw.train_samples)
        transformer.transform()
        train_data = transformer.transformed_data
        print('train_data x : ')
        print(train_data['x'])
        print('train_data y : ')
        print(train_data['y'])
        # Make sure train and testing data look like we would expect
        self.assertEqual(train_size, len(train_data['x']))
        self.assertEqual(train_size, len(train_data['y']))
        expected_train_x = [
                [1.0,2.0],
                [2.2,3.5],
                [3.0,3.1],
                [2.0,3.1],
                [2.4,3.4],
                [2.0,3.1],
                [6.0,3.1],
                [2.0,3.1],
        ]
        expected_train_y = [23,22,21,20,22,24,26,22]
        self.assertTrue(np.allclose(np.array(expected_train_x), train_data['x'], equal_nan=True))
        self.assertTrue(np.allclose(np.array(expected_train_y), train_data['y'], equal_nan=True))

        # Transform test samples
        transformer.set_samples(ttw.test_samples)
        transformer.transform()
        test_data = transformer.transformed_data
        print('test_data x :')
        print(test_data['x'])
        print('test_data y :')
        print(test_data['y'])
        # Make sure test data looks like what we would expect
        self.assertEqual(test_size, len(test_data['x']))
        self.assertEqual(test_size, len(test_data['y']))

        expected_test_x = [
                [4.2, 3.1],
                [2.0, 3.5]
        ]
        expected_test_y = [22, 27]
        self.assertTrue(np.allclose(np.array(expected_test_x), test_data['x'], equal_nan=True))
        self.assertTrue(np.allclose(np.array(expected_test_y), test_data['y'], equal_nan=True))

        # Create regression model
        regr = linear_model.LinearRegression()
        regr.fit(train_data['x'], train_data['y'])

        preds = regr.predict(test_data['x'])
        print('predictions :')
        print(preds)
        print()

        # The coefficients
        print("Coefficients: \n", regr.coef_)
        # The mean squared error
        print("Mean squared error: %.2f" % mean_squared_error(test_data['y'], preds))
        # The coefficient of determination: 1 is perfect prediction
        print("Coefficient of determination: %.2f" % r2_score(test_data['y'], preds))
        print()

        # Make test fail... were not done testing yet...
        self.assertTrue(False)

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
