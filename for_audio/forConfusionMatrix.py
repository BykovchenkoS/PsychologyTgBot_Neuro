from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from DataPreparation import x_test, y_test
from DataPreparation import encoder

# Загрузка сохраненной модели
model = load_model('my_lstm_model_for_audio')  # Замените 'path_to_your_saved_model' на путь к вашей сохраненной модели

# Предсказание на тестовых данных с использованием загруженной модели
pred_test = model.predict(x_test)
y_pred = encoder.inverse_transform(pred_test)
y_test = encoder.inverse_transform(y_test)

# Вывод отчета о классификации
print(classification_report(y_test, y_pred))

# Построение матрицы ошибок
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(12, 10))
cm = pd.DataFrame(cm, index=[i for i in encoder.categories_], columns=[i for i in encoder.categories_])
sns.heatmap(cm, linecolor='white', cmap='Blues', linewidth=1, annot=True, fmt='')
plt.title('Confusion Matrix', size=20)
plt.xlabel('Predicted Labels', size=14)
plt.ylabel('Actual Labels', size=14)
plt.show()
