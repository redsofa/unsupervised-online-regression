from nrc.factories.model import ModelFactory
from nrc.runners import ModelRunner
from nrc.models.stub_model import StubModel
import unittest
import io
from river import stream


class Test_ModelFactory(unittest.TestCase):
    def test_get_valid_stub_model_Instance(self):
        buffer_size = 10
        m = ModelFactory.get_instance('stub_model', buffer_size)
        self.assertTrue(type(m) is StubModel)
        m.clear_buffer()
        self.assertTrue(m.buffer.empty())

    def test_get_invalid_model(self):
        buffer_size = 10
        with self.assertRaises(Exception):
            m = ModelFactory.get_instance('invalid_model_name', buffer_size)


class Test_ModelRunner(unittest.TestCase):
    def test_run_models(self):
        buffer_size = 10
        model_names = ['stub_model']
        test_data = io.StringIO('F1, F2 \n 1, 2 \n 3, 2')
        params = {"converters" : {'F1':float, 'F2':float }}
        data_stream = stream.iter_csv(test_data, **params)
        runner = ModelRunner(data_stream, model_names, buffer_size)
        self.assertTrue(len(runner.models) == 1)
        self.assertEqual(model_names[0], runner.models[0].name)


if __name__ == '__main__':
    unittest.main()
