from nrc.models.base_model import *


class StubModel(BaseModel):
    def __init__(self, i_pre_train_size, i_buffer_size, i_max_samples=None):
        super().__init__(i_pre_train_size, i_buffer_size, 'stub_model', i_max_samples)

    def process(self, x, y):
        print(f'TRAINED ... New instance : features: {x} -- target: {y}')

    def pre_train(self, x, y):
        print(f'PRE-TRAIN ... New instance : features: {x} -- target: {y}')

    def predict_and_update(self, x, y):
        pass


if __name__ == '__main__':
    pass
