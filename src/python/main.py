import argparse
import pprint
import json
from fluire.factories.stream import StreamFactory
from fluire.models.runner import ModelRunner
from fluire.util.scalers import RiverStandardScalerWrapper
from fluire.settings.default_params import (
    DEFAULT_RAW_DATA_DIR,
    DEFAULT_DELTA_THRESHOLD,
    DEFAULT_OUTPUT_DRIFTS_CSV_FILE,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_INPUT_CSV_FILE,
    DEFAULT_INPUT_CSV_PARAMETERS_FILE,
    DEFAULT_OUTPUT_PREDICTIONS_FILE,
    DEFAULT_OUTPUT_STATS_FILE,
    DEFAULT_MAX_SAMPLES,
    DEFAULT_DRIFT_DETECTOR_CONFIG,
    DEFAULT_LOG_LEVEL,
    DEFAULT_WORKING_DATA_POINTS,
    DEFAULT_ALGORITHM,
    DEFAULT_IS_BASELINE_RUN
)
from fluire.util.stream import load_stream_params
import pandas as pd
from fluire.util.files import mkdir_structure
from functools import partial
import logging
from fluire.settings.logging import logger


def drift_to_df(drift_arr):
    ret_val = pd.DataFrame(
            {
                "location": [e[0] for e in drift_arr]
            }, columns=["location"]
    )
    return ret_val


def arrs_to_df(x_arr, y_pred_arr, y_true_arr):
    ret_val = pd.DataFrame(
        {"x": x_arr, "y_pred": y_pred_arr, "y_true": y_true_arr},
        columns=["x", "y_pred", "y_true"],
    )
    return ret_val


def int_or_none(value):
    if value == 'None':
        return None
    else:
        return int(value)


def float_or_none(value):
    if value == 'None':
        return None
    else:
        return float(value)


def str_to_dict(value):
    return json.loads(value)


def str_to_bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in ('true'):
        return True
    elif value.lower() in ('false'):
        return False
    else:
        msg = 'Boolean value expected.'
        logger.error(msg)
        raise argparse.ArgumentTypeError(msg)


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
        "--working_data_points",
        type=int,
        required=False,
        default=DEFAULT_WORKING_DATA_POINTS,
        help="Number of data point to use for initial train and test task.",
    )
    parser.add_argument(
        "-8",
        "--max_samples",
        type=int_or_none,
        required=False,
        default=DEFAULT_MAX_SAMPLES,
        help="Max Number of samples to process.",
    )
    parser.add_argument(
        "-9",
        "--output_drifts_csv_file",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_DRIFTS_CSV_FILE,
        help="Detected drift location CSV file (indices are relative to predictions csv file.)",
    )
    parser.add_argument(
        "-10",
        "--algorithm",
        type=str,
        required=False,
        default=DEFAULT_ALGORITHM,
        help="Algorithm to use in the online prediction.",
    )
    parser.add_argument(
        "-11",
        "--drift_detector_config",
        type=str_to_dict,
        required=False,
        default=DEFAULT_DRIFT_DETECTOR_CONFIG,
        help="Drift detection algorithm.",
    )
    parser.add_argument(
        '-12',
        '--loglevel',
        type=str,
        required=False,
        default=DEFAULT_LOG_LEVEL,
        help=f'Provide logging level. Example --loglevel debug, warning, info, default={DEFAULT_LOG_LEVEL}'
    )
    parser.add_argument(
        '-13',
        '--delta_threshold',
        type=float_or_none,
        required=False,
        default=DEFAULT_DELTA_THRESHOLD,
        help='Delta threshold setting.'
    )
    parser.add_argument(
        "-14",
        "--is_baseline_run",
        type=str_to_bool,
        required=False,
        default=DEFAULT_IS_BASELINE_RUN,
        help="Whether this model will run without retraining and drift detection.",
    )
    args = parser.parse_args()
    return args

def model_retrained_handler(*args, **kwargs):
    count_dict = args[0]
    count_dict['count'] += 1
    # Make sure the model memory address changes
    # print(kwargs['model'])
    retrain_arr = args[1]
    retrain_arr.append([kwargs['prediction_count']])


def drift_handler(*args, **kwargs):
    # The args arguments come from the utilization of a partial function definition
    drift_arr = args[0]
    # The kwargs come from the handler code call inside the model runner
    drift_arr.append([kwargs['prediction_count']])


def main():
    args = get_args()
    # Set logging level for the script.
    logging.getLogger().setLevel(args.loglevel.upper())

    logger.debug(f'Application parameters : \n {args} \n')

    # Create the output directory if it does not exit.
    mkdir_structure(args.output_dir)

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

    x_arr = []
    y_pred_arr = []
    y_true_arr = []
    drift_arr = []
    retrain_count = {'count': 0}
    retrain_arr = []

    partial_drift_fn = partial(drift_handler, drift_arr)
    partial_retrain_fn = partial(model_retrained_handler, retrain_count, retrain_arr)

    # For online standardization
    # riv_scaler = RiverStandardScalerWrapper()

    m_run = ModelRunner()
    m_run\
        .set_model_name(args.algorithm)\
        .set_working_data_points(args.working_data_points)\
        .set_data_stream(data_stream)\
        .set_scaler(None)\
        .set_drift_detector_config(**args.drift_detector_config)\
        .set_drift_handler(partial_drift_fn)\
        .set_model_retrained_handler(partial_retrain_fn)\
        .set_max_samples(args.max_samples)\
        .set_delta_threshold(args.delta_threshold)\
        .set_is_baseline_run(args.is_baseline_run)

    m_run.validate_settings()

    logger.debug(f'Running model : {m_run.model_name}')
    # Run the model
    for x, y_pred, y_true in m_run.run():
        x_arr.append(x[0].tolist())
        y_pred_arr.append(y_pred.flatten('F')[0])
        y_true_arr.append(y_true)

    p_df = arrs_to_df(x_arr, y_pred_arr, y_true_arr)
    p_df.to_csv(output_pred_csv_file, index=False)

    p_df = drift_to_df(drift_arr)
    p_df.to_csv(output_drift_csv_file, index=False)

    with open(output_stats_file, "w") as f:
        f.write("Program Arguments\n")
        f.write('------------------------\n')
        for key, value in vars(args).items():
            f.write(f"{key} : {value}\n")
        f.write("\n\n")
        f.write("Execution Information\n")
        f.write('---------------------\n')
        f.write(f"Model run time : {m_run.run_time}\n")
        f.write(f"Prediction count : {len(y_pred_arr)}\n")
        f.write('\n\n')
        f.write("Drift Information\n")
        f.write('-----------------\n')
        f.write(f'Drift count : {len(drift_arr)}\n')
        f.write('Detected Drifts at prediction index :\n')
        for e in drift_arr:
            f.write(f'{e}\n')
        if len(drift_arr) == 0:
            f.write('No Drifts Detected\n')
        f.write('\n\n')
        f.write("Model Update Information\n")
        f.write('------------------------\n')
        f.write(f'Model retrain count : {retrain_count["count"]}\n')
        f.write('Model retraining at prediction index :\n')
        for e in retrain_arr:
            f.write(f'{e}\n')
        if len(retrain_arr) == 0:
            f.write('No model retraining required.')
        f.write('\n\n')
        f.write("Feature and Target Information\n")
        f.write('------------------------------\n')
        f.write('Stream parameter settings :\n')
        pprint.pprint(stream_params, f)

    print("Results files saved")


if __name__ == "__main__":
    main()
