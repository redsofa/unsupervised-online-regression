import unittest
from nrc.util.transformers import ListToScikitLearnTransformer, RiverToScikitLearnSampleTransformer
import numpy as np
from nrc.util.window import TrainTestWindow

def generate_data():
    return({'f1':2.4, 'f2':35}, 0)


class TransformerTests(unittest.TestCase):
    def test_basic_sample_transform(self):
        print(f'\nExecuting {TransformerTests.test_basic_sample_transform.__name__} test')
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

    def test_list_sample_transform(self):
        print(f'\nExecuting {TransformerTests.test_list_sample_transform.__name__} test')
        ttw = TrainTestWindow(2, 1)
        ttw.add_one_sample({'f1':0.1}, 2)
        ttw.add_one_sample({'f1':0.2}, 5)

        transformer = ListToScikitLearnTransformer()
        transformer.set_samples(ttw.train_samples)
        transformer.execute()
        print(transformer.transformed_data['x'])
        print(transformer.transformed_data['y'])


if __name__ == '__main__':
    unittest.main()
