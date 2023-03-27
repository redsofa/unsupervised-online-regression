import unittest
from fluire.util.scalers import StandardScaler
import random


class TestStandardScaler(unittest.TestCase):
    def test_happy_path(self):
        std_scaler = StandardScaler()
        #r_std_scaler = RivStandardScaler()
        random.seed(42)
        samples = [{'f1': random.uniform(8, 12), 'f2': random.uniform(8, 12)} for _ in range(6)]
        print()
        print()
        print('Show the generated, un-scaled data : ')
        for sample in samples:
            print(sample)

        expected_scaled_values = [
            {'f1': 0.0, 'f2': 0.0},
            {'f1': 0.0, 'f2': 0.0},
            {'f1': 2.1674653620877917, 'f2': 7.885757405502203},
            {'f1': 2.273204997584291, 'f2': -1.0050641759219596},
            {'f1': -1.1701833155935442, 'f2': -1.072790042283996},
            {'f1': -2.0742915071321235, 'f2': 1.4669931232249165}
       ]

        actual_scaled_values = []

        print('Show and collect the scaled sample data :')
        for sample in samples:
            scaled = std_scaler.add_sample(sample)
            print(scaled)
            actual_scaled_values.append(scaled)
        '''
        print()
        print()
        print()
        for sample in samples:
            scaled = r_std_scaler.learn_one(sample).transform_one(sample)
            print(scaled)

        print()
        print()
        print()
        '''
        # Make sure the expected and actual values are the same.
        for item in list(zip(expected_scaled_values, actual_scaled_values)):
            # Compare expected and actual dictionaries values one by one
            self.assertDictEqual(item[0], item[1])

        '''
        def welford(x_array):
            k = 0
            M = 0
            S = 0
            for x in x_array:
                k += 1
                Mnext = M + (x - M) / k
                S = S + (x - M)*(x - Mnext)
                M = Mnext
                print(M, S)
            return (M, S/(k-1))
        '''
        '''
        import pandas as pd
        import numpy as np
        np.random.seed(123456789)   # repeatable results
        f0 = 2
        t = np.arange(0,1.0,1.0/65536)

        mysignal = (np.mod(f0*t,1) < 0.5)*2.0-1
        mynoise = 0.2*np.random.randn(*mysignal.shape)
        y1 = (mysignal+mynoise)[t<0.2]
        def welford(x_array):
            k = 0 
            M = 0
            S = 0
            for x in x_array:
                k += 1
                Mnext = M + (x - M) / k
                S = S + (x - M)*(x - Mnext)
                M = Mnext
            return (M, S/(k-1))

        for A in [1e7, -1e7]:
            y1b = y1 - 1 + A
            print("welford:", welford(y1b))
            print("numpy:   ", (np.mean(y1b), np.var(y1b, ddof=1)))
        '''

if __name__ == "__main__":
    unittest.main()
