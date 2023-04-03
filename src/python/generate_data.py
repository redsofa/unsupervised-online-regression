from river.datasets import synth

# https://github.com/online-ml/river/blob/main/river/datasets/synth/friedman.py

dataset = synth.FriedmanDrift(
        drift_type='gsg',
        position=(1, 4),
        transition_window=2,
        seed=42
)

for x, y in dataset.take(5):
    print(list(x.values()), y)

if __name__ == '__main__':
    pass
