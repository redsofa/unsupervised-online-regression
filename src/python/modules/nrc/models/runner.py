'''
The high-level API for running model could look like this :

model_runner.set_train_test_window(train_test_window)
model_runner.set_metrics(regression_metrics_window)
model_runner.set_model(regression_model)
model_runner.set_stream(csv_stream)
model_runner.set_max_samples()
model_runner.validate_settings() # check that the ttw total size < max_samples
model_runner.run()
'''

import time


class ModelRunner():
    def __init__(self):
        self._tt_win = None
        self._metrics_win = None
        self._model = None
        self._data_stream = None
        self._max_samples = None
        self._settings_valid = False
        self._start_time = None
        self._end_time = None

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

    def run(self):
        #print(f'Running model : {self._model.name}\n')
        #self.validate_settings()
        self._start_time  = time.time()

        for x, y in self._data_stream:
            print(x, y)
            # The add_instance() method figures out if we should stop the run because
            # we have reached the maximum number of records we want to process from the stream.
            # It also figures out if we are in pre-train or normal stream processing mode.
            # Additionally, it increments the sample count.
            #self.add_instance(x, y)

            # Stop running the algorithm if we this flag has been set.
            # This flag usually means that the maximum number of records to process from the stream
            # has been reached.
            #if self._stop_run :
            #    break

        self._end_time = time.time()


    def validate_settings(self):
         # Check that the stream has been set
        if self._data_stream is None:
            raise Exception(f'Cannot run the algorithm {self._model.name}, the input data stream has not been set.')

    def set_max_samples(self, max_samples):
        self._max_samples = max_samples

    def set_train_test_window(self, tt_win):
        self._tt_win = tt_win

    def set_metrics_window(self, m_win):
        self._metrics_win = m_win

    def set_model(self, model):
        self._model = model

    def set_data_stream(self, stream):
        self._data_stream = stream
