import unittest
from nrc.util.transformers import ListToScikitLearnTransformer
import numpy as np
from nrc.util.window import TrainTestWindow

def generate_data():
    return({'f1':2.4, 'f2':35}, 0)


class TransformerTests(unittest.TestCase):
    def test_list_sample_transform(self):
        print(f'\nExecuting {TransformerTests.test_list_sample_transform.__name__} test')
        ttw = TrainTestWindow(2, 1)
        ttw.add_one_sample({'f1':0.1}, 2)
        ttw.add_one_sample({'f1':0.2}, 5)

        transformer = ListToScikitLearnTransformer()
        transformer.samples = ttw.train_samples
        transformer.execute()

        print('Transformed x values')
        print(transformer.transformed_data['x'])
        print('Transformed y values')
        print(transformer.transformed_data['y'])

        self.assertTrue(isinstance(transformer.transformed_data['x'], np.ndarray))
        self.assertTrue(isinstance(transformer.transformed_data['y'], np.ndarray))
        self.assertTrue(np.allclose(np.array([[0.1],[0.2]]), transformer.transformed_data['x'], equal_nan=True))


if __name__ == '__main__':
    unittest.main()
