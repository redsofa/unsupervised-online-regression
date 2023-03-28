import argparse
from fluire.factories.stream import StreamFactory
from fluire.models.runner import ModelRunner
from fluire.util.scalers import RiverStandardScalerWrapper
from fluire.settings.default_params import (
    DEFAULT_RAW_DATA_DIR,
    DEFAULT_OUTPUT_DRIFTS_CSV_FILE,
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
from fluire.util.stream import load_stream_params
from fluire.util.window import TrainTestWindow, DataBuffer
import pandas as pd
from fluire.util.files import mkdir_structure
from functools import partial


def drift_to_df(drift_arr):
    ret_val = pd.DataFrame(
            {
                "location": [e[0] for e in drift_arr],
                "delta": [e[1] for e in drift_arr]
            }, columns=["location", "delta"]
    )
    return ret_val


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
    parser.add_argument(
        "-12",
        "--output_drifts_csv_file",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_DRIFTS_CSV_FILE,
        help="Detected drift location CSV file (indices are relative to predictions csv file.)",
    )
    args = parser.parse_args()
    return args


def model_retrained_handler(*args, **kwargs):
    count_dict = args[0]
    count_dict['count'] += 1
    # Make sure the model memory address changes
    # print(kwargs['model'])


def drift_handler(*args, **kwargs):
    # The args arguments come from the utilization of a partial function definition
    drift_arr = args[0]
    # The kwargs come from the handler code call inside the model runner
    drift_arr.append([kwargs['prediction_count'], kwargs['drift_indicator_value']])


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
    output_drift_csv_file = f"{args.output_dir}/{args.output_drifts_csv_file}"
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
    drift_arr = []
    retrain_count = {'count': 0}

    partial_drift_fn = partial(drift_handler, drift_arr)
    partial_retrain_fn = partial(model_retrained_handler, retrain_count)

    # For online standardization
    riv_scaler = RiverStandardScalerWrapper()

    # Configure the ModelRunner instance
    m_run = ModelRunner(model_name)
    m_run.set_train_test_window(tt_win)\
        .set_data_stream(data_stream)\
        .set_max_samples(args.max_samples)\
        .set_buffer(buffer)\
        .set_threshold(args.delta_threshold)\
        .set_drift_handler(partial_drift_fn)\
        .set_model_retrained_handler(partial_retrain_fn)

    # Run the model
    for x, y_pred, y_true in m_run.run():
        x_arr.append(x[0].tolist())
        y_pred_arr.append(y_pred[0][0])
        y_true_arr.append(y_true)

    p_df = arrs_to_df(x_arr, y_pred_arr, y_true_arr)
    p_df.to_csv(output_pred_csv_file, index=False)

    p_df = drift_to_df(drift_arr)
    p_df.to_csv(output_drift_csv_file, index=False)

    with open(output_stats_file, "w") as f:
        f.write("Program Arguments :\n\n")
        for key, value in vars(args).items():
            f.write(f"{key} : {value}\n")
        f.write("\n")
        f.write(f"Model run time : {m_run.run_time}\n")
        f.write(f"Prediction count : {len(y_pred_arr)}\n")
        f.write('\n')
        f.write('Detected Drifts : [prediction index, value of delta]\n')
        for e in drift_arr:
            f.write(f'{e}\n')
        if len(drift_arr) == 0:
            f.write('No Drifts Detected\n')
        f.write(f'Model retrain count : {retrain_count["count"]}')

    print("Results files saved")


if __name__ == "__main__":
    main()
