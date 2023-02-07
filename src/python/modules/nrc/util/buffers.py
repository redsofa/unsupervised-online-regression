from queue import Queue


class SlidingWindow:

    def __init__(self, i_buffer_size):
        self._init_size = i_buffer_size
        self._queue = Queue(i_buffer_size)

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
