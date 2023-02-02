import argparse
import time

# Modify these to default params suit your context... or just call the python script
# with your own CLI parameters
DEFAULT_FILE_NAME = '/Users/richardr/data/bioreactor/AAV-RBD-CD4L.csv'

def get_args():
    parser = argparse.ArgumentParser(description="Unsupervised, online regression modeling.")
    parser.add_argument('-1', '--input_file_name', type=str, required=False, default=DEFAULT_FILE_NAME, help="input file")

    args = parser.parse_args()
    return args


def main():
    start_time = time.time()

    print('Program Arguments :')
    args = get_args()
    print(args)

    end_time = time.time()
    print(f"Total execution time (seconds): str({end_time} - {start_time})")


if __name__ == '__main__':
    main()
