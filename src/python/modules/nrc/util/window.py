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


class WindowManager:
    '''
    TODO:
        The code below is a prototype of a WindowManager..

        The WindowManager class can contains multiple sliding windows
        Windows would / could include :
        - pre-train sliding window
        - test sliding window

        - post-train sliding window

    - Metrics values

        - etc..

        Adding to the buffer could possibly manage which window get the data depending
        on how far we are in the pre-training...

        Adding to the buffer could possibly manage when to run metrics calculations and trigger
        retraining, buffer flushing events... etc..
    '''

    def __init__(self, i_train_size, i_test_size, i_buffer_size):
        # Capture the sizes of the various sliding windows
        self._train_size = i_train_size
        self._test_size = i_test_size

        self._buffer_size = i_buffer_size
        self._metrics_size = self._buffer_size

        # Create the various sliding windows
        self._train_sw = SlidingWindow(self._train_size)
        self._test_sw = SlidingWindow(self._test_size)

        self._data_buffer = SlidingWindow(self._buffer_size)
        self._metrics_buffer = SlidingWindow(self._buffer_size)

        # Set the initial state of the window manager
        self._train_sample_count = 0
        self._is_pre_training = True
        self._pre_test_sample_count = 0
        self._is_pre_testing = False

        # Register event handlers
        self._register_handlers()


        '''
        Perhaps these are better variable names...

        TODO... Update once Algo text version 1 is available.

        # Initial training First X samples where Y are assumed to be known
        self._init_train_sample_count = 0
        self._init_test_sample_count = 0
        self.is_init_training = True
        self.is_init_testing = False

        # After the initial model has been trained.
        self._train_sample_count = 0
        self._test_sample_count = 0
        self._is_trained = False
        '''


    @property
    def is_pre_testing(self):
        return self._is_pre_testing

    @property
    def is_pre_training(self):
        return self._is_pre_training

    @property
    def train_sample_count(self):
        return self._train_sample_count

    @property
    def pre_test_sample_count(self):
        return self._pre_test_sample_count

    def _register_handlers(self):
        self._train_sw.subscribe('on_pre_train_one', self._inc_train_sample_count)
        self._train_sw.subscribe('on_pre_train_one', self._pre_train_one)
        self._train_sw.subscribe('on_pre_train_finished', self._on_pre_train_finished)
        self._test_sw.subscribe('on_pre_test_one', self._on_pre_test_one)
        self._test_sw.subscribe('on_pre_test_one', self._inc_pre_train_sample_count)
        self._test_sw.subscribe('on_pre_test_finished', self._on_pre_test_finished)

    def _pre_train_one(self, *args, **kwargs):
        x = kwargs['x']
        y = kwargs['y']
        print(f'New pre-training instance - x: {x}, y: {y}')
        if self.train_sample_count >= self._train_size:
            self._train_sw.trigger('on_pre_train_finished', is_pre_train=False, is_pre_test=True)

    def _inc_pre_train_sample_count(self, *args, **kwargs):
        if self.is_pre_testing:
            self._pre_test_sample_count += 1

    def _inc_train_sample_count(self, *args, **kwargs):
        if self.is_pre_training:
            self._train_sample_count += 1

    def _on_pre_train_finished(self, *args, **kwargs):
        self._is_pre_training = kwargs['is_pre_train']
        self._is_pre_testing = kwargs['is_pre_test']

    def _on_pre_test_finished(self, *args, **kwargs):
        self._is_pre_testing = False

    def add_one(self, x, y):
        # Are we in initial-training mode?
        if self.is_pre_training:
            self._train_sw.trigger('on_pre_train_one', x=x, y=y)
        # Are we in initial-testing mode ?
        if self._is_pre_testing:
            self._test_sw.trigger('on_pre_test_one', x=x, y=y)

    def _on_pre_test_one(self, *args, **kwargs):
        x = kwargs['x']
        y = kwargs['y']
        print(f'new pre-testing instance - x : {x}, y: {y}')
        if self.pre_test_sample_count >= self._test_size:
            self._test_sw.trigger('on_pre_test_finished')

    def _get_one(self):
        pass

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
