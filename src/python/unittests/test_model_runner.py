import unittest
from nrc.models.regression import SckitLearnLinearRegressionModel
from nrc.models.runner import ModelRunner
from nrc.util.window import TrainTestWindow, DataBuffer
from common_test_utils import get_test_data_stream
import numpy as np


class TestModelRunner(unittest.TestCase):
    def test_invalid_runner_run(self):
        print(f"\nExecuting {TestModelRunner.test_invalid_runner_run.__name__} test")
        m_run = ModelRunner(model_name=SckitLearnLinearRegressionModel.get_name())

        with self.assertRaises(Exception) as ex:
            # m_run is a generator. It does not execute any code unless we start iterating
            # over it. Therefore, we have to call the next() method on it
            next(m_run.run())

        print(ex.exception)

    # TODO : Make this testing more thorough. Need to test all invalid settings. 
    def test_invalid_runner_validate_settings(self):
        print(f"\nExecuting {TestModelRunner.test_invalid_runner_validate_settings.__name__} test")
        m_run = ModelRunner(model_name=SckitLearnLinearRegressionModel.get_name())

        with self.assertRaises(Exception) as ex:
            m_run.validate_settings()

        expected_error_msg = f"Cannot run the algorithm {m_run.model_name}."\
                             " The input data stream has not been set."

        self.assertEquals(str(ex.exception), expected_error_msg)

    def test_simple_model_run(self):
        print(f"\nExecuting {TestModelRunner.test_simple_model_run.__name__} test")
        # Configure window sizes
        train_test_window_size = 10
        train_size = round(train_test_window_size * 0.8)
        test_size = round(train_test_window_size * 0.2)
        buffer_size = test_size
        # If max_samples set to None, it will process data until the end of the stream
        max_samples = None

        print(f"train_test_window_size : {train_test_window_size}")
        print(f"train_size : {train_size}")
        print(f"test_size : {test_size}")
        print(f"buffer_size : {buffer_size}")
        print(f"max_samples : {max_samples}")

        # Create the ModelRunner object
        m_run = ModelRunner(model_name=SckitLearnLinearRegressionModel.get_name())

        # Configure a CSV stream instance of testing data
        data_stream = get_test_data_stream()

        # Configure a TrainTest_Window instance
        tt_win = TrainTestWindow(train_size, test_size)

        buffer = DataBuffer(buffer_size)

        features = []
        predictions = []

        # Configure the ModelRunner instance
        # and run it... As it runs, we get
        # predictions as it's processing the stream.
        for x, y_pred, y_true in (
            m_run.set_train_test_window(tt_win)
            .set_data_stream(data_stream)
            .set_max_samples(max_samples)
            .set_buffer(buffer)
            .set_threshold(5)
            .run()
        ):
            features.append(x)
            predictions.append(y_pred)

        print(f"Model run time: {m_run.run_time}")

        expected_features = [
            [[2.1, 3.1]],
            [[2.0, 3.1]],
            [[2.4, 3.2]],
            [[3.0, 3.4]],
            [[1.0, 2.0]],
            [[2.2, 3.5]],
            [[3.0, 3.1]],
            [[2.0, 3.1]],
            [[2.4, 3.4]],
            [[2.4, 3.4]],
            [[2.4, 3.4]],
            [[2.0, 3.2]],
        ]
        expected_predictions = [
            [[21.98889487]],
            [[21.89803473]],
            [[22.1024364]],
            [[22.32951945]],
            [[22.73886122]],
            [[21.44359941]],
            [[22.80663616]],
            [[21.89803473]],
            [[21.78435859]],
            [[21.78435859]],
            [[21.78435859]],
            [[21.73899583]],
        ]
        self.assertTrue(
            np.allclose(np.array(expected_predictions), predictions, equal_nan=True)
        )
        self.assertTrue(
            np.allclose(np.array(expected_features), features, equal_nan=True)
        )


if __name__ == "__main__":
    unittest.main()
