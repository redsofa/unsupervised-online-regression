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
        self._minimum_required_working_datapoints = 120
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
        self._drift_detector_name = None
        self._drift_detector_config = None
        self._drift_detectors_initialized = False
        self._drift_detectors_array = []
        self._drift_handler = None
        self._model_retrained_handler = None
        self._retrain_at_every_sample_count = None
        self._delta_threshold = None
        self._is_baseline_run = False
        logger.debug('ModelRunner construction done. Nothing initalized yet.')

    def validate_settings(self) -> None:
        logger.debug('Validating model runner settings.')
        if self._model is None:
            msg = 'The model instance has not been set.'
            logger.error(msg)
            raise Exception(msg)

        if self._model_eval_fn is None:
            msg = 'The model evaluation function has not been set.'
            logger.error(msg)
            raise Exception(msg)

        if self._data_stream is None:
            msg = 'The input data stream has not been set.'
            logger.error(msg)
            raise Exception(msg)

        if self._working_data_points < self._minimum_required_working_datapoints:
            msg = f'Number of working data points must be at least {self._minimum_required_datapoints}'
            logger.error(msg)
            raise Exception(msg)

        if self._delta_threshold is None and self._is_baseline_run is False:
            msg = 'Delta threshold is not set. It needs to be set for non-baseline model runs.'
            logger.error(msg)
            raise Exception(msg)

    def set_is_baseline_run(self, is_baseline: bool) -> ModelRunner:
        logger.debug('Setting whether model run is a baseline run.')
        self._is_baseline_run = is_baseline
        return self

    def set_delta_threshold(self, threshold):
        logger.debug('Setting delta threshold')
        self._delta_threshold = threshold
        return self

    def set_model_retrained_handler(self, fn):
        logger.debug('Setting model retrained handler.')
        self._model_retrained_handler = fn
        return self

    def set_drift_handler(self, fn):
        logger.debug('Setting drift detected handler.')
        self._drift_handler = fn
        return self

    def set_drift_detector_config(self, **kwargs) -> ModelRunner:
        self._drift_detector_config = kwargs
        detector_type = self._drift_detector_config['detector']
        logger.debug(f'detector kwargs : {kwargs}')
        logger.debug(f'Setting detector_type : {detector_type}')
        if detector_type == 'NA':
            self._drift_detector_name = 'NA'
        elif detector_type == 'ADWIN':
            self._drift_detector_name = 'ADWIN'
        elif detector_type == 'PERIODIC':
            self._drift_detector_name = 'PERIODIC'
            self._retrain_at_every_sample_count = kwargs['retrain_every']
        else:
            msg = 'Invalid drift detector type'
            logger.error(msg)
            raise Exception(msg)
        return self

    def set_scaler(self, obj: Scaler) -> ModelRunner:
        logger.debug('Scaler set.')
        self._scaler = obj
        return self

    def set_data_stream(self, stream) -> ModelRunner:
        logger.debug('Setting data stream.')
        self._data_stream = stream
        return self

    def set_max_samples(self, max_samples: int) -> ModelRunner:
        self._max_samples = max_samples
        return self

    def set_model_name(self, model_name: str) -> ModelRunner:
        logger.debug(f"Setting model : {model_name}")
        self._model_name = model_name
        self._initialize_model()
        self._initialize_model_eval_fn()
        return self

    def set_working_data_points(self, working_data_points: int) -> ModelRunner:
        self._working_data_points = working_data_points
        self._initialize_sliding_window_and_buffer()
        return self

    def _initialize_model(self) -> None:
        logger.debug('Initializing model')
        self._model = ModelFactory.get_instance(self._model_name)

    def _initialize_model_eval_fn(self) -> None:
        logger.debug('Initializing model evaluation function.')
        self._model_eval_fn = self._model.model_evaluation_fn

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

    @property
    def model_name(self):
        return self._model_name

    @property
    def run_time(self):
        if self._start_time is not None and self._end_time is not None:
            return self._end_time - self._start_time
        else:
            raise Exception("Start or End time has not been set yet.")

    def _make_one_prediction(self, sample):
        logger.debug('Making online prediction on single sample.')
        # A sample looks something like {'x': array([1., 2.]), 'y': array([None])}
        x = [sample["x"]]
        # Make a prediction with trained model
        y_pred = self._model.predict(x)
        self._prediction_count += 1
        logger.debug(f'Prediction count : {self._prediction_count}')
        # Process that prediction
        return x, y_pred

    def _flag_if_should_stop_run(self) -> None:
        logger.debug('Checking if the run should stop.')
        if self._max_samples is not None:
            if self._sample_count >= self._max_samples:
                logger.debug("Maximum instance count reached. Stopping stream processing.")
                self._stop_run = True

    def _add_initial_train_sample(self, sample):
        logger.debug(f'Sample count : {self._sample_count}')
        logger.debug('Adding initial training data.')
        if not self._sliding_window.is_full:
            self._sliding_window.add_data(sample)
            logger.debug(f'Sliding window was not full yet. Current size now : {self._sliding_window.len}.')
        elif not self._buffer.is_full:
            self._buffer.add_data(sample)
            logger.debug(f'Buffer was not full yet. Current size now : {self._buffer.len}.')
        else:
            self._initial_working_datapoints_recieved = True
            logger.debug('Both sliding window and buffer are full.')

    def _trigger_initial_model_training(self):
        logger.debug('Launching initial model training.')
        # The data comes in as a dictionary
        # (e.g. {x: {f1 : 0.1, f2: 0.3, ... fn: xn}, y : [y1,... yn]}
        # It needs to be transformed to numpy arrays

        # Transform the training and testing data
        x_train, y_train = XYTransformers.arr_dict_to_xy(self._sliding_window.get_as_list())
        x_test, y_test = XYTransformers.arr_dict_to_xy(self._buffer.get_as_list())
        logger.debug(f'x_train : {x_train}')
        logger.debug(f'y_train : {y_train}')
        logger.debug(f'x_test : {x_test}')
        logger.debug(f'y_test : {y_test}')
        # Fit the model to the training data
        self._model.fit(x_train, np.ravel(y_train))

        # Make predictions on the test data
        y_preds = self._model.predict(x_test)

        # Evaluate the model's performance (compare truth values with predictions) and store
        # the evaluation metric
        self._Z1 = self._model_eval_fn(y_true=y_test, y_pred=y_preds)
        self._initial_training_done = True
        logger.debug(f'Z1 score : {self._Z1}')
        logger.debug('Initial model trained.')

    def run(self):
        logger.debug('Running model.')
        self._start_time = time.time()
        try:
            for x, y in self._data_stream:
                logger.debug(f'New stream data point available. x:{x} <-> y:{y}')
                self._initial_drift_detectors_setup(len(x.items()))
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
                    if self._initial_working_datapoints_recieved:
                        logger.debug('All initial data points received. Triggering initial model training.')
                        self._trigger_initial_model_training()
                        x, y_pred = self._make_one_prediction(sample)
                        logger.debug('Clearing buffer contents.')
                        if not self._is_baseline_run:
                            logger.debug('Is not baseline run, processing prediction.')
                            self._buffer.clear_contents()
                            self._process_prediction(x, y_pred)
                        logger.debug('Yielding prediction results.')
                        yield (x, y_pred, y, False)
                    else:
                        yield ([sample["x"]], np.array([[None]]), sample["y"][0], True)
                else:
                    x, y_pred = self._make_one_prediction(sample)
                    if not self._is_baseline_run:
                        logger.debug('Is not baseline run, processing prediction.')
                        self._process_prediction(x, y_pred)
                    logger.debug('Yielding prediction results.')
                    yield (x, y_pred, y, False)
            self._end_time = time.time()
        except Exception as e:
            logger.error(str(e))
            raise e

    def _initial_drift_detectors_setup(self, num_features):
        if not self._drift_detector_config['detector'] == 'ADWIN':
            logger.debug('Drift detector is not ADWIN. No need to initialize.')
            return
        else:
            if not self._drift_detectors_initialized:
                logger.debug('Drift detector not initialized yet.')
                logger.debug(f'Initial setup of drift detector array. {num_features} detectors setup.')
                for x in range(0, num_features):
                    self._drift_detectors_array.append(drift.ADWIN(delta=self._drift_detector_config['delta']))
                self._drift_detectors_initialized = True

    def _is_drift_detected(self):
        logger.debug('Checking for drift.')
        drift_detected = False

        if self._drift_detector_config['detector'] == 'ADWIN':
            logger.debug('Checking for feature drifts in ADWIN drift detectors.')
            required_feature_drifts = self._drift_detector_config['required_feature_drifts']
            feature_drifts = 0
            if required_feature_drifts > len(self._drift_detectors_array) or required_feature_drifts <= 0:
                msg = "ADWIN's required_feature_drift parameter must be greater" \
                      + "than 0 and less than the number of features. " \
                      + f"required_feature_drift is set to : {required_feature_drifts}. " \
                      + f"The number of features is : {len(self._drift_detectors_array)}."
                logger.error(msg)
                raise Exception(msg)
            for d in self._drift_detectors_array:
                if d.drift_detected:
                    feature_drifts += 1
                    if feature_drifts == required_feature_drifts:
                        logger.debug('Requisite feature drifts reached.')
                        drift_detected = True
                        break

        if self._drift_detector_config['detector'] == 'PERIODIC':
            if self._prediction_count % self._retrain_at_every_sample_count == 0:
                drift_detected = True

        if drift_detected:
            if self._drift_handler:
                logger.debug('Calling drift handler.')
                self._drift_handler(
                    sample_count=self._sample_count
                )
        return drift_detected

    def _model_replacement_required(self, Z1, Z2, threshold):
        logger.debug('Determining if model replacement is required.')
        logger.debug(f'Z1 : {Z1}, Z2 : {Z2}, threshold : {threshold}, abs(Z1-Z2) : {abs(Z2-Z1)}')
        model_replacement_required = False
        if abs(Z2-Z1) > threshold:
            model_replacement_required = True
        logger.debug(f'Model replacement is required : {model_replacement_required}')
        return model_replacement_required

    def _update_drift_detectors(self, x, y_pred):
        if self._drift_detector_config['detector'] == 'ADWIN':
            logger.debug('Drift detector is ADWIN. Updating detectors with feature datapoints.')
            for idx, elem in enumerate(x[0]):
                self._drift_detectors_array[idx].update(elem)

    def _train_new_model(self) -> None:
        logger.debug('Training new model.')
        new_model = ModelFactory.get_instance(self._model_name)

        # Transform the training and testing data
        x_train, y_train = XYTransformers.arr_dict_to_xy(self._sliding_window.get_as_list())
        logger.debug(f'y_train : {y_train}')

        # TODO : Re-introduce these two lines. If kept, train and test
        # contain buffer elements. Training and testing have some data that is the same otherwise.
        # Results produced with these lines commented out are repported in the paper and
        # become worse when they are uncommented.
        # x_train = x_train[:-self._buffer.len]
        # y_train = y_train[:-self._buffer.len]

        x_test, y_test = XYTransformers.arr_dict_to_xy(self._buffer.get_as_list())
        # logger.debug(f'x_train : {x_train}')
        logger.debug(f'y_train : {y_train}')
        # logger.debug(f'x_test : {x_test}')
        logger.debug(f'y_test : {y_test}')

        # Fit the model to the training data
        new_model.fit(x_train, np.ravel(y_train))

        # Make predictions on the test data
        y_preds = new_model.predict(x_test)

        # Evaluate the model's performance (compare truth values with predictions) and store
        # the evaluation metric
        Z2 = self._model_eval_fn(y_true=y_test, y_pred=y_preds)
        logger.debug(f'Z2 score : {Z2}')
        logger.debug('New model trained.')

        return new_model, Z2

    def _process_prediction(self, x, y_pred):
        logger.debug('Processing new prediction.')
        xy_ins = XYTransformers.xy_pred_to_numpy_dictionary(x, y_pred)
        logger.debug('Adding data to buffer.')
        self._buffer.add_data(xy_ins)
        logger.debug('Updating the sliding window.')
        self._sliding_window.get_and_remove_oldest()
        self._sliding_window.add_data(xy_ins)

        if self._drift_detector_name != 'NA':
            logger.debug('Updating the drift detector.')
            self._update_drift_detectors(x, y_pred)

        if self._buffer.is_full:
            logger.debug('Buffer is full.')
            logger.debug(f'Buffer contents : {self._buffer.get_as_list()}')
            # If we are using a drift detector,
            if self._drift_detector_name != 'NA':
                logger.debug('Drift detector in use.')
                if self._is_drift_detected():
                    logger.debug(f'Drift detected using detector : {self._drift_detector_name}.')
                    new_model, Z2 = self._train_new_model()
                    if self._model_replacement_required(self._Z1, Z2, self._delta_threshold):
                        logger.debug('Replacing existing model with new model.')
                        self._model = new_model
                        self._Z1 = Z2
                        if self._model_retrained_handler:
                            logger.debug('Calling model retrain handler.')
                            self._model_retrained_handler(model=self._model, sample_count=self._sample_count)
                    else:
                        logger.debug('No model replacement required.')
                else:
                    logger.debug(f'No drifts in features detected using detector : {self._drift_detector_name}.')
            # If no drift detector is being used,
            else:
                logger.debug('Drift detector not in use.')
                new_model, Z2 = self._train_new_model()
                if self._model_replacement_required(self._Z1, Z2, self._delta_threshold):
                    if self._drift_handler:
                        logger.debug('Calling drift handler Z2-Z1 drift detected.')
                        self._drift_handler(
                            sample_count=self._sample_count
                        )
                    logger.debug('Model replacement required.')
                    logger.debug('Replacing existing model with new model.')
                    self._model = new_model
                    self._Z1 = Z2
                    if self._model_retrained_handler:
                        logger.debug('Calling model retrain handler.')
                        self._model_retrained_handler(model=self._model, sample_count=self._sample_count)
                else:
                    logger.debug('No model replacement required.')

            logger.debug('Clearing buffer contents.')
            self._buffer.clear_contents()


if __name__ == '__main__':
    pass
