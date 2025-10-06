import tensorflow as tf
from keras.src.activations import leaky_relu
from tensorflow import keras
import yfinance as yf
from tf_keras.src.activations import sigmoid
import numpy as np

tickers = ['CMCSA']
train_start_date = "2000-01-01"
train_end_date = "2009-12-31"

test_start_date = "2020-01-01"
test_end_date = "2025-01-01"

data_test = yf.download(tickers, start=train_start_date,end=test_end_date)
data_test.fillna(0)
x_test = data_test['Close']['CMCSA']
y_test = []
for i in range(len(x_test)-1):
    if x_test[i] > x_test[i+1]:
        y_test.append(0)
    elif x_test[i] < x_test[i+1]:
        y_test.append(1)
    else:
        y_test.append(0.5)
data = yf.download(tickers, train_start_date, train_end_date)
data.fillna(0)
x_train = data['Close']['CMCSA']
y_train = []
for i in range(len(x_train)-1):
    if x_train[i] > x_train[i+1]:
        y_train.append(0)
    elif x_train[i] < x_train[i+1]:
        y_train.append(1)
    else:
        y_train.append(0.5)
if x_train[-1] < x_test[0]:
    y_train.append(0)
elif x_train[-1] > x_test[0]:
    y_train.append(1)
else:
    y_train.append(0.5)
model = keras.Sequential([
    keras.layers.LSTM(units=64,activation='leaky_relu'),
    keras.layers.Dense(1, activation='sigmoid')
])
model.compile(optimizer='nadam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.fit(x_train, y_train,epochs=10)
test_loss, test_acc = model.evaluate(x_test, y_test,verbose=2)
model.save('/models/model_1.h5')