from skmultiflow.data import RegressionGenerator
from skmultiflow.drift_detection import ADWIN
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def annotation_line(
    ax, xmin, xmax, y, text, ytext=0, linecolor="black", linewidth=1, fontsize=12
):
    ax.annotate(
        "",
        xy=(xmin, y),
        xytext=(xmax, y),
        xycoords="data",
        textcoords="data",
        arrowprops={"arrowstyle": "|-|", "color": linecolor, "linewidth": linewidth},
    )
    ax.annotate(
        "",
        xy=(xmin, y),
        xytext=(xmax, y),
        xycoords="data",
        textcoords="data",
        arrowprops={"arrowstyle": "<->", "color": linecolor, "linewidth": linewidth},
    )

    xcenter = xmin + (xmax - xmin) / 2
    if ytext == 0:
        ytext = y + (ax.get_ylim()[1] - ax.get_ylim()[0]) / 20

    ax.annotate(text, xy=(xcenter, ytext), ha="center", va="center", fontsize=fontsize)


def main():
    data_stream = RegressionGenerator(
        n_samples=1000, n_features=4, n_targets=1, n_informative=3, random_state=42
    )
    # To collecte adwin-detected drifts
    y_drifts = []
    x0_drifts = []
    x1_drifts = []
    x2_drifts = []
    x3_drifts = []

    # Get 1000 initial data points
    X, y = data_stream.next_sample(1000)

    # Drift generation
    # Drift in y values
    for i in range(300, 350):
        y[i] = np.random.randint(600, high=650)

    # Drift in X[0] values
    for i in range(400, 450):
        X[i][0] = np.random.randint(1, high=4)

    # Drift in X[1] values
    for i in range(500, 550):
        X[i][1] = np.random.randint(1, high=4)

    # Drift in X[2] values
    for i in range(600, 650):
        X[i][2] = np.random.randint(1, high=5)

    # Drift in X[3] values
    for i in range(700, 750):
        X[i][3] = np.random.randint(3, high=6)

    # Drift Detection
    # Detect drifts
    drift_detector = ADWIN()
    for i, y_val in enumerate(y):
        drift_detector.add_element(y_val)
        if drift_detector.detected_change():
            print("Drift detected in y value")
            print(f"index : {i}")
            y_drifts.append(i)
            drift_detector.reset()

    drift_detector = ADWIN()
    for i, x_val in enumerate(X):
        drift_detector.add_element(x_val[0])
        if drift_detector.detected_change():
            print("Drift detected in x[0] value")
            print(f"index : {i}")
            x0_drifts.append(i)
            drift_detector.reset()

    drift_detector = ADWIN()
    for i, x_val in enumerate(X):
        drift_detector.add_element(x_val[1])
        if drift_detector.detected_change():
            print("Drift detected in x[1] value")
            print(f"index : {i}")
            x1_drifts.append(i)
            drift_detector.reset()

    drift_detector = ADWIN()
    for i, x_val in enumerate(X):
        drift_detector.add_element(x_val[2])
        if drift_detector.detected_change():
            print("Drift detected in x[2] value")
            print(f"index : {i}")
            x2_drifts.append(i)
            drift_detector.reset()

    drift_detector = ADWIN()
    for i, x_val in enumerate(X):
        drift_detector.add_element(x_val[3])
        if drift_detector.detected_change():
            print("Drift detected in x[3] value")
            print(f"index : {i}")
            x3_drifts.append(i)
            drift_detector.reset()

    # Save Generated data to CSV file
    col_names = [f"x{x}" for x in range(0, 4)]
    col_names.append("y")

    df = pd.DataFrame(columns=col_names)

    for X_vals, y_val in zip(X, y):
        instance = {}
        for i, val in enumerate(X_vals):
            instance[col_names[i]] = val
        instance["y"] = y_val
        df_one_instance = pd.DataFrame(
            [list(instance.values())], columns=list(instance.keys())
        )
        df = pd.concat([df, df_one_instance], ignore_index=True)

    print(df.head())

    df.to_csv("/tmp/synth.csv", index=False)

    # Save line plots
    line_plot(df, 120, y_drifts,  'y', 300, 350, 670, '/tmp/y_plot.png')
    line_plot(df, 120, x0_drifts, 'x0', 400, 450, 3.2, '/tmp/x0_plot.png')
    line_plot(df, 120, x1_drifts, 'x1', 500, 550, 3.2, '/tmp/x1_plot.png')
    line_plot(df, 120, x2_drifts, 'x2', 600, 650, 4.2, '/tmp/x2_plot.png')
    line_plot(df, 120, x3_drifts, 'x3', 700, 750, 5.2, '/tmp/x3_plot.png')


def line_plot(i_pdf, train_test_count, drifts, col_name, x_min, x_max, y_val, file_name):
    i_pdf.drop(['step'], axis=1, inplace=True, errors='ignore')
    i_pdf.insert(0, "step", range(0, len(i_pdf)))
    plt.figure(figsize=(10, 8))
    plt.axvline(train_test_count, color='black')
    plt.plot(
        i_pdf["step"].values,
        i_pdf[col_name].values,
        "g:"
    )
    annotation_line( ax=plt, text='', xmin=x_min, xmax=x_max, \
                                y=y_val, ytext=200, linewidth=1, linecolor='blue', fontsize=18 )

    # add drift markers to plot
    for e in drifts:
        plt.axvline(e, color="red", linestyle="dashdot")

    extraticks = drifts
    plt.xticks(list(plt.xticks()[0]) + extraticks + list([x_min, x_max, train_test_count]))
    plt.xticks(rotation = 90)
    plt.legend(['train/test cut-off', col_name, "ADWIN-detected Drift"])
    plt.savefig(file_name)



if __name__ == "__main__":
    main()
