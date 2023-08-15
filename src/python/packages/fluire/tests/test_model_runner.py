import unittest
from fluire.models.regression import SckitLearnLinearRegressionModel
from fluire.models.runner import ModelRunner


class TestModelRunner(unittest.TestCase):
    def test_invalid_runner_run(self):
        print(f"\nExecuting {TestModelRunner.test_invalid_runner_run.__name__} test")

        m_run = ModelRunner()\
            .set_model_name(SckitLearnLinearRegressionModel.get_name())

        with self.assertRaises(Exception):
            # m_run is a generator. It does not execute any code unless we start iterating
            # over it. Therefore, we have to call the next() method on it
            next(m_run.run())


if __name__ == "__main__":
    unittest.main()
