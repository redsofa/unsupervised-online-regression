from abc import ABC, abstractmethod
import time
from nrc.util.buffers import *


class BaseModel(ABC):
    def __init__(self, i_pretrain_size, i_buffer_size, i_name, i_max_samples=None):
        self._name = i_name
        self._buffer = SlidingWindow(i_buffer_size)
        self._start_time = None
        self._end_time = None
        self._data_stream = None
        self._is_pre_train = True
        self._stop_run = False
        self._max_samples = i_max_samples
        self._pre_train_size = i_pretrain_size
        self._sample_count = 0

    @property
    def sample_count(self):
        return self._sample_count

    @property
    def data_stream(self):
        return self._data_stream

    @data_stream.setter
    def data_stream(self, i_data_stream):
        self._data_stream = i_data_stream

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
    def name(self):
        return self._name

    @abstractmethod
    def process(self, x, y):
        pass

    @abstractmethod
    def pre_train(self, x, y):
        pass

    @abstractmethod
    def predict_and_update(self, x, y):
        pass

    def add_instance(self, x, y):
        if self._max_samples is not None:
            if self._sample_count >= self._max_samples:
                print('Maximum instance count reached. Stopping stream processing.')
                self._stop_run = True
                return

        if self._sample_count >= self._pre_train_size:
            self._is_pre_train = False

        self._sample_count += 1

    def run(self):
        # Check that the stream has been set
        if self.data_stream is None:
            raise Exception(f'Cannot run the algorithm {self.name}, the input data stream has not been set.')
        self._start_time  = time.time()

        print(f'Running model : {self._name}')
        for x, y in self.data_stream:
            self.add_instance(x, y)

            if self._stop_run :
                break

            if self._is_pre_train:
                self.pre_train(x, y)
            else:
                self.process(x, y)

        self._end_time = time.time()

    def __str__(self):
        return str(self.__dict__)


if __name__ == "__main__":
    pass
