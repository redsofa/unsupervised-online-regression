import argparse
import time
from nrc.factories.stream import StreamFactory
from nrc.models.runner import ModelRunner
from nrc.settings.default_params import *
from nrc.util.stream import *
from nrc.util.window import TrainTestWindow, DataBuffer
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def arrs_to_df(x_arr, y_pred_arr, y_true_arr):
    ret_val = pd.DataFrame({'x': x_arr, 'y_pred': y_pred_arr, 'y_true': y_true_arr}, columns=['x', 'y_pred', 'y_true'])
    return ret_val

def get_args():
    parser = argparse.ArgumentParser(description="Unsupervised, online regression modeling.")
    parser.add_argument('-1', '--input_stream_file', type=str, required=False, default=DEFAULT_INPUT_STREAM_FILE, help="Input file (csv).")
    parser.add_argument('-2', '--stream_parameter_file', type=str, required=False, default=DEFAULT_STREAM_PARAMETER_FILE, help='Stream configuration file.')
    parser.add_argument('-3', '--train_samples', type=int, required=False, default=DEFAULT_TRAIN_SAMPLES, help='Number of training samples to use.')
    parser.add_argument('-4', '--test_samples', type=int, required=False, default=DEFAULT_TEST_SAMPLES, help='Number of test samples to use.')
    parser.add_argument('-5', '--buffer_size', type=int, required=False, default=DEFAULT_BUFFER_SIZE, help='Data buffer size to use.')
    parser.add_argument('-6', '--max_samples', type=int, required=False, default=DEFAULT_MAX_SAMPLES, help='Max Number of samples to process.')
    parser.add_argument('-7', '--delta_threshold', type=float, required=False, default=DEFAULT_DELTA_THRESHOLD, help='Evaluation metrics difference threshold.')
    parser.add_argument('-8', '--output_csv_file', type=str, required=False, default=DEFAULT_OUTPUT_FILE, help='Default output CSV file.')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    # Array of models to run.
    model_name = 'sklearn_linear_regression_model'
    # stream_params specifies how to transform the input data stream features and which column is
    # the target variable.
    stream_params = load_stream_params(args.stream_parameter_file)
    # Get the datastream
    data_stream = StreamFactory.get_csv_stream(args.input_stream_file, **stream_params)

    # Configure a TrainTest_Window instance
    tt_win = TrainTestWindow(args.train_samples, args.test_samples)

    # Configure the buffer
    buffer = DataBuffer(args.buffer_size)

    x_arr = []
    y_pred_arr = []
    y_true_arr = []

    # Configure the ModelRunner instance
    m_run = ModelRunner(model_name)
    m_run.set_train_test_window(tt_win)\
        .set_data_stream(data_stream)\
        .set_max_samples(args.max_samples)\
        .set_buffer(buffer)\
        .set_threshold(args.delta_threshold)

    # Run the model
    for x, y_pred, y_true in m_run.run():
        x_arr.append(x[0])
        y_pred_arr.append(y_pred[0][0])
        y_true_arr.append(y_true)

    p_df = arrs_to_df(x_arr, y_pred_arr, y_true_arr)
    p_df.to_csv(args.output_csv_file, index=False)

    # Calculate MSE and RMSE values
    mse = mean_squared_error(p_df.y_true.values, p_df.y_pred.values)
    print(f'MSE : {mse}')

    #  Setting squared to False will return the RMSE.
    rmse = mean_squared_error(p_df.y_true.values, p_df.y_pred.values, squared=False)
    print(f'RMSE : {rmse}')

    mae = mean_absolute_error(p_df.y_true.values, p_df.y_pred.values)
    print(f'MAE : {mae}')

    r2 = r2_score(p_df.y_true.values, p_df.y_pred.values)
    print(f'R2 : {r2}')

    print(f'Model run time: {m_run.run_time}')

    print('Results file saved')

if __name__ == '__main__':
    main()
