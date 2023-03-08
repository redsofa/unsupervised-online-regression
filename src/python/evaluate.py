import argparse
import time
from nrc.factories.stream import StreamFactory
from nrc.models.runner import ModelRunner
from nrc.settings.default_params import *
from nrc.util.stream import *
from nrc.util.window import TrainTestWindow, DataBuffer
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error

def get_args():
    parser = argparse.ArgumentParser(description="Plot unsupervised, online regression modeling results.")
    parser.add_argument('-1', '--input_results_file', type=str, required=True)
    parser.add_argument('-2', '--output_plots_file', type=str, required=False)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    print(f'Reading input file : {args.input_results_file}')
    p_df = pd.read_csv(args.input_results_file)

    print(p_df.head(10))

    # Calculate MSE and RMSE values
    mse = mean_squared_error(p_df.y_true.values, p_df.y_pred.values)
    print(f'MSE : {mse}')
    #  Setting squared to False will return the RMSE.
    rmse = mean_squared_error(p_df.y_true.values, p_df.y_pred.values, squared=False)
    print(f'RMSE : {rmse}')

if __name__ == '__main__':
    main()
