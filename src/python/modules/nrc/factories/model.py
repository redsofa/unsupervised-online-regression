from nrc.models.stub import StubRegressionModel
from nrc.models.regression import SckitLearnLinearRegressionModel 


class ModelFactory():

    @staticmethod
    def get_instance(i_model_name, i_pre_train_size, i_buffer_size, i_max_samples=None):
        ret_val = None
        if i_model_name == "stub_regression_model":
            ret_val =  ModelFactory.get_stub_regression_model(i_pre_train_size, i_buffer_size, i_max_samples)
        elif i_model_name == 'sklearn_linear_regression_model':
            ret_val = ModelFactory.get_sklearn_linear_regression_model(i_pre_train_size, i_buffer_size, i_max_samples)
        else:
            raise Exception('Model not available from factory')

        print(f'\nInstantiated model : {i_model_name}')
        print()
        return ret_val

    @staticmethod
    def get_stub_regression_model(i_pre_train_size, i_buffer_size, i_max_samples):
        return StubRegressionModel(i_pre_train_size, i_buffer_size, i_max_samples)

    @staticmethod
    def get_sklearn_linear_regression_model(i_pre_train_size, i_buffer_size, i_max_samples):
        return SckitLearnLinearRegressionModel(i_pre_train_size, i_buffer_size, i_max_samples)


if __name__ == '__main__':
    pass
