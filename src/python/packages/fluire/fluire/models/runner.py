from __future__ import annotations
import time
from fluire.util.transformers import XYTransformers
from fluire.factories.model import ModelFactory
from fluire.util.scalers import Scaler
import numpy as np
from river import drift


class ModelRunner:
    def __init__(self, model_name: str) -> None:
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
        self._prediction_count = 0
        self._evaluation_fn = self._model.model_evaluation_fn
        self._drift_handler = None
        self._model_retrained_handler = None
        self._scaler = None
        self._tt_win_updates = 0
        self._retrain_at_every_sample_count = -1
        self._drift_detector = None

    def set_drift_detector(self, detector):
        if detector is None:
            self._drift_detector = None
        elif detector == 'ADWIN':
            #self._drift_detector = drift.ADWIN(clock=16, max_buckets=20, min_window_length=50)
            self._drift_detector = drift.ADWIN()
        elif detector == 'KSWIN':
            self._drift_detector = drift.KSWIN(alpha=0.0001, seed=42)
        elif detector == 'PAGEHINKLEY':
            self._drift_detector = drift.PageHinkley()
        else:
            raise Exception('Invalid drift detector')
        return self

    def set_scaler(self, obj: Scaler) -> ModelRunner:
        self._scaler = obj
        return self

    def set_model_retrained_handler(self, fn):
        self._model_retrained_handler = fn
        return self

    def set_retrain_at_every_sample_count(self, count):
        self._retrain_at_every_sample_count = count
        return self

    @property
    def model_name(self):
        return self._model_name

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
        # The data comes in as a dictionary
        # (e.g. {x: {f1 : 0.1, f2: 0.3, ... fn: xn}, y : [y1,... yn]}
        # It needs to be transformed to numpy arrays

        # Transform the training and testing data
        x_train, y_train = XYTransformers.arr_dict_to_xy(self._tt_win.train_samples)
        x_test, y_test = XYTransformers.arr_dict_to_xy(self._tt_win.test_samples)

        # Fit the model to the training data
        self._model.fit(x_train, np.ravel(y_train))

        # Make predictions on the test data
        y_preds = self._model.predict(x_test)

        # Evaluate the model's performance (compare truth values with predictions) and store
        # the evaluation metric
        self._Z1 = self._evaluation_fn(y_true=y_test, y_pred=y_preds)

        self._initial_training_done = True

    def _trigger_new_model_training(self):
        # The data comes in as a dictionary
        # (e.g. {x: {f1 : 0.1, f2: 0.3, ... fn: xn}, y : [y1,... yn]}
        # It needs to be transformed to numpy arrays

        # Transform the training and testing data
        x_train, y_train = XYTransformers.arr_dict_to_xy(self._tt_win.train_samples)
        x_test, y_test = XYTransformers.arr_dict_to_xy(self._tt_win.test_samples)

        new_model = ModelFactory.get_instance(self._model_name)

        # Fit the model to the training data
        new_model.fit(x_train, np.ravel(y_train))

        # Make predictions on the test data
        y_preds = new_model.predict(x_test)

        # Evaluate the model's performance (compare truth values with predictions) and return
        # the evaluation metric
        eval_metric = self._evaluation_fn(y_true=y_test, y_pred=y_preds)

        return new_model, eval_metric

    def _retrain_required(self, x, y_pred):
        if self._retrain_at_every_sample_count is not None:
            if self._tt_win_updates == self._retrain_at_every_sample_count:
                return True
            else:
                return False

        if self._drift_detector is not None:
            self._drift_detector.update(y_pred[0])
            if self._drift_detector.drift_detected:
                return True
            else:
                return False

    def _process_prediction(self, x, y_pred):
        new_sample = XYTransformers.xy_pred_to_numpy_dictionary(x, y_pred)
        self._tt_win_updates += 1
        # The oldest sample in the training will be removed
        self._tt_win.get_and_remove_oldest_train_sample()
        # The oldest sample in the testing window will be removed
        # AND added to the training window
        oldest_test_sample = self._tt_win.get_and_remove_oldest_test_sample()
        self._tt_win.add_one_train_sample(oldest_test_sample)
        self._tt_win.add_one_test_sample(new_sample)

        if self._retrain_required(x, y_pred):
            print('Retrain required')
            self._tt_win_updates = 0
            self._model, _ = self._trigger_new_model_training()
            if self._model_retrained_handler:
                self._model_retrained_handler(model=self._model)

            if self._drift_handler:
                self._drift_handler(
                    prediction_count=self._prediction_count, drift_indicator_value=0
                )

    def _make_one_prediction(self, sample):
        self._prediction_count += 1
        # A sample looks something like {'x': array([1., 2.]), 'y': array([None])}
        x = [sample["x"]]
        # Make a prediction with trained model
        y_pred = self._model.predict(x)
        # Process that prediction
        return x, y_pred

    def add_one_sample(self, sample):
        if self._max_samples is not None:
            if self._sample_count >= self._max_samples:
                print("Maximum instance count reached. Stopping stream processing.")
                self._stop_run = True
                return
        # We are in the initial training mode.. Need to fill up
        # the train/test window so we can train the initial model.
        if not self._tt_win.is_filled:
            self._tt_win.add_one_sample(sample)
            if self._tt_win.is_filled:
                self._trigger_initial_training()

    def run(self):
        print("\nLaunching model runner")
        print("Validating model runner settings")
        self.validate_settings()
        print(f"Running model : {self._model_name}")
        self._start_time = time.time()

        try:
            for x, y in self._data_stream:
                self._sample_count += 1
                # Stop running the algorithm if we this flag has been set.
                # This flag usually means that the maximum number of records to process from the
                # stream has been reached. The add_one_sample() method figures out if we should
                # stop the run because we have reached the maximum number of records we want to
                # process from the stream.
                if self._stop_run:
                    break
                # Scale the data if scaler is set
                if self._scaler:
                    x = self._scaler.add_sample(x)
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
        except Exception as e:
            raise e

    def validate_settings(self):
        # Check that the model has been set
        if self._model is None:
            raise Exception(
                "Cannot launch the model runner. The model instance has not been set."
            )

        # Check that the stream has been set
        if self._data_stream is None:
            raise Exception(
                f"Cannot run the algorithm {self._model_name}. "
                "The input data stream has not been set."
            )

        # Check if TrainTestWindow instance has been set
        if self._tt_win is None:
            raise Exception(
                f"Cannot run the algorithm {self._model_name}. "
                "The TrainTestWindow instance has not been set."
            )

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

    def set_drift_handler(self, fn):
        self._drift_handler = fn
        return self


if __name__ == "__main__":
    pass
