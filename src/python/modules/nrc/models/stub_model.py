from queue import Queue


class StubModel:
    def __init__(self, i_buffer_size):
        self._name = 'stub_model'
        self._buffer = Queue(i_buffer_size)

    @property
    def buffer(self):
        return self._buffer

    @property
    def name(self):
        return self._name

    def process(self, x, y):
        print(f'In model : {self._name}')
        print(f'New instance : features: {x} -- target: {y}')

    def clear_buffer(self):
        while not self._buffer.empty(): 
            self._buffer.get()


if __name__ == '__main__':
    pass
