# Code source: Jaques Grobler
# License: BSD 3 clause

import pandas as pd
from sklearn import datasets


# Load the diabetes dataset into a pandas dataframe

# This returns a tuple (data, target)
diab_dfs = datasets.load_diabetes(return_X_y=True, as_frame=True)
# This merges the two dataframes into one 
diab_df = pd.concat([diab_dfs[0], diab_dfs[1]], axis=1)

# Save the dataframe to a CSV file
diab_df.to_csv('diabetes.csv', sep=",", header=True, index=False)
