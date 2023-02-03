from queue import Queue
from abc import ABC, abstractmethod


class BaseModel(ABC):
    def __init__(self, i_buffer_size, i_name):
        self._name = i_name
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

    def pre_train(self, x, y):
        pass

    def predict_and_update(self, x, y):
        pass


if __name__ == "__main__":
    pass
