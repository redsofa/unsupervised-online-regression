import argparse
import time
from nrc.factories.stream import StreamFactory
from nrc.factories.model import ModelFactory
from nrc.settings.default_params import *
from nrc.util.stream import *


def get_args():
    parser = argparse.ArgumentParser(description="Unsupervised, online regression modeling.")
    parser.add_argument('-1', '--input_file_name', type=str, required=False, default=DEFAULT_FILE_NAME, help="Input file (csv)")
    parser.add_argument('-2', '--stream_parameters', type=str, required=False, default=DEFAULT_STREAM_PARAMETERS, help='Stream parameters')
    parser.add_argument('-3', '--buffer_size', type=int, required=False, default=DEFAULT_BUFFER_SIZE, help='Buffer size')
    parser.add_argument('-4', '--max_samples', type=int, required=False, default=DEFAULT_MAX_SAMPLES, help='Max Number of samples to process')
    parser.add_argument('-5', '--pre_train_size', type=int, required=False, default=DEFAULT_PRETRAIN_SIZE, help='Size of the pre-training dataset')

    args = parser.parse_args()
    return args


def main():
    args = get_args()
    # Array of models to run.
    model_names = ['stub_model']
    # stream_params specifies how to transform the input data stream features and which column is
    # the target variable.
    stream_params = load_stream_params(args.stream_parameters)

    # Runs models sequentially and use the same data stream each time.
    for model_name in model_names:
        data_stream = StreamFactory.get_csv_stream(args.input_file_name, **stream_params)
        model = ModelFactory.get_instance(model_name, args.pre_train_size, args.buffer_size, args.max_samples)
        model.data_stream = data_stream
        model.run()
        print(f"\nTotal execution time (seconds): {model.run_time}\n")
        print('Model State:\n')
        print(model)
        print()


if __name__ == '__main__':
    main()
