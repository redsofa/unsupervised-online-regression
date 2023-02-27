import time
import numpy as np
from nrc.util.transformers import DepVaritoInstanceTransformer

class ModelRunner():
    def __init__(self):
        self._tt_win = None
        self._initial_training_done = False
        self._metrics_win = None
        self._model = None
        self._data_stream = None
        self._max_samples = None
        self._settings_valid = False
        self._start_time = None
        self._end_time = None
        self._stop_run = False
        self._sample_count = 0
        self._transformer = None
        self._instance_transformer = DepVaritoInstanceTransformer()

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
    def initial_training_done(self):
        return self._initial_training_done

    def _trigger_initial_training(self):
        print('Initial training triggered')
        self._transformer.samples = self._tt_win.train_samples
        train = self._transformer.execute()
        self._transformer.samples = self._tt_win.test_samples
        test = self._transformer.execute()
        self._model.fit(train['x'], train['y'])
        self._initial_training_done = True
        print('Initial training complete')

    def add_one_sample(self, x, y):
        self._sample_count += 1
        if self._max_samples is not None:
            if self._sample_count >= self._max_samples:
                print('Maximum instance count reached. Stopping stream processing.')
                self._stop_run = True
                return
        # We are in the initial training mode.. Need to fill up
        # the train/test window
        if not self._tt_win.is_filled:
            self._tt_win.add_one_sample(x, y)
            if self._tt_win.is_filled:
                self._trigger_initial_training()
        else:
            # The stream data comes in as a dictionary. We need a transformer to transform it
            # prior to passing the x, y values to the model for prediction.
            self._instance_transformer.dep_var = x
            tr_instance = self._instance_transformer.execute()
            # Make prediction
            y_pred = self._model.predict(tr_instance['x'])
            print(y_pred)
            # Add to buffer (x, y_pred)
            # Add to post_train_ train_test_winddow
            # Check buffer size
            # if buffer size == the max_buffer_size 
            # fit model
            # make predictions...
            # Calculate RMSE
            # if d_threashold < delta... etc ...


    def run(self):
        print('\nLaunching model runner')
        print('Validating model runner settings')
        self.validate_settings()
        print(f'Running model : {self._model.name}')
        self._start_time  = time.time()

        for x, y in self._data_stream:
            # The add_one_sample() method figures out if we should stop the run because
            # we have reached the maximum number of records we want to process from the stream.
            self.add_one_sample(x, y)

            # Stop running the algorithm if we this flag has been set.
            # This flag usually means that the maximum number of records to process from the stream
            # has been reached.
            if self._stop_run :
                break

            if self.initial_training_done:
                print('model trained... on to buffers and predictions ')


        self._end_time = time.time()

    def validate_settings(self):
        # Check that the model has been set
        if self._model is None:
            raise Exception('Cannot launch the model runner. The model instance has not been set.')

        # Check that the stream has been set
        if self._data_stream is None:
            raise Exception(f'Cannot run the algorithm {self._model.name}, the input data stream has not been set.')

        # Check if TrainTestWindow instance has been set
        if self._tt_win is None:
            raise Exceptino(f'Cannot run the algorithm {self._model.name}, the TrainTestWindow instance has not been set.')

    def set_transformer(self, transformer):
        self._transformer = transformer

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
