import unittest
from nrc.metrics.regression import RegressionMetrics


class TestRegressionMetrics(unittest.TestCase):
    def test_add_to_metrics(self):
        # Create the regression metrics object
        m = RegressionMetrics()
        # Add a few y_true and y_pred values
        m.add_one_prediction(2, 23)
        m.add_one_prediction(4, 2)
        # Get the various metrics out of the object.
        self.assertAlmostEqual(11.500000, m.mae, places=6)
        self.assertAlmostEqual(222.500000, m.mse, places=6)
        self.assertAlmostEqual(14.916434, m.rmse, places=6)
        self.assertAlmostEqual(-221.500000, m.r2, places=6)


if __name__ == '__main__':
    unittest.main()
