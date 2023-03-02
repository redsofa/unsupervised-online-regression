import unittest
from nrc.models.regression import SckitLearnLinearRegressionModel
from nrc.models.runner import ModelRunner
from nrc.factories.model import ModelFactory
from nrc.factories.stream import StreamFactory
from nrc.util.window import TrainTestWindow, DataBuffer
from common_test_utils import get_test_data_stream
import io
from sklearn import linear_model


class TestModelRunner(unittest.TestCase):
    def test_simple_model_run(self):
        print(f'\nExecuting {TestModelRunner.test_simple_model_run.__name__} test')

        # Configure window sizes
        train_test_window_size = 10
        train_size = round(train_test_window_size * 0.8)
        test_size = round(train_test_window_size * 0.2)
        buffer_size = test_size
        max_samples = None # If set to None, it will process data until the end of the stream

        print(f'train_test_window_size : {train_test_window_size}')
        print(f'train_size : {train_size}')
        print(f'test_size : {test_size}')
        print(f'buffer_size : {buffer_size}')
        print(f'max_samples : {max_samples}')

        # Create the ModelRunner object
        m_run = ModelRunner(model_name = SckitLearnLinearRegressionModel.name)

        # Configure a CSV stream instance of testing data
        data_stream = get_test_data_stream()

        # Configure a TrainTest_Window instance
        tt_win = TrainTestWindow(train_size, test_size)

        buffer = DataBuffer(buffer_size)

        # Configure the ModelRunner instance
        # and run it... As it runs, we get 
        # predictions as it's processing the stream.
        for x, y in m_run\
            .set_train_test_window(tt_win)\
            .set_data_stream(data_stream)\
            .set_max_samples(max_samples)\
            .set_buffer(buffer)\
            .set_threshold(5)\
            .run():
                #pass
                #
                print(f'Yielded prediction - Input Features : {x}, Predictions {y}')


        print(f'Model run time: {m_run.run_time}')

        # Initially fail the test to ensure code gets executed in
        # test run
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
