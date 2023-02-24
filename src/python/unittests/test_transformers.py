import unittest
from nrc.util.transformers import RiverToScikitLearnSampleTransformer
import numpy as np


def generate_data():
    return({'f1':2.4, 'f2':35}, 0)


class TestRiverToScikitLearnSampleTransformer(unittest.TestCase):
    def test_basic_sample_transform(self):
        print(f'\nExecuting {TestRiverToScikitLearnSampleTransformer.test_basic_sample_transform.__name__} test')
        river_data = generate_data()
        transformer = RiverToScikitLearnSampleTransformer()
        transformer.set_one_sample(river_data[0], river_data[1])
        transformer.execute()

        print('Transformed x values')
        print(transformer.transformed_data['x'])
        print('Transformed y values')
        print(transformer.transformed_data['y'])

        self.assertTrue(isinstance(transformer.transformed_data['x'], np.ndarray))
        self.assertTrue(isinstance(transformer.transformed_data['y'], np.ndarray))
        self.assertTrue(np.allclose(np.array([[2.4, 35]]), transformer.transformed_data['x'], equal_nan=True))
        self.assertTrue(np.allclose(np.array([[0]]), transformer.transformed_data['y'], equal_nan=True))

if __name__ == '__main__':
    unittest.main()
