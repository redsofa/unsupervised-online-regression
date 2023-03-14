import argparse
from nrc.factories.stream import StreamFactory
from nrc.models.runner import ModelRunner
from nrc.settings.default_params import (
    DEFAULT_RAW_DATA_DIR,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_INPUT_CSV_FILE,
    DEFAULT_INPUT_CSV_PARAMETERS_FILE,
    DEFAULT_OUTPUT_PREDICTIONS_FILE,
    DEFAULT_OUTPUT_STATS_FILE,
    DEFAULT_TRAIN_SAMPLES,
    DEFAULT_TEST_SAMPLES,
    DEFAULT_BUFFER_SIZE,
    DEFAULT_MAX_SAMPLES,
    DEFAULT_DELTA_THRESHOLD,
)
from nrc.util.stream import load_stream_params
from nrc.util.window import TrainTestWindow, DataBuffer
import pandas as pd
from nrc.util.files import mkdir_structure


def arrs_to_df(x_arr, y_pred_arr, y_true_arr):
    ret_val = pd.DataFrame(
        {"x": x_arr, "y_pred": y_pred_arr, "y_true": y_true_arr},
        columns=["x", "y_pred", "y_true"],
    )
    return ret_val


def get_args():
    parser = argparse.ArgumentParser(
        description="Unsupervised, online regression modeling."
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
        "--input_csv_param_file",
        type=str,
        required=False,
        default=DEFAULT_INPUT_CSV_PARAMETERS_FILE,
        help="Input CSV parameters file for this script.",
    )
    parser.add_argument(
        "-5",
        "--output_predictions_file",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_PREDICTIONS_FILE,
        help="Predictions output CSV file for this script.",
    )
    parser.add_argument(
        "-6",
        "--output_stats_file",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_STATS_FILE,
        help="File name for the output statistics",
    )
    parser.add_argument(
        "-7",
        "--train_samples",
        type=int,
        required=False,
        default=DEFAULT_TRAIN_SAMPLES,
        help="Number of training samples to use.",
    )
    parser.add_argument(
        "-8",
        "--test_samples",
        type=int,
        required=False,
        default=DEFAULT_TEST_SAMPLES,
        help="Number of test samples to use.",
    )
    parser.add_argument(
        "-9",
        "--buffer_size",
        type=int,
        required=False,
        default=DEFAULT_BUFFER_SIZE,
        help="Data buffer size to use.",
    )
    parser.add_argument(
        "-10",
        "--max_samples",
        type=int,
        required=False,
        default=DEFAULT_MAX_SAMPLES,
        help="Max Number of samples to process.",
    )
    parser.add_argument(
        "-11",
        "--delta_threshold",
        type=float,
        required=False,
        default=DEFAULT_DELTA_THRESHOLD,
        help="Evaluation metrics difference threshold.",
    )
    args = parser.parse_args()
    return args


def drift_handler(**kwargs):
    print(f'Drift detected at prediction number : {kwargs["prediction_count"]}')
    print(f'Value of d is : {kwargs["drift_indicator_value"]}')


def main():
    args = get_args()
    # Create the output directory if it does not exit.
    mkdir_structure(args.output_dir)

    # Array of models to run.
    model_name = "sklearn_linear_regression_model"

    # Store fully qualified names of files that are used in this script
    stream_params_file = f"{args.raw_data_dir}/{args.input_csv_param_file}"
    input_stream_file = f"{args.raw_data_dir}/{args.input_csv_file}"
    output_pred_csv_file = f"{args.output_dir}/{args.output_predictions_file}"
    output_stats_file = f"{args.output_dir}/{args.output_stats_file}"

    # stream_params specifies how to transform the input data stream features and which column is
    # the target variable. These settings are stored in a JSON file. Load the parameters from
    # file.
    stream_params = load_stream_params(stream_params_file)

    # Get the datastream
    data_stream = StreamFactory.get_csv_stream(input_stream_file, **stream_params)

    # Configure a TrainTest_Window instance
    tt_win = TrainTestWindow(args.train_samples, args.test_samples)

    # Configure the buffer
    buffer = DataBuffer(args.buffer_size)

    x_arr = []
    y_pred_arr = []
    y_true_arr = []

    # Configure the ModelRunner instance
    m_run = ModelRunner(model_name)
    m_run.set_train_test_window(tt_win).set_data_stream(data_stream).set_max_samples(
        args.max_samples
    ).set_buffer(buffer).set_threshold(args.delta_threshold).set_drift_handler(
        drift_handler
    )

    # Run the model
    for x, y_pred, y_true in m_run.run():
        x_arr.append(x[0].tolist())
        y_pred_arr.append(y_pred[0][0])
        y_true_arr.append(y_true)

    p_df = arrs_to_df(x_arr, y_pred_arr, y_true_arr)
    p_df.to_csv(output_pred_csv_file, index=False)

    with open(output_stats_file, "w") as f:
        f.write("Program Arguments :\n\n")
        for key, value in vars(args).items():
            f.write(f"{key} : {value}\n")
        f.write("\n")
        f.write(f"Model run time : {m_run.run_time}\n")
        f.write(f"Prediction count : {len(y_pred_arr)}")

    print("Results files saved")


if __name__ == "__main__":
    main()
