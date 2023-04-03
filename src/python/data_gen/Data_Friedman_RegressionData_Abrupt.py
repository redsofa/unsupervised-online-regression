import numpy as np
import pandas as pd

# Source : https://github.com/anonymous-account-research/uncertainty-drift-detection/blob/master/01_Artificial_DataSets/Data_Friedman_RegressionData_Abrupt.ipynb

x1 = np.random.uniform(0,1,20000)
x2 = np.random.uniform(0,1,20000)
x3 = np.random.uniform(0,1,20000)
x4 = np.random.uniform(0,1,20000)
x5 = np.random.uniform(0,1,20000)
x6 = np.random.uniform(0,1,20000)
x7 = np.random.uniform(0,1,20000)
x8 = np.random.uniform(0,1,20000)
x9 = np.random.uniform(0,1,20000)
x10= np.random.uniform(0,1,20000)

# Validation drift
x1[2000:3000]=np.random.uniform(-1,2,1000)
x3[2000:3000]=np.random.uniform(-1,2,1000)
x5[2000:3000]=np.random.uniform(-1,2,1000)

# 1. Drift
x1[5000:7500]=np.random.uniform(-1,2,2500)
x3[5000:7500]=np.random.uniform(-1,2,2500)
x5[5000:7500]=np.random.uniform(-1,2,2500)

# 2. Drift
x7[10000:12000]=np.random.uniform(-1,2,2000)
x9[10000:12000]=np.random.uniform(-1,2,2000)
x10[10000:12000]=np.random.uniform(-1,2,2000)

# 3. Drift
x1[16000:20000]=np.random.uniform(-1,2,4000)
x3[16000:20000]=np.random.uniform(-1,2,4000)
x5[16000:20000]=np.random.uniform(-1,2,4000)

#y_org = 10*np.sin(np.pi*x1*x2)+20*(x3-0.5)**2 + 10*x4 + 5*x5 + np.random.normal(0,1)
y = 10*np.sin(np.pi*x4*x5)+20*(x2-0.5)**2 + 10*x1 + 5*x3 + np.random.normal(0,1)

relevant_drift_points = [2000, 3000, 5000, 7500, 16000]
irrelevant_drift_points = [10000, 12000]

data = pd.DataFrame([x1,x2,x3,x4,x5,x6,x7,x8,x9,x10, y]).transpose()
data.columns = ['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10', 'y']

#data = data.drop(['y_org'], axis = 1)

data.to_csv('/tmp/friedman_with_2_abrupt_drift.csv', index=False)
