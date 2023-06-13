from __future__ import annotations
from fluire.factories.model import ModelFactory
from fluire.util.window import Window
from fluire.util.scalers import Scaler
from fluire.util.transformers import XYTransformers
from fluire.settings.logging import logger
from river import drift
from math import floor
import time
import numpy as np


class ModelRunner:
    def __init__(self) -> None:
        self._model_name = None
        self._model = None
        self._working_data_points = None
        self._minimum_required_working_datapoints = 10
        self._sliding_window = None
        self._buffer = None
        self._Z1 = None
        self._max_samples = None
        self._data_stream = None
        self._model_eval_fn = None
        self._scaler = None
        self._sample_count = 0
        self._start_time = None
        self._end_time = None
        self._stop_run = False

        self._initial_training_done = False
        self._initial_working_datapoints_recieved = False
        self._prediction_count = 0
        self._drift_handler = None
        self._drift_detector = None
        self._retrain_at_every_sample_count = None
        self._model_retrained_handler = None
        logger.info('ModelRunner Construction. Nothing initalized yet.')

    def set_scaler(self, obj: Scaler) -> ModelRunner:
        logger.info('Scaler set.')
        self._scaler = obj
        return self

    def validate_settings(self) -> None:
        logger.info('Validating model runner settings.')
        # Check that the model has been set
        if self._model is None:
            raise Exception(
                "The model instance has not been set."
            )
        # Check that the model evaluation function has been set
        if self._model_eval_fn is None:
            raise Exception(
                "The model evaluation function has not been set."
            )

        # Check that the stream has been set
        if self._data_stream is None:
            raise Exception(
                "The input data stream has not been set."
            )
        # Do we have the proper amount of datapoints
        if self._working_data_points < self._minimum_required_working_datapoints:
            raise Exception(
                f'Number of working data points must be at least {self._minimum_required_datapoints}'
            )

    def set_data_stream(self, stream) -> ModelRunner:
        logger.info('Setting data stream.')
        self._data_stream = stream
        return self

    def set_max_samples(self, max_samples: int) -> ModelRunner:
        self._max_samples = max_samples
        return self

    def set_model_name(self, model_name: str) -> ModelRunner:
        logger.info(f"Setting model : {model_name}")
        self._model_name = model_name
        self._initialize_model()
        self._initialize_model_eval_fn()
        return self

    def _initialize_model(self) -> None:
        logger.info('Initializing model')
        self._model = ModelFactory.get_instance(self._model_name)

    def _initialize_model_eval_fn(self) -> None:
        logger.info('Initializing model evaluation function.')
        self._model_eval_fn = self._model.model_evaluation_fn

    def set_working_data_points(self, working_data_points: int) -> ModelRunner:
        self._working_data_points = working_data_points
        self._initialize_sliding_window_and_buffer()
        return self

    def _initialize_sliding_window_and_buffer(self) -> None:
        if self._working_data_points < self._minimum_required_working_datapoints:
            raise Exception(f'Number of working data points must be at least {self._minimum_required_working_datapoints}')
        buffer_len = floor(self._working_data_points / 4)
        sliding_widown_len = self._working_data_points - buffer_len
        self._sliding_window = Window(max_len=sliding_widown_len, slides=True)
        self._buffer = Window(max_len=buffer_len, slides=False)

    @property
    def working_data_points(self):
        return self._working_data_points

    @property
    def sliding_window(self):
        return self._sliding_window

    @property
    def buffer(self):
        return self._buffer

    def _make_one_prediction(self, sample):
        logger.info('Making online prediction on single sample.')
        # A sample looks something like {'x': array([1., 2.]), 'y': array([None])}
        x = [sample["x"]]
        # Make a prediction with trained model
        y_pred = self._model.predict(x)
        self._prediction_count += 1
        logger.info(f'Prediction count : {self._prediction_count}')
        # Process that prediction
        return x, y_pred

    def _flag_if_should_stop_run(self) -> None:
        logger.info('Checking if the run should stop')
        if self._max_samples is not None:
            if self._sample_count >= self._max_samples:
                logger.info("Maximum instance count reached. Stopping stream processing.")
                self._stop_run = True

    def _add_initial_train_sample(self, sample):
        logger.info(f'Sample count : {self._sample_count}')
        if not self._sliding_window.is_full:
            logger.info(f'Sliding window is not full yet. Size : {self._sliding_window.len}. Adding new sample to the sliding window.')
            self._sliding_window.add_data(sample)
        elif not self._buffer.is_full:
            logger.info(f'Buffer is not full yet. Size : {self._buffer.len}. Adding new sample to the buffer.')
            self._buffer.add_data(sample)
        else:
            self._initial_working_datapoints_recieved = True
            logger.info('Both sliding window and buffer are full.')

    def _trigger_initial_model_training(self):
        logger.info('Launching initial model training.')
        # The data comes in as a dictionary
        # (e.g. {x: {f1 : 0.1, f2: 0.3, ... fn: xn}, y : [y1,... yn]}
        # It needs to be transformed to numpy arrays

        # Transform the training and testing data
        x_train, y_train = XYTransformers.arr_dict_to_xy(self._sliding_window.get_as_list())
        x_test, y_test = XYTransformers.arr_dict_to_xy(self._buffer.get_as_list())
        logger.info(f'x_train : {x_train}')
        logger.info(f'y_train : {y_train}')
        logger.info(f'x_test : {x_test}')
        logger.info(f'y_test : {y_test}')
        # Fit the model to the training data
        self._model.fit(x_train, np.ravel(y_train))

        # Make predictions on the test data
        y_preds = self._model.predict(x_test)

        # Evaluate the model's performance (compare truth values with predictions) and store
        # the evaluation metric
        self._Z1 = self._model_eval_fn(y_true=y_test, y_pred=y_preds)

        self._initial_training_done = True
        logger.info(f'Z1 score : {self._Z1}')
        logger.info('Initial model trained.')

    def run(self):
        logger.info('Running model.')
        self._start_time = time.time()
        try:
            for x, y in self._data_stream:
                logger.info('New stream data point available.')
                self._sample_count += 1
                self._flag_if_should_stop_run()
                if self._stop_run:
                    break

                # Scale the data if scaler is set
                if self._scaler is not None:
                    x = self._scaler.add_sample(x)

                # Transform the input data.
                # Incoming data looks like :
                #
                # x : {'c1': 1.0, 'c2': 2.0}
                # y : 23
                #
                # Need to convert it to a dictionary that looks like:
                # {'x': array([1., 2.]), 'y': array([23])}
                #
                sample = XYTransformers.xy_to_numpy_dictionary(x, y)

                # If the sliding window AND buffer are not full yet,
                # add the incoming sample data to the appropriate collection.
                if not self._initial_working_datapoints_recieved:
                    self._add_initial_train_sample(sample)
                # If the initial sliding window and buffer are full,
                # check if the initial model training has been done.
                # If it hasn't, trigger the initial model training. Once that
                # is done, make the first prediction on the incoming sample,
                # yield and process it.
                elif not self._initial_training_done:
                    self._trigger_initial_model_training()
                    x, y_pred = self._make_one_prediction(sample)
                    logger.info('Yielding first prediction')
                    yield (x, y_pred, y)
                    self._process_prediction(x, y_pred)
                    # If the initial sliding window and buffer are full,
                    # and the initial model has been trained,
                    # make the online prediction, yield and process it.
                else:
                    x, y_pred = self._make_one_prediction(sample)
                    logger.info('Yielding prediction')
                    yield (x, y_pred, y)
                    self._process_prediction(x, y_pred)

            self._end_time = time.time()
        except Exception as e:
            logger.error(str(e))
            raise e

    def _process_prediction(self, x, y_pred):
        logger.info('Processing new prediction')
        new_sample = XYTransformers.xy_pred_to_numpy_dictionary(x, y_pred)
        logger.info(new_sample)
        # The oldest sample in the training will be removed
        '''self._tt_win.get_and_remove_oldest_train_sample()'''
        # The oldest sample in the testing window will be removed
        # AND added to the training window
        '''oldest_test_sample = self._tt_win.get_and_remove_oldest_test_sample()
        self._tt_win.add_one_train_sample(oldest_test_sample)
        self._tt_win.add_one_test_sample(new_sample)

        if self._retrain_required(x, y_pred):
            logger.info('Retrain required')
            self._tt_win_updates = 0
            self._model, _ = self._trigger_new_model_training()
            if self._model_retrained_handler:
                self._model_retrained_handler(model=self._model)

            if self._drift_handler:
                self._drift_handler(
                    prediction_count=self._prediction_count, drift_indicator_value=0
                )
        '''

if __name__ == '__main__':
    pass
