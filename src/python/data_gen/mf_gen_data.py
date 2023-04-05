from skmultiflow.data import RegressionGenerator
from skmultiflow.drift_detection import ADWIN
from skmultiflow.utils import check_random_state
import numpy as np
import pandas as pd

def main():
    data_stream = RegressionGenerator(n_samples=1000,
                                    n_features=4,
                                    n_targets=1,
                                    n_informative=3,
                                    random_state=42)

    drift_detector = ADWIN()

    # Get 500 initial data points
    X, y =  data_stream.next_sample(500)

    for i in range(250, 300):
        y[i] = np.random.randint(3000, high=5000)
        X[i][0] = np.random.randint(1000, high=4000)
        X[i][1] = np.random.randint(2000, high=4000)
        X[i][2] = np.random.randint(3000, high=4000)

    for i, y_val in enumerate(y):
        drift_detector.add_element(y_val)
        if drift_detector.detected_change():
            print('Drift detected in y value')
            print(f'index : {i}')
            drift_detector.reset()

    drift_detector = ADWIN()
    for i, x_val in enumerate(X):
        drift_detector.add_element(x_val[0])
        if drift_detector.detected_change():
            print('Drift detected in x value')
            print(f'index : {i}')
            drift_detector.reset()


    # Save to CSV file
    col_names = [f'x{x}' for x in range(1, 5)]
    col_names.append('y')

    df = pd.DataFrame(columns = col_names)

    for X_vals, y_val in zip(X, y):
        instance = {}
        for i, val in enumerate(X_vals):
            instance[col_names[i]] = val
        instance['y'] = y_val
        df_one_instance = pd.DataFrame([list(instance.values())], columns=list(instance.keys()))
        df = pd.concat([df, df_one_instance], ignore_index=True)

    print(df.head())

    df.to_csv('/tmp/synth.csv', index=False)



if __name__ == "__main__":
    main()
