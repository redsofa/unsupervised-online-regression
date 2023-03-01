from collections import deque


class RegressionMetricsWindow():
    def __init__(self, window_size):
        self._window_size = window_size
        self._metrics_win = SlidingWindow(self._window_size)

    def add_one_metric(self, metric):
        self._metrics_win.add_data(metric)

    def len(self):
        return self._metrics_win.len()


class DataBuffer():
    def __init__(self, max_len):
        self._max_len = max_len
        self._data_win = SlidingWindow(self._max_len)

    @property
    def is_filled(self):
        return (self._data_win.len() >= self._max_len)

    def add_one_sample(self, sample):
        if self._data_win.len() < self._max_len:
            self._data_win.add_data(data)
        else:
            raise Exception('Buffer is full')

    def add_one_sample(self, x, y):
        indep = {'x' : x}
        dep = {'y' : y}

        data = indep | dep # merge x and y dictionaries (python 3.9+)
        if self._data_win.len() < self._max_len:
            self._data_win.add_data(data)
        else:
            raise Exception('Buffer is full')

    def get_and_remove_oldest_sample(self):
        return self._data_win.get_and_remove_oldest()


class TrainTestWindow():
    def __init__(self, train_size, test_size):
        self._train_size = train_size
        self._test_size = test_size
        self._train_win = SlidingWindow(self._train_size)
        self._test_win = SlidingWindow(self._test_size)
        self._on_filled_handler = None

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
        return (self._train_win.len() >= self._train_size) \
                and (self._test_win.len() >= self._test_size)

    def add_one_test_sample(self, x, y):
        indep = {'x' : x}
        dep = {'y': y}
        data = indep | dep
        self._test_win.add_data(data)

    def add_one_train_sample(self, x, y):
        indep = {'x' : x}
        dep = {'y': y}
        data = indep | dep
        self._train_win.add_data(data)

    def get_and_remove_oldest_train_sample(self):
        return self._test_win.get_and_remove_oldest()

    def get_and_remove_oldest_test_sample(self):
        return self._train_win.get_and_remove_oldest()

    def add_one_sample(self, sample):
        if self._train_win.len() < self._train_size:
            self._train_win.add_data(sample)
        elif self._test_win.len() < self._test_size:
            self._test_win.add_data(sample)
        else:
            raise Exception('Train and test windows are full')
        if self.is_filled :
            if self._on_filled_handler:
                self._on_filled_handler()
    '''
    def add_one_sample(self, x, y):
        indep = {'x' : x}
        dep = {'y' : y}

        data = indep | dep # merge x and y dictionaries (python 3.9+)
        if self._train_win.len() < self._train_size:
            self._train_win.add_data(data)
        elif self._test_win.len() < self._test_size:
            self._test_win.add_data(data)
        else:
            raise Exception('Train and test windows are full')
        if self.is_filled :
            if self._on_filled_handler:
                self._on_filled_handler()
    '''

    def register_on_window_filled_handler(self, function):
        self._on_filled_handler = function


# Basically a queue first, in first out,
class SlidingWindow():
    def __init__(self, max_len):
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

    def get_and_remove_oldest(self):
        return self._data.popleft()


if __name__ == '__main__':
    pass
