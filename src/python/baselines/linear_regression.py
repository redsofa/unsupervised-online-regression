import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from fluire.util.files import mkdir_structure
import os
import argparse


DEFAULT_RAW_DATA_DIR = '/Users/richardr/data/usup_reg/raw/uci/protein'
DEFAULT_OUTPUT_DIR = '/Users/richardr/data/usup_reg/work/uci/protein'
DEFAULT_INPUT_CSV_FILE = 'CASP.csv'
DEFAULT_OUTPUT_PREDICTIONS_FILE = 'CASP_batch_predictions.csv'
DEFAULT_OUTPUT_STATS_FILE = 'CASP_batch_stats.txt'
DEFAULT_TRAIN_SAMPLES = 100
DEFAULT_TEST_SAMPLES = 20
DEFAULT_X_COL_INDICES = "1,2,3,4,5,6,7,8,9"
DEFAULT_Y_COL_INDEX = "0"


def get_args():
    parser = argparse.ArgumentParser(
        description="Baseline regression modeling."
    )
    parser.add_argument(
        "-1",
        "--raw_data_dir",
        type=str,
        required=False,
        default=DEFAULT_RAW_DATA_DIR,
        help="Root of input files directory for this script.",
    )
    parser.add_argument(
        "-2",
        "--output_dir",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_DIR,
        help="Root of output files directory for this script.",
    )
    parser.add_argument(
        "-3",
        "--input_csv_file",
        type=str,
        required=False,
        default=DEFAULT_INPUT_CSV_FILE,
        help="Input CSV file for this script.",
    )
    parser.add_argument(
        "-4",
        "--output_predictions_file",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_PREDICTIONS_FILE,
        help="Predictions output CSV file for this script.",
    )
    parser.add_argument(
        "-5",
        "--output_stats_file",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_STATS_FILE,
        help="File name for the output statistics",
    )
    parser.add_argument(
        "-6",
        "--train_samples",
        type=int,
        required=False,
        default=DEFAULT_TRAIN_SAMPLES,
        help="Number of training samples to use.",
    )
    parser.add_argument(
        "-7",
        "--test_samples",
        type=int,
        required=False,
        default=DEFAULT_TEST_SAMPLES,
        help="Number of test samples to use.",
    )
    parser.add_argument(
            "-8",
            "--x_col_indices",
            type=lambda s: [int(item) for item in s.split(',')],
            required=False,
            default=DEFAULT_X_COL_INDICES,
            help='X column indices',
    )
    parser.add_argument(
            "-9",
            "--y_col_index",
            type=lambda s: [int(item) for item in s.split(',')],
            required=False,
            default=DEFAULT_Y_COL_INDEX,
            help='y column index',
    )
    args = parser.parse_args()
    return args


def arrs_to_df(x_arr, y_pred_arr, y_true_arr):
    ret_val = pd.DataFrame(
        {"x": x_arr, "y_pred": y_pred_arr, "y_true": y_true_arr},
        columns=["x", "y_pred", "y_true"],
    )
    return ret_val


def main():
    args = get_args()
    # Create the output directory if it does not exit.
    mkdir_structure(args.output_dir)

    # Store fully qualified names of files that are used in this script
    input_csv_file = f"{args.raw_data_dir}/{args.input_csv_file}"
    output_pred_csv_file = f"{args.output_dir}/{args.output_predictions_file}"

    train_and_test_instances = args.train_samples + args.test_samples

    # Load source file into pandas dataframe (pdf for short)
    pdf = pd.read_csv(input_csv_file)

    total_instances = pdf.shape[0]
    non_train_and_test_instances = total_instances - train_and_test_instances

    # Train and test split of the initial instance data
    train_pdf = pdf.iloc[:args.train_samples]
    test_pdf = pdf.iloc[args.train_samples:train_and_test_instances]

    train_X = train_pdf.iloc[:, args.x_col_indices].values
    train_y = train_pdf.iloc[:, args.y_col_index].values

    test_X = test_pdf.iloc[:, args.x_col_indices].values
    test_y = test_pdf.iloc[:, args.y_col_index].values

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(train_X, train_y)

    # Make predictions using the testing set
    pred_y = regr.predict(test_X)

    # Ignore this...
    # The coefficients (FROM TRAINING)
    # print("Coefficients: \n", regr.coef_)
    # The mean squared error
    # print("Mean squared error: %.2f" % mean_squared_error(test_y, pred_y))
    # The coefficient of determination: 1 is perfect prediction
    # print("Coefficient of determination: %.2f" % r2_score(test_y, pred_y))

    # make predictions on the rest of the data
    non_train_or_test_pdf = pdf.iloc[train_and_test_instances:total_instances]
    rest_X = non_train_or_test_pdf.iloc[:, args.x_col_indices].values
    rest_y = non_train_or_test_pdf.iloc[:, args.y_col_index].values

    pred_rest_y = regr.predict(rest_X)
    print("Mean squared error: %.2f" % mean_squared_error(rest_y, pred_rest_y))
    # The coefficient of determination: 1 is perfect prediction
    print("R2 score : %.2f" % r2_score(rest_y, pred_rest_y))

    pred_pdf = arrs_to_df(rest_X.tolist(), pred_rest_y.flatten().tolist(), rest_y.flatten().tolist())
    pred_pdf.to_csv(output_pred_csv_file, index=False)


if __name__ == '__main__':
    main()




