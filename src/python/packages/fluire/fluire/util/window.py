from collections import deque


class Window():
    def __init__(self, max_len, slides=False):
        self._max_len = max_len
        self._data = deque(maxlen=max_len)
        self._slides = slides

    def clear_contents(self):
        self._data.clear()

    def get_element_at(self, index):
        try:
            return self._data[index]
        except IndexError:
            raise Exception('Element index out of range.')

    @property
    def max_len(self):
        return self._max_len

    @property
    def len(self):
        return len(self._data)

    @property
    def is_full(self):
        return self.len == self._max_len

    def add_data(self, i_data):
        if not self._slides:
            if self.len == self._max_len:
                raise Exception('End of Window reached. Not a sliding window.')
            else:
                self._data.append(i_data)
        else:
            self._data.append(i_data)

    def get_as_list(self):
        return list(self._data)

    def get_and_remove_oldest(self):
        if self.len > 0:
            return self._data.popleft()
        else:
            return None


if __name__ == '__main__':
    pass
