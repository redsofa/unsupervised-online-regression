from river import metrics
import pandas as pd


class RegressionMetrics:

    def __init__(self):
        self._MAE = metrics.MAE()
        self._MSE = metrics.MSE()
        self._RMSE = metrics.RMSE()
        self._R2 = metrics.R2()

    def add_one_prediction(self, y_true, y_pred):
        self._MAE.update(y_true, y_pred)
        self._MSE.update(y_true, y_pred)
        self._RMSE.update(y_true, y_pred)
        self._R2.update(y_true, y_pred)

    def __str__(self):
        d ={}
        d['MAE'] = self._MAE.get()
        d['MSE'] = self._MSE.get()
        d['RMSE'] = self._RMSE.get()
        d['R2'] = self._R2.get()
        df = pd.DataFrame.from_dict(d, orient='index', columns=['value'])
        df.reset_index()
        return df.to_string()

    @property
    def rmse(self):
        return self._RMSE.get()

    @property
    def mae(self):
        return self._MAE.get()

    @property
    def mse(self):
        return self._MSE.get()

    @property
    def r2(self):
        return self._R2.get()


if __name__ == '__main__':
    pass
