import unittest
from fluire.util.transformers import XYTransformers
from fluire.util.window import Window
import numpy as np


class TransformerTests(unittest.TestCase):
    def test_sample_transforms(self):
        print(f'\nExecuting {TransformerTests.test_sample_transforms.__name__} test')
        # Create window
        w = Window(max_len=5, slides=False)
        # Add one sample
        x = {'f1': 0.1}
        y = 2
        sample = XYTransformers.xy_to_numpy_dictionary(x, y)
        # Add second sample
        w.add_data(sample)
        x = {'f1': 0.2}
        y = 5
        sample = XYTransformers.xy_to_numpy_dictionary(x, y)
        w.add_data(sample)

        # Transform the training data inside the train/test window
        transformed_x, transformed_y = XYTransformers.arr_dict_to_xy(w.get_as_list())

        # Make sure the transformed data is as we expected
        self.assertTrue(np.allclose(np.array([[0.1], [0.2]]), transformed_x, equal_nan=True))
        self.assertTrue(np.allclose(np.array([[2], [5]]), transformed_y, equal_nan=True))


if __name__ == '__main__':
    unittest.main()
