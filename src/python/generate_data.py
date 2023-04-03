from river.datasets import synth
import pandas as pd


# https://github.com/online-ml/river/blob/main/river/datasets/synth/friedman.py
def main():
    col_names = [f'f_{x}' for x in range(0, 10)]
    col_names.append('y')

    df = pd.DataFrame(columns = col_names)
    dataset = synth.FriedmanDrift(
            drift_type='gsg',
            position=(1, 4),
            transition_window=2,
            seed=42
    )

    for x, y in dataset.take(10000):
        instance = {}
        for i, val in enumerate(x.values()):
            instance[col_names[i]] = val
        instance['y'] = y
        df_one_instance = pd.DataFrame([list(instance.values())], columns=list(instance.keys()))
        df = pd.concat([df, df_one_instance], ignore_index=True)

    print(df.head())

    df.to_csv('~/data/usup_reg/raw/synth/synth.csv', index=False)


if __name__ == '__main__':
    main()
