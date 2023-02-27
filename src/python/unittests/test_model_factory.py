from nrc.factories.model import ModelFactory
from nrc.factories.stream import StreamFactory
from nrc.models.regression import SckitLearnLinearRegressionModel
import unittest
import io


class Test_ModelFactory(unittest.TestCase):
    def test_get_valid_stub_model_Instance(self):
        buffer_size = 10
        pre_train_size = 5
        m = ModelFactory.get_instance(SckitLearnLinearRegressionModel.name)
        self.assertTrue(type(m) is SckitLearnLinearRegressionModel)

    def test_get_invalid_model(self):
        buffer_size = 10
        pre_train_size = 5
        with self.assertRaises(Exception):
            m = ModelFactory.get_instance('invalid_model_name')


if __name__ == '__main__':
    unittest.main()
