import argparse
import pandas as pd
from sklearn.preprocessing import StandardScaler


DEFAULT_INPUT_DIR = '/Users/richardr/data/usup_reg/raw/uci/wine'
DEFAULT_INPUT_FILE = 'winequality_white.csv'
DEFAULT_OUTPUT_DIR = '/Users/richardr/data/usup_reg/raw/uci/wine'
DEFAULT_OUTPUT_FILE = 'std_winequality_white.csv'
DEFAULT_X_COL_INDICES = '0,1'


def get_args():
    parser = argparse.ArgumentParser(
        description="Standardize csv file"
    )
    parser.add_argument(
        "-1",
        "--input_dir",
        type=str,
        required=False,
        default=DEFAULT_INPUT_DIR,
        help="",
    )
    parser.add_argument(
        "-2",
        "--input_file",
        type=str,
        required=False,
        default=DEFAULT_INPUT_FILE,
        help="",
    )
    parser.add_argument(
        "-3",
        "--output_dir",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_DIR,
        help="",
    )
    parser.add_argument(
        "-4",
        "--output_file",
        type=str,
        required=False,
        default=DEFAULT_OUTPUT_FILE,
        help="",
    )
    parser.add_argument(
       "-5",
       "--x_col_indices",
       type=lambda s: [int(item) for item in s.split(',')],
       required=False,
       default=DEFAULT_X_COL_INDICES,
       help='X column indices',
    )
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    input_file = f'{args.input_dir}/{args.input_file}'
    output_file = f'{args.output_dir}/{args.output_file}'

    scaler = StandardScaler()
    i_pdf = pd.read_csv(input_file)
    i_pdf.iloc[:, args.x_col_indices] = scaler.fit_transform(i_pdf.iloc[:, args.x_col_indices])

    i_pdf.to_csv(output_file, index=False)


if __name__ == "__main__":
    main()
