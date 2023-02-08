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
        self._threshold = None

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
    def process_one(self, x, y):
        pass

    @abstractmethod
    def pre_train_one(self, x, y):
        pass

    @abstractmethod
    def predict_and_update_one(self, x, y):
        pass

    @abstractmethod
    def _evaluate_metrics(self):
        pass

    @abstractmethod
    def _update_buffer_yn(self):
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

        print(f'Running model : {self._name}\n')
        for x, y in self.data_stream:
            # The add_instance() method figures out if we should stop the run because
            # we have reached the maximum number of records we want to process from the stream.
            # It also figures out if we are in pre-train or normal stream processing mode.
            # Additionally, it increments the sample count.
            self.add_instance(x, y)

           # Stop running the algorithm if we this flag has been set.
           # This flag usually means that the maximum number of records to process from the stream
           # has been reached.
            if self._stop_run :
                break

            # If we are in pre-training mode, call the pre-train_one method.
            if self._is_pre_train:
                self.pre_train_one(x, y)
            else:
                # Here the model has been trained. We need to process the incoming sample.
                # The process_one() method calls predict_and_update_one(),
                # which (may do a fit or partial fit) depending on the size of the buffer and
                # the evaluation metrics.
                y_pred = self.process_one(x, y)
                add_to_buffer = self._evaluate_metrics()
                if add_to_buffer:
                    self._update_buffer_yn(prediction)

        self._end_time = time.time()

    def __str__(self):
        return str(self.__dict__)


if __name__ == "__main__":
    pass
