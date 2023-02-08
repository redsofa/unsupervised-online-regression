from nrc.factories.model import ModelFactory
from nrc.factories.stream import StreamFactory
from nrc.models.stub_model import StubModel
import unittest
import io


class Test_ModelFactory(unittest.TestCase):
    def test_get_valid_stub_model_Instance(self):
        buffer_size = 10
        pre_train_size = 5
        m = ModelFactory.get_instance('stub_model', pre_train_size, buffer_size)
        self.assertTrue(type(m) is StubModel)

    def test_get_invalid_model(self):
        buffer_size = 10
        with self.assertRaises(Exception):
            m = ModelFactory.get_instance('invalid_model_name', buffer_size)


class Test_ModelRunning(unittest.TestCase):
    def test_run_stub_model(self):
        buffer_size = 10
        pre_train_size = 5
        # A stream with 2 samples
        test_data = io.StringIO("c1,c2,t\n1,2,0\n3,2,1")
        params = {"converters":{"c1":float, "c2":float}, "target":"t"}
        data_stream = StreamFactory.get_csv_stream(test_data, **params)
        # Create stub model and run it...
        model = ModelFactory.get_instance('stub_model', pre_train_size, buffer_size)
        model.data_stream = data_stream
        model.run()
        # There should be only 2 samples that were fed to the model
        self.assertEqual(model.sample_count, 2)


if __name__ == '__main__':
    unittest.main()
