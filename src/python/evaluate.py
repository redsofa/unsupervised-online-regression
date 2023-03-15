import argparse
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from nrc.settings.default_params import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_OUTPUT_PREDICTIONS_FILE,
    DEFAULT_OUTPUT_STATS_FILE,
    DEFAULT_OUTPUT_PLOT_FILE,
    DEFAULT_OUTPUT_DRIFTS_CSV_FILE
)
from nrc.util.files import mkdir_structure


def get_args():
    parser = argparse.ArgumentParser(
        description="Plot unsupervised, online regression modeling results."
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
        default=DEFAULT_OUTPUT_PREDICTIONS_FILE,
        help="Predictions output CSV file for this script.",
    )
    parser.add_argument(
        "-3",
        "--stats_file",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_STATS_FILE,
        help="File name for the output statistics",
    )
    parser.add_argument(
        "-4",
        "--plot_file",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_PLOT_FILE,
        help="File name for the output statistics",
    )
    parser.add_argument(
        "-5",
        "--drift_file",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_DRIFTS_CSV_FILE,
        help="Detected drift location CSV file (indices are relative to predictions csv file.)",
    )
    args = parser.parse_args()
    return args


def pred_true_plot(pred_df, drift_df, file_name):
    pred_df.insert(0, "step", range(0, len(pred_df)))
    plt.figure(figsize=(10, 8))
    plt.plot(
        pred_df["step"].values,
        pred_df["y_true"].values,
        "g:",
        pred_df["step"].values,
        pred_df["y_pred"].values,
        "b--",
    )
    # add drift markers to plot
    for e in drift_df.values:
        plt.axvline(e[0], color="red", linestyle="dashdot")
    plt.legend(["y_pred", "y_true", "drift"])
    plt.savefig(file_name)


def main():
    args = get_args()
    mkdir_structure(args.output_dir)

    stats_file = f"{args.output_dir}/{args.stats_file}"
    pred_csv_file = f"{args.output_dir}/{args.predictions_file}"
    plot_file = f'{args.output_dir}/{args.plot_file}'
    drift_csv_file = f'{args.output_dir}/{args.drift_file}'

    print(f"Reading input file : {pred_csv_file}")
    pred_df = pd.read_csv(pred_csv_file)
    drift_df = pd.read_csv(drift_csv_file)

    min_y_true = pred_df.y_true.min()
    max_y_true = pred_df.y_true.max()

    with open(stats_file, "a") as f:
        f.write("\n\nPrediction Metrics :\n")
        # Calculate MSE and RMSE values
        mse = mean_squared_error(pred_df.y_true.values, pred_df.y_pred.values)
        f.write(f"MSE : {mse}\n")

        #  Setting squared to False will return the RMSE.
        rmse = mean_squared_error(pred_df.y_true.values, pred_df.y_pred.values, squared=False)
        f.write(f"RMSE : {rmse}\n")

        mae = mean_absolute_error(pred_df.y_true.values, pred_df.y_pred.values)
        f.write(f"MAE : {mae}\n")

        r2 = r2_score(pred_df.y_true.values, pred_df.y_pred.values)
        f.write(f"R2 : {r2}\n")
        f.write('\n')

        f.write(f'Min y_true : {min_y_true} - Max y_true : {max_y_true}\n')

    print("Results files updated")

    pred_true_plot(pred_df, drift_df, plot_file)


if __name__ == "__main__":
    main()
