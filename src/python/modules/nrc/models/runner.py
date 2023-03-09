import time
import math
import numpy as np
from nrc.util.transformers import XYTransformers
from sklearn.metrics import mean_squared_error
from nrc.factories.model import ModelFactory

class ModelRunner():
    def __init__(self, model_name):
        self._tt_win = None
        self._initial_training_done = False
        self._Z1 = None
        self._model_name = model_name
        self._model = ModelFactory.get_instance(model_name)
        self._data_stream = None
        self._max_samples = None
        self._settings_valid = False
        self._start_time = None
        self._end_time = None
        self._stop_run = False
        self._sample_count = 0
        self._buffer = None
        self._delta_threshold = None
        self._evaluation_fn = self._model.model_evaluation_fn
        self._threshold_calculation_fn = self._model.threshold_calculation_fn

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def run_time(self):
        if self._start_time is not None and self._end_time is not None:
            return self._end_time - self._start_time
        else:
            raise Exception("Start or End time has not been set yet.")

    @property
    def initial_training_done(self):
        return self._initial_training_done

    def _trigger_initial_training(self):
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
        self._Z1 = self._evaluation_fn(y_true=y_test, y_pred=y_preds)

        # Normalize the Z1 value (Average value of RMSE)
        self._Z1 = self._Z1/len(y_test)

        self._initial_training_done = True

    def _swap_model(self, model):
        self._model = model

    def _train_model_on_buffer(self):
        train_samples = self._buffer.samples[0:1] 
        test_samples = self._buffer.samples[2:3]
        # Transform the training and testing data
        x_train, y_train = XYTransformers.arr_dict_to_xy(train_samples)
        x_test, y_test = XYTransformers.arr_dict_to_xy(test_samples)

        new_model = ModelFactory.get_instance(self._model_name)

        # Fit the model to the training data
        new_model.fit(x_train, y_train)
        return new_model

    def _trigger_new_model_training(self):
        # The data comes in as a dictionary (e.g. {x: {f1 : 0.1, f2: 0.3, ... fn: xn}, y : [y1,... yn]}
        # It needs to be transformed to numpy arrays

        # Transform the training and testing data
        x_train, y_train = XYTransformers.arr_dict_to_xy(self._tt_win.train_samples)
        x_test, y_test = XYTransformers.arr_dict_to_xy(self._tt_win.test_samples)

        new_model = ModelFactory.get_instance(self._model_name)

        # Fit the model to the training data
        new_model.fit(x_train, y_train)

        # Make predictions on the test data
        y_preds = new_model.predict(x_test)

        # Evaluate the model's performance (compare truth values with predictions) and return
        # the evaluation metric
        eval_metric = self._evaluation_fn(y_true=y_test, y_pred=y_preds)

        return new_model, eval_metric

    def _process_prediction(self, x, y_pred):
        if not self._buffer.is_filled :
            new_sample = XYTransformers.xy_pred_to_numpy_dictionary(x, y_pred)
            self._buffer.add_one_sample(new_sample)
            #The oldest sample in the training will be removed 
            oldest_train_sample = self._tt_win.get_and_remove_oldest_train_sample()
            #The oldest sample in the testing window will be removed
            #AND added to the training window
            oldest_test_sample = self._tt_win.get_and_remove_oldest_test_sample()
            self._tt_win.add_one_train_sample(oldest_test_sample)
            self._tt_win.add_one_test_sample(new_sample)
        else :
            new_model, Z2 = self._trigger_new_model_training()
            d = self._threshold_calculation_fn(Z1 = self._Z1, Z2 = Z2 , buffer_max_len = self._buffer.max_len)

            if (d < self._delta_threshold):
                self._buffer.remove_samples(1)
            else:
                # We have a drift
                # Fit new model on the buffer
                self._train_model_on_buffer()
                # Clear the buffer
                self._buffer.clear_contents()

            self._Z1 = Z2
            
    def _make_one_prediction(self, sample):
        # A sample looks something like {'x': array([1., 2.]), 'y': array([None])}
        x = [sample['x']]
        # Make a prediction with trained model
        y_pred = self._model.predict(x)
        # Process that prediction
        return x, y_pred

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

    def run(self):
        print('\nLaunching model runner')
        print('Validating model runner settings')
        self.validate_settings()
        print(f'Running model : {self._model_name}')
        self._start_time  = time.time()

        for x, y in self._data_stream:
            # Stop running the algorithm if we this flag has been set.
            # This flag usually means that the maximum number of records to process from the stream
            # has been reached. The add_one_sample() method figures out if we should stop the run because
            # we have reached the maximum number of records we want to process from the stream.
            if self._stop_run :
                break

            # Incoming data looks like :
            #
            # x : {'c1': 1.0, 'c2': 2.0}
            # y : 23
            #
            # Need to convert it to a dictionary that looks like:
            # {'x': array([1., 2.]), 'y': array([23])}
            #
            sample = XYTransformers.xy_to_numpy_dictionary(x, y)
            if not self._initial_training_done:
                self.add_one_sample(sample)
            else:
                x, y_pred = self._make_one_prediction(sample)
                yield(x, y_pred, y)
                self._process_prediction(x, y_pred)

        self._end_time = time.time()

    def validate_settings(self):
        # Check that the model has been set
        if self._model is None:
            raise Exception('Cannot launch the model runner. The model instance has not been set.')

        # Check that the stream has been set
        if self._data_stream is None:
            raise Exception(f'Cannot run the algorithm {self._model_name}. The input data stream has not been set.')

        # Check if TrainTestWindow instance has been set
        if self._tt_win is None:
            raise Exceptino(f'Cannot run the algorithm {self._model_name}. The TrainTestWindow instance has not been set.')

        if self._buffer is None:
            raise Exceptino(f'Cannot run the algorithm {self._model_name}. The DataBuffer instance has not been set.')

        if self._delta_threshold is None:
            raise Exception(f'Cannot run the algorithm {self._model_name}. The delta threshold is not set.') 

    def set_threshold(self, delta):
        self._delta_threshold = delta
        return self

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


if __name__ == '__main__':
    pass
