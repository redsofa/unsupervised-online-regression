from abc import ABC, abstractmethod
import numpy as np

class AbstractTransformer(ABC):
    def __init__(self):
        self._data = None
        self._transformed_data = None

    @property
    def data(self):
        return self._data

    def execute(self):
        self.transform()

    @property
    def transformed_data(self):
        return self._transformed_data

    @abstractmethod
    def transform(self): pass


class AbstractSampleTransformer(AbstractTransformer):
    def set_one_sample(self, x, y):
        _tmp = {'x':x, 'y':y }
        self._data = _tmp


class AbstractListTransformer(AbstractTransformer):
    def set_samples(self, samples):
        self._data = samples


class ListToScikitLearnTransformer(AbstractListTransformer):
    def transform(self):
        self._transformed_data = {}
        x = []
        y = []

        for e in self._data:
            x.append(list(e['x'].values()))
            y.append(e['y'])

        self._transformed_data['x'] = np.array(x)
        self._transformed_data['y'] = np.array([y])


class RiverToScikitLearnSampleTransformer(AbstractSampleTransformer):
    def transform(self):
        self._transformed_data = {}
        self._transformed_data['x'] = np.array([list(self._data['x'].values())])
        self._transformed_data['y'] = np.array([self._data['y']])


if __name__ == '__main__':
    pass
