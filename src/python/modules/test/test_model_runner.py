import unittest
from nrc.models.runner import ModelRunner
from nrc.factories.model import ModelFactory
from nrc.factories.stream import StreamFactory
from nrc.util.window import TrainTestWindow, RegressionMetricsWindow
import io

# Unit test helper functions
def get_test_data():
    sample_data = \
            '''c1,c2,y
            1.0,2.0,23
            2.2,3.5,22
            3.0,3.1,21
            2.0,3.1,20
            2.4,3.4,22
            2.0,3.1,24
            6.0,3.1,26
            2.0,3.1,22
            4.2,3.1,22
            2.0,3.5,27
            2.1,3.1,22
            2.0,3.1,25
            2.4,3.2,22
            3.0,3.4,25
            1.0,2.0,23
            2.2,3.5,22
            3.0,3.1,21
            2.0,3.1,20
            2.4,3.4,22
            2.4,3.4,22
            2.4,3.4,22
            2.0,3.2,24
            '''.replace(' ', '')

    ret_val = io.StringIO(sample_data)
    return ret_val

def get_stream_params():
    return {"converters":{"c1":float, "c2":float, 'y':int}, "target":"y"}

def get_test_data_stream():
    test_data = get_test_data()
    params = get_stream_params()
    data_stream = StreamFactory.get_csv_stream(test_data, **params)
    return data_stream


class TestModelRunner(unittest.TestCase):
    def test_simple_model_run(self):
        print(f'\nExecuting {TestModelRunner.test_simple_model_run.__name__} test')

        # Configure window sizes
        window_size = 10
        train_size = round(window_size * 0.8)
        test_size = round(window_size * 0.2)
        buffer_size = round(window_size * 0.4)
        max_samples = None

        print(f'window_size : {window_size}')
        print(f'train_size : {train_size}')
        print(f'test_size : {test_size}')
        print(f'buffer_size : {buffer_size}')
        print(f'max_samples : {max_samples}')

        # Create the ModelRunner object
        m_run = ModelRunner()

        # Configure a CSV stream instance of testing data
        data_stream = get_test_data_stream()

        # Configure a TrainTest_Window instance
        tt_win = TrainTestWindow(train_size, test_size)

        # Configure regression metrics window instance
        m_met = RegressionMetricsWindow(buffer_size)

        # Get a ScikitLearnRegressionModel instance
        model = ModelFactory.get_instance(
                'sklearn_linear_regression_model',
                1,
                1,
                1)

        # Configure the ModelRunner instance
        m_run.set_train_test_window(tt_win)
        m_run.set_data_stream(data_stream)
        m_run.set_model(model)
        m_run.set_max_samples(max_samples)
        m_run.run()

        print(f'Model run time: {m_run.run_time}')

        # Initially fail the test to ensure code gets executed in
        # test run
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
