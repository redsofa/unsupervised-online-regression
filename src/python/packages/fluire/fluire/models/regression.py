from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from river import forest


# https://riverml.xyz/0.15.0/api/forest/ARFRegressor/
class AdaptiveRandomForestRegressionModel():

    def __init__(self):
        self._model = forest.ARFRegressor(seed=42)

    @staticmethod
    def get_name():
        return 'river_adaptive_random_forest_regression_model'


# https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html#sphx-glr-auto-examples-linear-model-plot-ols-py
class SckitLearnLinearRegressionModel():

    def __init__(self):
        self._model = linear_model.LinearRegression()

    def predict(self, x):
        return self._model.predict(x)

    def fit(self, x, y):
        self._model.fit(x, y)

    @property
    def model_evaluation_fn(self):
        def fn(**kwargs):
            return mean_squared_error(kwargs['y_true'], kwargs['y_pred'], squared=False)
        return fn

    @property
    def threshold_calculation_fn(self):
        def fn(**kwargs):
            Z1 = kwargs['Z1']
            Z2 = kwargs['Z2']
            # buffer_max_len = kwargs['buffer_max_len']
            d = (abs(Z2 - Z1))
            return d
        return fn

    @staticmethod
    def get_name():
        return 'sklearn_linear_regression_model'


if __name__ == '__main__':
    pass
