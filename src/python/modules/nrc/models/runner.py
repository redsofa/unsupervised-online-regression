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

class ModelRunner():
    def __init__(self):
        self._tt_win = None
        self._metrics_win = None
        self._momdel = None
        self._stream = None
        self._max_samples = None
        self._settings_valid = False

    def run(self):
        #if self._settings_vali:
            # do something
        #else
            # raise Exception('Invalid ModelRunner settings. Make sure that xyz...')
        pass

    def validate_settings(self):
        pass

    def set_max_samples(self, max_samples):
        self._max_samples = max_samples

    def set_train_test_window(self, tt_win):
        self._tt_win = tt_win

    def set_metrics_window(self, m_win):
        self._metrics_win = m_win

    def set_model(self, model):
        self._model = model

    def set_stream(self, stream):
        self._stream = stream
