from queue import Queue
from nrc.util.observable import IObservable, IObserver
from collections import defaultdict

'''
TODO:

    May need buffer object that contains multiple sliding windows
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
class BufferManager:
    def __init__(self, i_train_size, i_test_size, i_buffer_size):
        self._pre_train_train_buffer_size = i_train_size
        self._pre_train_test_buffer_size = i_test_size
        self._pre_train_size = i_train_size + i_test_size

        self._buffer_size = i_buffer_size
        self._metrics_collection_size = self._buffer_size

        self._pre_train_train_buffer = SlidingWindow(self._pre_train_train_buffer_size)
        self._pre_train_test_buffer = SlidingWindow(self._pre_train_test_buffer_size)

        self._post_train_data_buffer = SlidingWindow(self._buffer_size)
        self._metrics_buffer = SlidingWindow(self._buffer_size)

        self._pre_train_train_buffer.subscribe('on_add_ptb', self.bla)

    def bla(self, *args, **kwargs):
        print('bla dude')
        print(kwargs)

    def add_one(self, x, y):
        self._pre_train_train_buffer.trigger('on_add_ptb', x=x, y=y)



class SlidingWindow(IObservable):
    def __init__(self, i_buffer_size):
        self._init_size = i_buffer_size
        self._queue = Queue(i_buffer_size)
        self._observers = defaultdict(list)

    def subscribe(self, event_type, fn):
        self._observers[event_type].append(fn)

    def unsubscribe(self, event_type, fn):
        for f in self._observers[event_type]:
            if f == fn :
                self._observers[event_type].remove(f)

    def trigger(self, event_type, *args, **kwargs):
        for fn in self._observers[event_type]:
            fn(event_type, *args, **kwargs)

    def clear_contents(self):
        while not self._queue.empty():
            self._queue.get()

    def len(self):
        return self._queue.qsize()

    def add_data(self, i_data):
        if self.len() < self._init_size:
            self._queue.put(i_data)
        else:
            self._queue.get()
            self._queue.put(i_data)

    def get_data(self):
        return self._queue.get()


if __name__ == '__main__':
    pass
