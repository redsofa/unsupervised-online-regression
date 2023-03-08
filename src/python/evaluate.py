import argparse
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


def get_args():
    parser = argparse.ArgumentParser(description="Plot unsupervised, online regression modeling results.")
    parser.add_argument('-1', '--input_results_file', type=str, required=True)
    parser.add_argument('-2', '--output_plots_file', type=str, required=False)
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    print()
    print('Program Arguments')
    for key, value in vars(args).items():
        print (f'{key} - {value}')

    print()

    print(f'Reading input file : {args.input_results_file}')
    p_df = pd.read_csv(args.input_results_file)

    print(p_df.head(10))

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


if __name__ == '__main__':
    main()
