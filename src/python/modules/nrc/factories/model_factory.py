from nrc.models.stub_model import StubModel


class ModelFactory():

    @staticmethod
    def get_instance(i_model_name, i_buffer_size):
        if i_model_name == "stub_model":
            return ModelFactory.get_stub_model(i_buffer_size)
        else:
            raise Exception('Model not available from factory')

    @staticmethod
    def get_stub_model(i_buffer_size):
        return StubModel(i_buffer_size)


if __name__ == '__main__':
    pass
