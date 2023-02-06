from queue import Queue
from abc import ABC, abstractmethod
import time


class BaseModel(ABC):
    def __init__(self, i_buffer_size, i_name):
        self._name = i_name
        self._buffer = Queue(i_buffer_size)
        self._start_time = None
        self._ent_time = None
        self._stream = None

    @property
    def stream(self):
        return self._stream

    @stream.setter
    def stream(self, i_stream):
        self._stream = i_stream

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def run_time(self):
        if self.start_time is not None and self.end_time is not None:
            return self.end_time - self.start_time
        else:
            raise Exception("Start or End time has not been set yet.")

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
    def process(self, x, y):
        pass

    @abstractmethod
    def pre_train(self, x, y):
        pass

    @abstractmethod
    def predict_and_update(self, x, y):
        pass

    @abstractmethod
    def run(self):
        pass


if __name__ == "__main__":
    pass
