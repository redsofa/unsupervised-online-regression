from nrc.models.stub_model import StubModel


class ModelFactory():

    @staticmethod
    def get_instance(i_model_name, i_pre_train_size, i_buffer_size, i_max_samples=None):
        ret_val = None
        if i_model_name == "stub_model":
            ret_val =  ModelFactory.get_stub_model(i_pre_train_size, i_buffer_size, i_max_samples)
        else:
            raise Exception('Model not available from factory')

        print(f'\nInstantiated model : {i_model_name}')
        print()
        return ret_val

    @staticmethod
    def get_stub_model(i_pre_train_size, i_buffer_size, i_max_samples):
        return StubModel(i_pre_train_size, i_buffer_size, i_max_samples)


if __name__ == '__main__':
    pass
