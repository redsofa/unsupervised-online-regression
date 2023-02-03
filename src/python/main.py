import argparse
import time
import json
from nrc.factories.stream_factory import StreamFactory
from queue import Queue
from nrc.settings.default_params import *
from nrc.runners import ModelRunner


def get_args():
    parser = argparse.ArgumentParser(description="Unsupervised, online regression modeling.")
    parser.add_argument('-1', '--input_file_name', type=str, required=False, default=DEFAULT_FILE_NAME, help="Input file (csv)")
    parser.add_argument('-2', '--stream_parameters', type=str, required=False, default=DEFAULT_STREAM_PARAMETERS, help='Stream parameters')
    parser.add_argument('-3', '--buffer_size', type=str, required=False, default=DEFAULT_BUFFER_SIZE, help='Buffer size')
    args = parser.parse_args()
    return args

def load_stream_params(i_params_file):
    with open(i_params_file) as f:
        data = f.read()
    stream_params = json.loads(data)
    for e in stream_params['converters']:
        data_type = stream_params['converters'][e]
        if data_type == 'float':
            stream_params['converters'][e] = float
        elif data_type == 'int':
            stream_params['converters'][e] = int
        else:
            stream_params['converters'][e] = str
    return stream_params

def main():
    start_time = time.time()
    args = get_args()

    model_names = ['stub_model']

    input_file = args.input_file_name
    stream_params = load_stream_params(args.stream_parameters)
    data_stream = StreamFactory.get_csv_stream(input_file, **stream_params)

    runner = ModelRunner(data_stream, model_names, args.buffer_size)
    runner.run_models()

    end_time = time.time()
    print(f"\nTotal execution time (seconds): str({end_time} - {start_time})")


if __name__ == '__main__':
    main()
