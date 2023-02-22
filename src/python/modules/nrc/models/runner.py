'''
The high-level API for running model could look like this :

model_runner.set_train_test_window(ttw)
model_runner.set_metrics(regression_metrics)
model_runner.set_model(regression_model)
model_runner.set_stream(stream)
model_runner.set_max_samples()
model_runner.validate_settings() # check that the ttw total size < max_samples
model_runner.run()
'''

class ModelRunner():
    def __init__(self):
        pass
