import unittest
from common_test_utils import get_test_data_stream
from fluire.util.scalers import StandardScaler


class TestStandardScaler(unittest.TestCase):
    def test_happy_path(self):
        scaler = StandardScaler()
        # Configure a CSV stream instance of testing data
        data_stream = get_test_data_stream()
        for x, y in data_stream:
            print(f'adding ({x}, {y})')
            scaler.add_sample(x)
            x = scaler.standardized_sample
            print(f'Standardized data {x}')



if __name__ == "__main__":
    unittest.main()
