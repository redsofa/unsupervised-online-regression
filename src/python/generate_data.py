from skmultiflow.data import RegressionGenerator
from skmultiflow.drift_detection import ADWIN

# NOTE THIS WAS GENERATED WITH CHATGPT AND ADAPTED FOR OUR CONTEXT


# Define a regression generator with 1 dependent variables and 4 independent variable
generator = RegressionGenerator(n_features=4, n_targets=1, n_informative=3, random_state=42)

# Define a drift detector using ADWIN
drift_detector = ADWIN()

# Generate 500 samples with no drift
for i in range(500):
    X, y = generator.next_sample()
    # Do something with the data

 

# Introduce a drift at sample 500
generator.n_targets = 1

 

# Generate 500 samples with drift
for i in range(500):
    X, y = generator.next_sample()
    # Do something with the data

 

    # Check if there's a drift
    if drift_detector.detected_change():
        # If there's a drift, reset the drift detector
        drift_detector.reset()
        # Introduce a new drift
        generator.n_targets = 3
