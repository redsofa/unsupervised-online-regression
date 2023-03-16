from fluire.models.regression import SckitLearnLinearRegressionModel


class ModelFactory():

    @staticmethod
    def get_instance(model_name):
        ret_val = None
        if model_name == SckitLearnLinearRegressionModel.get_name():
            ret_val = ModelFactory.get_sklearn_linear_regression_model()
        else:
            raise Exception('Model not available from factory')

        return ret_val

    @staticmethod
    def get_sklearn_linear_regression_model():
        return SckitLearnLinearRegressionModel()


if __name__ == '__main__':
    pass
