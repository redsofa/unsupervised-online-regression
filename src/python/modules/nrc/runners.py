from nrc.factories.model import ModelFactory

class ModelRunner:
    def __init__(self, i_input_stream, i_model_names, i_buffer_size):
        self._input_stream = i_input_stream
        self._buffer_size = i_buffer_size
        self._models = []
        for n in i_model_names:
            self._models.append(ModelFactory.get_instance(n, self._buffer_size))

    def run_models(self):
        for x, y in self._input_stream :
            for m in self._models:
                m.process(x, y)
    
    @property
    def models(self):
        return self._models


if __name__ == '__main__':
    pass
