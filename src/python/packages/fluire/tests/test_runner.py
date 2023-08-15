import unittest
from fluire.models.runner import ModelRunner
from fluire.models.regression import SckitLearnLinearRegressionModel
from common_test_utils import get_test_data_stream
from fluire.settings.logging import logger


class TestModelRunner(unittest.TestCase):
    def test_simple_model_run(self):
        logger.debug(f"Executing {TestModelRunner.test_simple_model_run.__name__} test")
        # Get the unit testing data stream
        data_stream = get_test_data_stream()
        detector_info = {"detector": "ADWIN", "required_feature_drifts": 1, "delta": 0.02}
        # detector_info = {'detector': 'PERIODIC', 'retrain_every': 1}

        # Create the ModelRunner object
        m_run = ModelRunner()
        # Set this private memeber variable just for the test.
        m_run._minimum_required_working_datapoints = 10
        m_run\
            .set_model_name(SckitLearnLinearRegressionModel.get_name())\
            .set_working_data_points(10)\
            .set_data_stream(data_stream)\
            .set_scaler(None)\
            .set_drift_detector_config(**detector_info)\
            .set_drift_handler(None)\
            .set_model_retrained_handler(None)\
            .set_max_samples(None)\
            .set_delta_threshold(0.03)

        m_run.validate_settings()

        logger.debug(f'Working data points : {m_run.working_data_points}')
        logger.debug(f'Size of sliding window : {m_run.sliding_window.len}')
        logger.debug(f'Size of buffer : {m_run.buffer.len}')

        logger.debug(f'Sliding window max_len : {m_run.sliding_window.max_len}')
        logger.debug(f'Buffer max_len : {m_run.buffer.max_len}')

        for x, y_pred, y_true, is_train_data in m_run.run():
            logger.debug(f'Yielded x : {x}, Yielded prediction : {y_pred}')


if __name__ == "__main__":
    unittest.main()
