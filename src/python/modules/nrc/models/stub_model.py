from nrc.models.base_model import *


class StubModel(BaseModel):
    def __init__(self, i_buffer_size):
        super().__init__(i_buffer_size, 'stub_model')

    def process(self, x, y):
        print(f'In model : {self._name}')
        print(f'New instance : features: {x} -- target: {y}')

    
if __name__ == '__main__':
    pass
