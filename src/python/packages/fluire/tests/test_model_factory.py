from nrc.factories.model import ModelFactory
from nrc.models.regression import SckitLearnLinearRegressionModel
import unittest


class Test_ModelFactory(unittest.TestCase):
    def test_get_valid_stub_model_Instance(self):
        m = ModelFactory.get_instance(SckitLearnLinearRegressionModel.get_name())
        self.assertTrue(type(m) is SckitLearnLinearRegressionModel)

    def test_get_invalid_model(self):
        with self.assertRaises(Exception):
            ModelFactory.get_instance('invalid_model_name')


if __name__ == '__main__':
    unittest.main()
