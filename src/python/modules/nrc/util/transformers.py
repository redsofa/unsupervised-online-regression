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
        return self._transformed_data

    @property
    def transformed_data(self):
        return self._transformed_data

    @abstractmethod
    def transform(self):
        pass

class AbstractDepVarTransformer(AbstractTransformer):
    @property
    def dep_var(self):
        return self._data

    @dep_var.setter
    def dep_var(self, x):
        self._data = []
        self._data.append(x)

class DepVaritoInstanceTransformer(AbstractDepVarTransformer):
    def transform(self):
        self._transformed_data = {}
        x = []
        x.append(list(self._data[0].values()))
        self._transformed_data['x'] = np.array(x)
        self._transformed_data['y'] = None


class AbstractListTransformer(AbstractTransformer):
    @property
    def samples(self):
        return self._data

    @samples.setter
    def samples(self, samples):
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
        self._transformed_data['y'] = np.array(y)


if __name__ == '__main__':
    pass
