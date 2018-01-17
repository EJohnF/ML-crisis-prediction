import pandas as pd
import numpy as np
from datetime import timedelta

data = pd.read_csv('sp500_daily1990.csv', ',')
N = len(data['Date'])
dates = pd.to_datetime(data['Date'])
data['Date'] = dates

greed = pd.read_csv('fearGreed1.csv', ',')
dates = pd.to_datetime(greed['date'])
greed['date'] = dates

matrix = data.as_matrix()[:, 0:7]
greed = greed.as_matrix()[:,0:2]

def new_version():
    result = []
    current_date = matrix[0][0]
    index = 0
    lastGreed = 0
    while current_date < matrix[-1][0]:
        for i in range(5):
            if matrix[index][0] == current_date:
                result.append(matrix[index])
                index += 1
            else:
                result.append(matrix[index-1])
                result[-1][0] = current_date
                result[-1][1] = matrix[index - 1][4]
                result[-1][2] = matrix[index - 1][4]
                result[-1][3] = matrix[index - 1][4]
                result[-1][4] = matrix[index - 1][4]
                result[-1][5] = 0
                result[-1][6] = 0
            while greed[lastGreed][0] < result[-1][0]:
                lastGreed += 1
            result[-1][5] = greed[lastGreed][1]
            current_date += timedelta(days=1)
        current_date += timedelta(days=2)
    return result

matrix = new_version()

matrix = np.delete(matrix, 0, 1)
N = matrix.shape[0]
def to_set(matrix, treshold):
    x = []
    y = []
    for i in range(0, N-5, 5):
        x.append([])
        for j in range(i, i+5, 1):
            x[int(i/5)].extend(matrix[j])
        if i > 0:
            if (x[int(i/5)][-3]-x[int(i/5)-1][-3])/x[int(i/5)-1][-3] < treshold:
                # 1 if downtrend was more than treshold, 0 - otherwise
                y.append(1)
            else:
                y.append(0)
    return x, y

x, y = to_set(matrix, -0.025)
print(sum(y))
x.pop()
np.savetxt("data_week_X.csv", x, fmt="%15.2f", delimiter=",")
np.savetxt("data_week_Y.csv", y, fmt="%1.0d", delimiter=",")