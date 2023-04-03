import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Source : https://github.com/anonymous-account-research/uncertainty-drift-detection/blob/master/01_Artificial_DataSets/Data_Breiman_2dplanes_RegressionData_Abrupt.ipynb

x1 = np.random.choice([-1,1], size=20000)

x2 = np.random.randint(-1,2, size=20000)
x3 = np.random.randint(-1,2, size=20000)
x4 = np.random.randint(-1,2, size=20000)
x5 = np.random.randint(-1,2, size=20000)
x6 = np.random.randint(-1,2, size=20000)
x7 = np.random.randint(-1,2, size=20000)
x8 = np.random.randint(-1,2, size=20000)
x9 = np.random.randint(-1,2, size=20000)
x10 = np.random.randint(-1,2, size=20000)

#Create drift 1
x1[5000:7500] = np.random.choice([-2,-1,1,2], size=2500)

#Create drift 2
x4[10000:12500] = np.random.randint(-2,3, size=2500)
x5[10000:12500] = np.random.randint(-2,3, size=2500)
x6[10000:12500] = np.random.randint(-2,3, size=2500)
x7[10000:12500] = np.random.randint(-2,3, size=2500)

#Create drift 3

x1[15000:17500] = np.random.choice([-2,-1,1,2], size=2500)
x4[15000:17500] = np.random.randint(-2,3, size=2500)
x5[15000:17500] = np.random.randint(-2,3, size=2500)
x6[15000:17500] = np.random.randint(-2,3, size=2500)
x7[15000:17500] = np.random.randint(-2,3, size=2500)


y = np.where(np.sign(x1)==1, 3+3*x2+2*x3+1*x4+np.random.normal(0,1,size=20000), -3+3*x5+2*x6+1*x7+np.random.normal(0,1,size=20000))
data = pd.DataFrame([x1,x2,x3,x4,x5,x6,x7,x8,x9,x10, y]).transpose()
data.columns = ['x1','x2','x3','x4','x5','x6','x7','x8','x9','x10', 'y']
print(data.head())

data.to_csv('/tmp/2dplanes_with_3_abrupt_drift.csv', index=False)

