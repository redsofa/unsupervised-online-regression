import argparse
import time
from river import stream
from nrc import stream_factory

# Modify these to default params suit your context... or just call the python script
# with your own CLI parameters
DEFAULT_FILE_NAME = '../../datasets/small.csv'


def get_args():
    parser = argparse.ArgumentParser(description="Unsupervised, online regression modeling.")
    parser.add_argument('-1', '--input_file_name', type=str, required=False, default=DEFAULT_FILE_NAME, help="input file")

    args = parser.parse_args()
    return args


def main():
    start_time = time.time()

    print('Program Arguments :')
    args = get_args()

    input_file = args.input_file_name

    params = {
            'converters' : {
                'F1' : float,
                'F2' : float
            }
    }
    for x, y in stream.iter_csv(input_file, target='TARGET', **params):
        print(f'New instance : features: {x} -- target: {y}')


    end_time = time.time()
    print(f"\nTotal execution time (seconds): str({end_time} - {start_time})")


if __name__ == '__main__':
    main()
