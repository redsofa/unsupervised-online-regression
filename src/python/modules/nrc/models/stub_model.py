from queue import Queue
from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self, i_buffer_size):
        self._name = 'stub_model'
        self._buffer = Queue(i_buffer_size)
    
    @property
    def buffer(self):
        return self._buffer

    @property
    def name(self):
        return self._name

    def clear_buffer(self):
        while not self._buffer.empty(): 
            self._buffer.get()

    @abstractmethod
    def process(self): 
        pass



class StubModel(BaseModel):
    def process(self, x, y):
        print(f'In model : {self._name}')
        print(f'New instance : features: {x} -- target: {y}')

    
if __name__ == '__main__':
    pass
