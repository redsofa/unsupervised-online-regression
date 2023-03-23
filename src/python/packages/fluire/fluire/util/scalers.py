from collections import (
    Counter,
    defaultdict
)
# A note on the imports here :
#
# Counter is an unordered collection where elements are stored as
# Dict keys and their counts as dict values.

# defaultdict means that if a key is not found in the dictionary,
# then instead of a KeyError being thrown, a new entry is created.
# The type of this new entry is given by the argument of defaultdict.
from math import sqrt


def safe_div(num, denum):
    if denum is None:
        return 0.0
    elif denum == 0.0:
        return 0.0
    else:
        return num / denum


class StandardScaler:
    def __init__(self):
        self._counters = Counter()
        self._mean_estimates = defaultdict(float)
        self._std_dev_estimates = defaultdict(float)
        self._standardized_sample = defaultdict(float)

    def add_sample(self, x: dict) -> None:
        # Note this algorithm is from :
        # Žliobaitė I, Hollmen J. Optimizing regression models for data streams with
        # missing values. Machine Learning. 2015 Apr;99:47-73.

        # The strategy for storing and cycling through the data structure is from River :
        # https://github.com/online-ml/river/blob/main/river/preprocessing/scale.py
        # The code is similar but not exactly the same.
        if type(x) is dict:
            for k, xt in x.items():
                previous_mean_estimate = self._mean_estimates[k]
                previous_std_dev_estimate = self._std_dev_estimates[k]
                t = self._counters[k]
                n_ = safe_div(1, t)

                # Update counter for this feature
                self._counters[k] += 1

                # Update mean estimates for this feature
                self._mean_estimates[k] = n_ * xt + (1 - n_) * previous_mean_estimate

                # Update the standard deviation
                self._std_dev_estimates[k] = sqrt( n_ * (xt - self._mean_estimates[k]) ** 2 + (1 - n_) * previous_std_dev_estimate ** 2 )

                # Update standardized data
                self._standardized_sample[k] = safe_div((xt - previous_mean_estimate), previous_std_dev_estimate)
        else:
            raise Exception('add_sample() Expects a dictionary!')

        # Return standardized data
        return dict(self._standardized_sample)

    @property
    def standardized_sample(self):
        return dict(self._standardized_sample)


if __name__ == "__main__":
    pass
