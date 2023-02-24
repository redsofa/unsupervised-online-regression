from nrc.models.base import *


# https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html#sphx-glr-auto-examples-linear-model-plot-ols-py
class SckitLearnLinearRegressionModel(BaseRegressionModel):
    def __init__(self, i_pre_train_size, i_buffer_size, i_max_samples=None):
        super().__init__(i_pre_train_size, i_buffer_size, 'sklearn_linear_regression_model', i_max_samples)

    def process_one(self, x, y):
        print(f'TRAINED -  processing one... New instance : features: {x} -- target: {y}')

    def pre_train_one(self, x, y):
        print(f'PRE-TRAIN - pre-training one... New instance : features: {x} -- target: {y}')

    def predict_and_update_one(self, x, y):
        pass

    def _evaluate_metrics(self):
        pass

    def _update_buffer_yn(self):
        pass



if __name__ == '__main__':
    pass