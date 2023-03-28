import unittest
from fluire.util.scalers import StandardScaler, RiverStandardScalerWrapper
import random
import pandas as pd
import numpy as np

class TestStandardScaler(unittest.TestCase):
    def test_standard_scaler_happy_path(self):
        std_scaler = StandardScaler()
        random.seed(42)
        samples = [{'f1': random.uniform(8, 12), 'f2': random.uniform(8, 12)} for _ in range(6)]
        print()
        print()
        print('Show the generated, un-scaled data : ')
        for sample in samples:
            print(sample)

        expected_scaled_values = [
            {'f1': 0.0, 'f2': 0.0},
            {'f1': 0.0, 'f2': 0.0},
            {'f1': 2.1674653620877917, 'f2': 7.885757405502203},
            {'f1': 2.273204997584291, 'f2': -1.0050641759219596},
            {'f1': -1.1701833155935442, 'f2': -1.072790042283996},
            {'f1': -2.0742915071321235, 'f2': 1.4669931232249165}
       ]

        actual_scaled_values = []

        print('Show and collect the scaled sample data :')
        for sample in samples:
            scaled = std_scaler.add_sample(sample)
            print(scaled)
            actual_scaled_values.append(scaled)

        # Make sure the expected and actual values are the same.
        for item in list(zip(expected_scaled_values, actual_scaled_values)):
            # Compare expected and actual dictionaries values one by one
            self.assertDictEqual(item[0], item[1])

    def test_riv_standard_scaler_wrapper_happy_path(self):
        r_std_scaler = RiverStandardScalerWrapper()
        random.seed(42)
        samples = [{'f1': random.uniform(8, 12), 'f2': random.uniform(8, 12)} for _ in range(6)]
        print()
        print()
        print('Show the generated, un-scaled data : ')
        for sample in samples:
            print(sample)

        expected_scaled_values = [
            {'f1': 0.0, 'f2': 0.0},
            {'f1': -0.999, 'f2': 0.999},
            {'f1': 0.937, 'f2': 1.350},
            {'f1': 1.129, 'f2': -0.651},
            {'f1': -0.776, 'f2': -0.729},
            {'f1': -1.274, 'f2': 0.992}
       ]

        actual_scaled_values = []

        print('Show and collect the scaled sample data :')
        for sample in samples:
            scaled = r_std_scaler.add_sample(sample)
            print(scaled)
            actual_scaled_values.append(scaled)

        # Make sure the expected and actual values are the same.
        for item in list(zip(expected_scaled_values, actual_scaled_values)):
            # Compare expected and actual dictionaries values one by one
            a = pd.Series(item[0])
            b = pd.Series(item[1])
            # 3 decimal tolerance when doing comparison
            self.assertTrue(np.allclose(a, b, rtol=1e-3, atol=1e-3))


if __name__ == "__main__":
    unittest.main()
