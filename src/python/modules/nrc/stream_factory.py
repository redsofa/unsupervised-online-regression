from river import stream

class StreamFactory():
    def __init__(self):
        self._params = None
        self._stream = None

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    def get_csv_stream(self, input_file, target, **kwargs):
        return stream.iter_csv(input_file, target, **kwargs)


if __name__ == '__main__':
    pass
