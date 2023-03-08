import argparse
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def get_args():
    parser = argparse.ArgumentParser(description="Plot unsupervised, online regression modeling results.")
    parser.add_argument('-1', '--input_results_file', type=str, required=True)
    parser.add_argument('-2', '--output_plots_file', type=str, required=False)
    args = parser.parse_args()
    return args


def pred_true_plot(pdf, file_name):
    pdf.insert(0, 'step', range(0, len(pdf)))
    plt.figure(figsize=(10, 8))
    plt.plot(
        pdf['step'].values, pdf['y_pred'].values, 'r--', 
        pdf['step'].values, pdf['y_true'].values, 'g--'
    )
    plt.legend(['y_pred', 'y_true'])
    plt.savefig(file_name)



def main():
    args = get_args()

    print()
    print('Program Arguments')
    for key, value in vars(args).items():
        print (f'{key} - {value}')

    print()

    print(f'Reading input file : {args.input_results_file}')
    p_df = pd.read_csv(args.input_results_file)

    print()
    print('Print results file header')
    print(p_df.head(10))
    print()
    print('Metrics Calculations')

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

    pred_true_plot(p_df, args.output_plots_file)


if __name__ == '__main__':
    main()
