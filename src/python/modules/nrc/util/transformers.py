from abc import ABC, abstractmethod
import numpy as np


class XYTransformers():
    @staticmethod
    def arr_dict_to_xy(xy_list):
        x = []
        y = []
        for e in xy_list:
            x.append(e['x'])
            y.append(e['y'])
        return (x, y)

    @staticmethod
    def xy_to_numpy_dictionary(x, y):
        xy_dict = {'x': x, 'y': {'y1': y}}
        x = np.array(list(xy_dict['x'].values()))
        y = np.array(list(xy_dict['y'].values()))
        return {'x': x, 'y': y}

    @staticmethod
    def xy_pred_to_numpy_dictionary(x, y):
        return {'x': x[0], 'y': y[0]}


if __name__ == '__main__':
    pass
