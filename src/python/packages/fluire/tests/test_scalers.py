import unittest
from common_test_utils import get_test_data_stream
from fluire.util.scalers import StandardScaler
import random


class TestStandardScaler(unittest.TestCase):
    def test_happy_path(self):
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
            {'f1': 0.0, 'f2': 0.0},
            {'f1': 2.3686343349945287, 'f2': -2.2641467845950727},
            {'f1': -1.0649675839972408, 'f2': -1.5623987634087035},
            {'f1': -1.9051024652950495, 'f2': 1.2547081423640767}
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


if __name__ == "__main__":
    unittest.main()
