import argparse
import pandas as pd
from distutils.util import strtobool
import matplotlib.pyplot as plt
from fluire.util.files import mkdir_structure

DEFAULT_INPUT_DIR = '/Users/richardr/data/usup_reg/work/z1_z2_only/lr/protein/2023_08_08__14_47_22'
DEFAULT_OUTPUT_DIR = '/tmp'
DEFAULT_PREDICTIONS_FILE = 'protein_predictions.csv'
DEFAULT_DRIFTS_FILE = 'protein_drifts.csv'


def get_args():
    parser = argparse.ArgumentParser(
        description="Plot unsupervised, online regression modeling results."
    )
    parser.add_argument(
        '-0',
        '--input_dir',
        type=str,
        required=False,
        default=DEFAULT_INPUT_DIR,
        help='Root of input file directory for this script.'
    )
    parser.add_argument(
        "-1",
        "--output_dir",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_DIR,
        help="Root of output files directory for this script.",
    )
    parser.add_argument(
        "-2",
        "--predictions_file",
        type=str,
        required=False,
        default=DEFAULT_PREDICTIONS_FILE,
        help="Predictions output CSV file for this script.",
    )
    parser.add_argument(
        "-3",
        "--drift_file",
        type=str,
        required=False,
        default=DEFAULT_DRIFTS_FILE,
        help="Detected drift location CSV file (indices are relative to predictions csv file.)",
    )
    args = parser.parse_args()
    return args


def y_true_plot(pred_df, file_name, title):
    copy_df = pred_df.copy(deep=True)
    copy_df.insert(0, "step", range(0, len(copy_df)))
    plt.figure(figsize=(20, 12))
    plt.ticklabel_format(style='plain')
    train_df = copy_df[copy_df['is_train_data'] == True]
    plt.scatter(
        train_df["step"].values,
        train_df["y_true"].values,
        color='red',
        s=1)
    y_true_df = copy_df[copy_df['is_train_data'] == False]
    plt.scatter(
        y_true_df["step"].values,
        y_true_df["y_true"].values,
        color='green',
        s=1
    )
    plt.axvline(train_df.shape[0], color="black", linestyle="dashdot")
    # plt.text(train_df.shape[0] - 10, 0, 'Initial train \n and test data', rotation=90)
    plt.title(title)
    plt.legend(["initial_data", "y_true", "Initial Data Mark"])
    plt.savefig(file_name)


def y_pred_plot(pred_df, drift_df, file_name, title):
    copy_df = pred_df.copy(deep=True)
    copy_df.insert(0, "step", range(0, len(copy_df)))
    plt.figure(figsize=(20, 12))
    plt.ticklabel_format(style='plain')
    train_df = copy_df[copy_df['is_train_data'] == True]
    plt.scatter(
        train_df["step"].values,
        train_df["y_true"].values,
        color='red',
        s=1)
    y_true_df = copy_df[copy_df['is_train_data'] == False]
    plt.scatter(
        y_true_df["step"].values,
        y_true_df["y_pred"].values,
        color='blue',
        s=1
    )
    plt.axvline(train_df.shape[0], color="black", linestyle="dashdot")
    # plt.text(train_df.shape[0] - 10, 0, 'Initial train \n and test data', rotation=90)
    for e in drift_df.values:
        plt.axvline(e[0], color="orange", linestyle="dashdot", ymin=0, ymax=0.1)

    plt.title(title)
    plt.legend(["Initial Data", "y_pred", "Initial Data Mark" ,"Model Retrain Mark"])
    plt.savefig(file_name)


def y_pred_y_true_plot(pred_df, drift_df, file_name, title):
    copy_df = pred_df.copy(deep=True)
    copy_df.insert(0, "step", range(0, len(copy_df)))
    plt.figure(figsize=(20, 12))

    plt.ticklabel_format(style='plain')
    train_df = copy_df[copy_df['is_train_data'] == True]
    plt.scatter(
            train_df["step"].values,
            train_df["y_true"].values,
            color='red',
            s=1)
    y_true_df = copy_df[copy_df['is_train_data'] == False]
    plt.scatter(
            y_true_df["step"].values,
            y_true_df["y_pred"].values,
            color='blue',
            s=1
    )
    plt.scatter(
        y_true_df["step"].values,
        y_true_df["y_true"].values,
        color='green',
        s=1
    )
    plt.axvline(train_df.shape[0], color="black", linestyle="dashdot")

    # plt.text(train_df.shape[0] - 10, 0, 'Initial train \n and test data', rotation=90)
    for e in drift_df.values:
        plt.axvline(e[0], color="orange", linestyle="dashdot", ymin=0, ymax=0.1)

    plt.title(title)
    plt.legend(["Initial Data", "y_pred", "y_true", "Initial Data Mark" ,"Model Retrain Mark"])
    plt.savefig(file_name)


def main():
    args = get_args()
    mkdir_structure(args.output_dir)

    pred_csv_file = f"{args.input_dir}/{args.predictions_file}"
    drift_csv_file = f'{args.input_dir}/{args.drift_file}'

    print(f"Reading input file : {pred_csv_file}")
    pred_df = pd.read_csv(pred_csv_file)
    drift_df = pd.read_csv(drift_csv_file)

    y_true_plot(pred_df,
                f'{args.output_dir}/y_true_plot.png',
                f'y_true plot of : \n {pred_csv_file}\n')

    y_pred_plot(pred_df,
                drift_df,
                f'{args.output_dir}/y_pred_plot.png',
                f'y_pred plot of : \n {pred_csv_file}\n')

    y_pred_y_true_plot(pred_df,
                       drift_df,
                       f'{args.output_dir}/y_pred_y_true_plot.png',
                       f'y_pred and y_true plot of : \n {pred_csv_file}\n')


if __name__ == "__main__":
    main()
