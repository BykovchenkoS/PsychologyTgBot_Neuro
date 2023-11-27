from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

from DataPreparation import x_train, y_train, x_test, y_test
from DataPreparation import encoder

model = Sequential()

model.add(LSTM(128, input_shape=(x_train.shape[1], 1), return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(64, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(32))
model.add(Dropout(0.2))

model.add(Dense(units=6, activation='softmax'))

model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(x_train, y_train, batch_size=64, epochs=50, validation_data=(x_test, y_test), callbacks=[ReduceLROnPlateau(monitor='loss', factor=0.4, verbose=0, patience=2, min_lr=0.0000001)])

model.save("my_lstm_model_for_audio")

# Оценка точности модели на тестовых данных
accuracy = model.evaluate(x_test, y_test)[1] * 100
print(f"Accuracy of the model on test data: {accuracy:.2f}%")
