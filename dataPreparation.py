import pandas as pd
import numpy as np
from datetime import timedelta

data = pd.read_csv('sp500_daily1990.csv', ',')
N = len(data['Date'])
del data['Adj Close']
dates = pd.to_datetime(data['Date'])
data['Date'] = dates

matrix = data.as_matrix()[:, 0:6]

def old_version():
    i = 1
    startWeekIndex = 0
    while i < N:
        if matrix[i][0] - timedelta(days=1) != matrix[i - 1][0] and matrix[i][0] < timedelta(days=6) + \
                matrix[startWeekIndex][0]:
            matrix = np.insert(matrix, i, matrix[i - 1], 0)
            matrix[i][0] += timedelta(days=1)
            matrix[i][1] = matrix[i - 1][4]
            matrix[i][2] = matrix[i - 1][4]
            matrix[i][3] = matrix[i - 1][4]
            matrix[i][4] = matrix[i - 1][4]
            matrix[i][5] = 0
        if matrix[i][0] > matrix[startWeekIndex][0] + timedelta(days=5):
            startWeekIndex = i
        i += 1
    print(matrix[0:1000,0])
    matrix = np.delete(matrix, 0, 1)
    np.savetxt("data.csv", matrix, fmt="%15.2f", delimiter=",")

def new_version():
    result = []
    current_date = matrix[0][0]
    index = 0
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
            current_date += timedelta(days=1)
        current_date += timedelta(days=2)
    return result

matrix = new_version()
matrix = np.delete(matrix, 0, 1)

def to_set(matrix, treshold):
    x = []
    y = []
    for i in range(0, N-5, 5):
        x.append([])
        for j in range (i,i+5,1):
            x[int(i/5)].extend(matrix[j])
        if i > 0:
            if (x[int(i/5)][-2]-x[int(i/5)-1][-2])/x[int(i/5)-1][-2] < treshold:
                # 1 if downtrend was more than treshold, 0 - otherwise
                y.append(1)
            else:
                y.append(0)
    return x, y

x, y = to_set(matrix, -0.025)
np.savetxt("data_week_X.csv", x, fmt="%15.2f", delimiter=",")
np.savetxt("data_week_Y.csv", y, fmt="%1.0d", delimiter=",")