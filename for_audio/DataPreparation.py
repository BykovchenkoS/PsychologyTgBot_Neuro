from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv('features.csv')

X = data.iloc[:, :-1].values
Y = data['labels'].values

encoder = OneHotEncoder()
Y = encoder.fit_transform(np.array(Y).reshape(-1, 1)).toarray()
x_train, x_test, y_train, y_test = train_test_split(X, Y, random_state=0, shuffle=True)

scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

print("Размерности данных до изменений: ", x_train.shape, y_train.shape, x_test.shape, y_test.shape)

x_train = np.expand_dims(x_train, axis=2)
x_test = np.expand_dims(x_test, axis=2)

print("Размерности данных после изменений: ", x_train.shape, y_train.shape, x_test.shape, y_test.shape)
