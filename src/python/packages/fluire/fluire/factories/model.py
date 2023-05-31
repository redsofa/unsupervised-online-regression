from fluire.models.regression import SckitLearnLinearRegressionModel
from fluire.models.regression import ScikitLearnRandomForestRegressor
from fluire.models.regression import ScikitLearnSVRRegressor


class ModelFactory():

    @staticmethod
    def get_instance(model_name):
        ret_val = None
        if model_name == SckitLearnLinearRegressionModel.get_name():
            ret_val = ModelFactory.get_sklearn_linear_regression_model()
        elif model_name == ScikitLearnRandomForestRegressor.get_name():
            ret_val = ModelFactory.get_sklearn_random_forest_regressor_model()
        elif model_name == ScikitLearnSVRRegressor.get_name():
            ret_val = ModelFactory.get_svr_regressor_model()
        else:
            raise Exception('Model not available from factory')

        return ret_val

    @staticmethod
    def get_svr_regressor_model():
        return ScikitLearnSVRRegressor()

    @staticmethod
    def get_sklearn_random_forest_regressor_model():
        return ScikitLearnRandomForestRegressor()

    @staticmethod
    def get_sklearn_linear_regression_model():
        return SckitLearnLinearRegressionModel()


if __name__ == '__main__':
    pass
