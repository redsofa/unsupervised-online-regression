from nrc.models.base import *
from sklearn import linear_model

# https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html#sphx-glr-auto-examples-linear-model-plot-ols-py
class SckitLearnLinearRegressionModel():

    def __init__(self):
        self._model = linear_model.LinearRegression()

    def predict(self, x):
        return self._model.predict(x)

    def fit(self, x, y):
        self._model.fit(x, y)

    def evaluate(self, x_test, y_pred, y_true):
        pass

    @property
    def name(self):
        return SckitLearnLinearRegressionModel.get_name()

    @staticmethod
    def get_name():
        return 'sklearn_linear_regression_model' 

if __name__ == '__main__':
    pass
