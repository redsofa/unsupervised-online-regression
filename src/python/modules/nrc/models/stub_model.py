from nrc.models.base_model import *


class StubModel(BaseModel):
    def __init__(self, i_buffer_size):
        super().__init__(i_buffer_size, 'stub_model')

    def process(self, x, y):
        pass

    def pre_train(self, x, y):
        pass

    def predict_and_update(self, x, y):
        pass


if __name__ == '__main__':
    pass
