import time
import numpy as np
from nrc.util.transformers import XYTransformers
from sklearn.metrics import mean_squared_error


class ModelRunner():
    def __init__(self):
        self._tt_win = None
        self._initial_training_done = False
        self._evaluation_metric = None
        self._model = None
        self._data_stream = None
        self._max_samples = None
        self._settings_valid = False
        self._start_time = None
        self._end_time = None
        self._stop_run = False
        self._sample_count = 0
        self._transformer = None
        #        self._instance_transformer = DepVaritoInstanceTransformer()
        self._buffer = None

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
        # The data comes in as a dictionary (e.g. {x: {f1 : 0.1, f2: 0.3, ... fn: xn}, y : [y1,... yn]}
        # It needs to be transformed to numpy arrays

        # Transform the training and testing data
        x_train, y_train = XYTransformers.arr_dict_to_xy(self._tt_win.train_samples)
        x_test, y_test = XYTransformers.arr_dict_to_xy(self._tt_win.test_samples)

        # Fit the model to the training data
        self._model.fit(x_train, y_train)

        # Make predictions on the test data
        y_preds = self._model.predict(x_test)

        # Evaluate the model's performance (compare truth values with predictions) and store
        # the evaluation metric
        self._evaluation_metric = mean_squared_error(y_test, y_preds)

        self._initial_training_done = True
        print('Initial training complete')

    def _swap_model(self, model):
        self._model = model

    def _process_prediction(self, x, y_pred):
        print(f'Processing prediction (x, y_pred): ({x}, {y_pred})')
        # If buffer is not full
        if not self._buffer.is_filled :
            # Note that x and y are numpy arrays. No transformations needed to use in prediction.
            # Fill up the buffer and a post-initial-training train/test window
            # Keep filling the buffer and windows until we reach the maximum buffer size
            '''
            self._buffer.add_one_sample(x, y_pred)

            # Remove the oldest sample from the training window
            self._tt_win.get_and_remove_oldest_train_sample()

            # The first sample x,y in the test window will be taken out and put into into the
            # train window.
            # Save and take out the oldest sample from the testing window
            oldest_test_sample = self._tt_win.get_and_remove_oldest_test_sample()

            # The new test instance is the new incoming x value and the prediction
            self._tt_win.add_one_test_sample(x, y_pred)

            # Put the oldest test sample into the training window
            self._tt_win.add_one_train_sample(oldest_test_sample)
            '''
        else :
            print('Buffer is full!!')


            # If the Size of B == b:
            #   Predictions = model.fit(training window)
            #   evaluate with testing data
            #   Calculate d from the calculated RMSE value
            #   if the d < delta_threshold :
            #     REMOVE first entry from buffer ..???
            #   else:
            #     model = retrain model using buffer
            #     slush the buffer
            #  Z1 = Z2 (Metrics values)
            # Make prediction
            #y_pred = self._model.predict(tr_instance['x'])
            #print(y_pred)
            # B = B + {x_ins, y_ins)

            # Add to buffer (x, y_pred)
            # Add to post_train_ train_test_winddow
            # Check buffer size
            # if buffer size == the max_buffer_size
            # fit model
            # make predictions...
            # Calculate METRICS
            # if d_threashold < delta... etc ...

    def _trigger_one_prediction(self, sample):
        x = [sample['x']]
        # Make a prediction with trained model
        y_pred = self._model.predict(x)
        # Process that prediction
        self._process_prediction(x, y_pred)

    def add_one_sample(self, sample):
        self._sample_count += 1
        if self._max_samples is not None:
            if self._sample_count >= self._max_samples:
                print('Maximum instance count reached. Stopping stream processing.')
                self._stop_run = True
                return
        # We are in the initial training mode.. Need to fill up
        # the train/test window so we can train the initial model.
        if not self._tt_win.is_filled:
            self._tt_win.add_one_sample(sample)
            if self._tt_win.is_filled:
                self._trigger_initial_training()
        else:
            self._trigger_one_prediction(sample)

    def run(self):
        print('\nLaunching model runner')
        print('Validating model runner settings')
        self.validate_settings()
        print(f'Running model : {self._model.name}')
        self._start_time  = time.time()

        for x, y in self._data_stream:
            # The add_one_sample() method figures out if we should stop the run because
            # we have reached the maximum number of records we want to process from the stream.

            # Incoming data looks like :
            #
            # x : {'c1': 1.0, 'c2': 2.0}
            # y : 23
            #
            # Need to convert it to a dictionary that looks like:
            # {'x': array([1., 2.]), 'y': array([23])}
            #
            sample = XYTransformers.xy_to_numpy_dictionary(x, y)

            self.add_one_sample(sample)

            # Stop running the algorithm if we this flag has been set.
            # This flag usually means that the maximum number of records to process from the stream
            # has been reached.
            if self._stop_run :
                break

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

        if self._buffer is None:
            raise Exceptino(f'Cannot run the algorithm {self._model.name}, the DataBuffer instance has not been set.')

    def set_max_samples(self, max_samples):
        self._max_samples = max_samples
        return self

    def set_train_test_window(self, tt_win):
        self._tt_win = tt_win
        return self

    def set_model(self, model):
        self._model = model
        return self

    def set_data_stream(self, stream):
        self._data_stream = stream
        return self

    def set_buffer(self, buffer):
        self._buffer = buffer
        return self
