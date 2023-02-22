from collections import deque
from nrc.util.observable import BaseObservableImpl
from collections import defaultdict

class TrainTestWindow(BaseObservableImpl):
    def __init__(self, train_size, test_size):
        # Call the base class's default constructor.
        # Creates the self._observers instance.
        super().__init__()
        self._train_size = train_size
        self._test_size = test_size
        self._train_win = SlidingWindow(self._train_size)
        self._test_win = SlidingWindow(self._test_size)

        self.register_on_add_sample_handler(self._on_add_sample)

    @property
    def train_sample_count(self):
        return self._train_win.len()

    @property
    def test_sample_count(self):
        return self._test_win.len()

    @property
    def is_training(self):
        return self._train_win < self._train_size

    @property
    def is_testing(self):
        self._test_win < self._test_size

    @property
    def test_samples(self):
        return self._test_win.get_as_list()

    @property
    def train_samples(self):
        return self._train_win.get_as_list()

    @property
    def is_filled(self):
        return (self._train_win.len() == self._train_size) \
                and (self._test_win.len() == self._test_size)

    def _on_add_sample(self, *args, **kwargs):
        x = kwargs['x']
        y = {'y' : kwargs['y']}
        data = x | y # merge x and y dictionaries (python 3.9+)
        if self._train_win.len() < self._train_size:
            self._train_win.add_data(data)
        elif self._test_win.len() < self._test_size:
            self._test_win.add_data(data)
        else:
            raise Exception('Train and test windows are full')
        if self.is_filled :
            self.trigger('on_is_filled', None, None)

    def add_one_sample(self, *args, **kwargs):
        self.trigger('on_add_sample', *args, **kwargs)

    def register_on_filled_handler(self, function):
        self.subscribe('on_is_filled', function)

    def register_on_add_sample_handler(self, function):
        self.subscribe('on_add_sample', function)

# Basically a queue first, in first out,
class SlidingWindow(BaseObservableImpl):
    def __init__(self, max_len):
        # Call the base class's default constructor.
        # Creates the self._observers instance.
        super().__init__()
        self._max_len = max_len
        self._data = deque(maxlen = max_len)

    def clear_contents(self):
        self._data.clear()

    def get_element_at(self, index):
        try:
            return self._data[index]
        except IndexError:
            raise Exception('Element index out of range.')

    def len(self):
        return len(list(self._data))

    def add_data(self, i_data):
        self._data.append(i_data)

    def get_as_list(self):
        return list(self._data)

    def pop(self):
        return self._data.popleft()


if __name__ == '__main__':
    pass
