import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from fluire.util.files import mkdir_structure
import os


HOME_DIR = os.path.expanduser('~')
IN_DIR = '/data/usup_reg/raw/uci/protein'
IN_FILE = 'CASP.csv'
OUT_DIR = '/data/usup_reg/work/uci/protein'
TRAIN_INSTANCES = 100
TEST_INSTANCES = 20
X_COL_INDICES = range(1, 10)
Y_COL_INDEX = range(0, 1)


def arrs_to_df(x_arr, y_pred_arr, y_true_arr):
    ret_val = pd.DataFrame(
        {"x": x_arr, "y_pred": y_pred_arr, "y_true": y_true_arr},
        columns=["x", "y_pred", "y_true"],
    )
    return ret_val


def main():
    src_dir = f'{HOME_DIR}/{IN_DIR}'
    src_file = f'{src_dir}/{IN_FILE}'

    dst_dir = f'{HOME_DIR}/{OUT_DIR}'

    train_and_test_instances = TRAIN_INSTANCES + TEST_INSTANCES

    # Create the output directory if it does not exit.
    mkdir_structure(dst_dir)

    # Load source file into pandas dataframe (pdf for short)
    pdf = pd.read_csv(src_file)

    total_instances = pdf.shape[0]
    non_train_and_test_instances = total_instances - train_and_test_instances

    # Train and test split of the initial instance data
    train_pdf = pdf.iloc[:TRAIN_INSTANCES]
    test_pdf = pdf.iloc[TRAIN_INSTANCES:train_and_test_instances]

    train_X = train_pdf.iloc[:, X_COL_INDICES].values
    train_y = train_pdf.iloc[:, Y_COL_INDEX].values

    test_X = test_pdf.iloc[:, X_COL_INDICES].values
    test_y = test_pdf.iloc[:, Y_COL_INDEX].values

    # Create linear regression object
    regr = linear_model.LinearRegression()

    # Train the model using the training sets
    regr.fit(train_X, train_y)

    # Make predictions using the testing set
    pred_y = regr.predict(test_X)

    # The coefficients (FROM TRAINING)
    print("Coefficients: \n", regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(test_y, pred_y))
    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(test_y, pred_y))


    # make predictions on the rest of the data
    non_train_or_test_pdf = pdf.iloc[train_and_test_instances:non_train_and_test_instances]
    rest_X = non_train_or_test_pdf.iloc[:, X_COL_INDICES].values
    rest_y = non_train_or_test_pdf.iloc[:, Y_COL_INDEX].values

    pred_rest_y = regr.predict(rest_X)
    print("Mean squared error: %.2f" % mean_squared_error(rest_y, pred_rest_y))
    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(rest_y, pred_rest_y))

    print(rest_X)
    print(pred_rest_y)
    print(rest_y)

    print(len(rest_X))
    print(len(rest_y))
    print(len(pred_rest_y))
    return

    pred_pdf = arrs_to_df(rest_X, pred_rest_y, rest_y)
    pred_pdf.to_csv('./tmp.csv', index=False)


    # Plot outputs0
    # plt.scatter(test_X, test_y, color="black")
    # plt.plot(diabetes_X_test, diabetes_y_pred, color="blue", linewidth=3)

    # plt.xticks(())
    # plt.yticks(())

    # plt.show()


if __name__ == '__main__':
    main()




