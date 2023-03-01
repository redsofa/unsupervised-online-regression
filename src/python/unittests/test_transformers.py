import unittest
from nrc.util.transformers import XYTransformers 
import numpy as np
from nrc.util.window import TrainTestWindow


class TransformerTests(unittest.TestCase):
    def test_sample_transforms(self):
        print(f'\nExecuting {TransformerTests.test_sample_transforms.__name__} test')
        # Create train/test window
        ttw = TrainTestWindow(2, 1)
        # Add one sample
        x = {'f1':0.1}
        y = 2
        sample = XYTransformers.xy_to_numpy_dictionary(x, y)
        # Add second sample
        ttw.add_one_sample(sample)
        x = {'f1':0.2}
        y = 5
        sample = XYTransformers.xy_to_numpy_dictionary(x, y)
        ttw.add_one_sample(sample)

        #transform the training data inside the train/test window 
        transformed_x, transformed_y = XYTransformers.arr_dict_to_xy(ttw.train_samples)
        
        #make sure the transformed data is as we expected
        self.assertTrue(np.allclose(np.array([[0.1],[0.2]]), transformed_x, equal_nan=True))
        self.assertTrue(np.allclose(np.array([[2],[5]]), transformed_y, equal_nan=True))


if __name__ == '__main__':
    unittest.main()
