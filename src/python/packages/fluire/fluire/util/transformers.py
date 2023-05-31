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
        # Incoming data looks like :
        #
        # x : {'c1': 1.0, 'c2': 2.0}
        # y : 23
        #
        # Need to convert it to a dictionary that looks like:
        # {'x': array([1., 2.]), 'y': array([23])}
        x_np_arr = np.array(list(x.values()))
        y_np_arr = np.array([y])

        return {'x': x_np_arr, 'y': y_np_arr}

    @staticmethod
    def xy_pred_to_numpy_dictionary(x, y):
        if type(y[0]) == np.ndarray:
            y = y[0]
        else:
            y = np.array(y)

        return {'x': x[0], 'y': y}


if __name__ == '__main__':
    pass
