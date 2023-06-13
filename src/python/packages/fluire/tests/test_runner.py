import unittest
from fluire.models.runner_2 import ModelRunner
from fluire.models.regression import SckitLearnLinearRegressionModel
from common_test_utils import get_test_data_stream
from fluire.settings.logging import logger


class TestModelRunner(unittest.TestCase):
    def test_simple_model_run(self):
        logger.info(f"Executing {TestModelRunner.test_simple_model_run.__name__} test")
        # Get the unit testing data stream
        data_stream = get_test_data_stream()

        # Create the ModelRunner object
        m_run = ModelRunner()
        m_run\
            .set_model_name(SckitLearnLinearRegressionModel.get_name())\
            .set_working_data_points(10)\
            .set_data_stream(data_stream)

        m_run.validate_settings()

        logger.info(f'Working data points : {m_run.working_data_points}')
        logger.info(f'Size of sliding window : {m_run.sliding_window.len}')
        logger.info(f'Size of buffer : {m_run.buffer.len}')

        logger.info(f'Sliding window max_len : {m_run.sliding_window.max_len}')
        logger.info(f'Buffer max_len : {m_run.buffer.max_len}')

        for x, y_pred, y_true in m_run.run():
            logger.info(f'Yielded prediction {y_pred}')
            #logger.info(f'yielded x : {x}')
            #logger.info(f'Size of sliding window : {m_run.sliding_window.len}')
            #logger.info(f'Size of buffer : {m_run.buffer.len}')

 


if __name__ == "__main__":
    unittest.main()
