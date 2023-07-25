from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
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


def arr_dict_to_xy(xy_list):
    x = []
    y = []
    for e in xy_list:
        x.append(e['X'].tolist())
        y.append(e['y'].tolist())
    return (x, y)


def trans_xy_arr_to_dict(X, y):
    # Transform the input data.
    # Incoming data looks like :
    #
    # x : [0.2, 0.1, etc...]
    # y : 2.2
    #
    # Need to convert it to a dictionary that looks like:
    # {'X': array([1., 2.]), 'y': array([23])}
    #
    ret_val = {'X': np.array(X), 'y': np.array(y)}
    return ret_val


def main() -> None:

    # Instantiate the model we will be using.
    model = SGDRegressor()

    # Create a sliding window object.
    sliding_window = Window(max_len=80, slides=True)

    # Create a buffer object.
    buffer = Window(max_len=20, slides=False)

    # Generate a regression dataset with 2 input features
    X, y, w = make_regression(n_features=2, n_samples=4000,
                              random_state=42, coef=True, noise=0.1)

    print(f'Length of the X and Y collections : {len(X)}, {len(y)}')

    # Store the initial 100 samples in a i_X and i_y variables
    i_X = X[0:100]  # Slice the collection from index 0 to 100. Excludes the end index.
    i_y = y[0:100]  # Slice the collection from index 0 to 100. Excludes the end index.

    print(f'Length of the initial X collection : {len(i_X)}')
    print(f'Length of the initial y collection : {len(i_y)}')

    # Train/test split of the initial data is 80/20
    i_X_train, i_X_test, i_y_train, i_y_test = train_test_split(i_X, i_y,
                                                                test_size=0.2,
                                                                random_state=42
                                                                )
    # Fill the sliding window with the intial training data.
    for i, x in enumerate(i_X_train):
        sample = trans_xy_arr_to_dict(x, [i_y_train[i]])
        sliding_window.add_data(sample)

    print(f'Length of the initial sliding window : {sliding_window.len}')

    # Fit model on a batch that consists of the batch of initial training data
    model.partial_fit(i_X_train, i_y_train)

    # At this point we have a model that has been incrementally trained on
    # 80 data points. We can use the model to make predictions and get
    # a RMSE value.
    y_preds = model.predict(i_X_test)

    Z1 = mean_squared_error(i_y_test, y_preds, squared=False)

    print(f'Z1 value : {Z1}')

    r_X = X[100:]  # Slice collection from index 100 to the end.
    r_y = y[100:]  # Slice collection from index 100 to the end.

    print(f'Length of the remainder of the X collection : {len(r_X)}')
    print(f'Length of the remainder of the y collection : {len(r_y)}')

    # We can now iterate throught the rest of the data and do
    # a prediction, record that prediction as the true value and do a
    # partial_fit.
    for i, x in enumerate(r_X):
        # Make one prediction.
        y_pred = model.predict([x])
        sample = trans_xy_arr_to_dict(x, y_pred)

        # Add prediction to sliding window and remove oldest sample.
        sliding_window.get_and_remove_oldest()
        sliding_window.add_data(sample)

        # Add the prediction to the buffer.
        buffer.add_data(sample)

        # Use y_pred as the true value and call partial_fit.
        # model.partial_fit([x], y_pred)

        if buffer.is_full:
            print()
            print('Buffer is full')
            sw_x, sw_y = arr_dict_to_xy(sliding_window.get_as_list())

            # The sliding window has the buffer contents. Remove these from this collection.
            x_train = sw_x[:-buffer.len]
            y_train = sw_y[:-buffer.len]
            # print(f'Length of x_train and y_train : {len(x_train)}, {len(y_train)}')

            x_test, y_test = arr_dict_to_xy(buffer.get_as_list())

            # print(f'Lentgh of x_test and y_test : {len(x_test)}, {len(y_test)}')

            print('Partially fitting on the sliding window (chunked)')
            print()

            model.partial_fit(x_train, np.ravel(y_train))
            y_pred = model.predict(x_test)
            Z2 = mean_squared_error(y_test, y_pred, squared=False)
            print(f'Z2 value : {Z2}')
            #  TODO.. Decide to do ... partial fit updates the model probably... 
            buffer.clear_contents()


if __name__ == "__main__":
    main()
