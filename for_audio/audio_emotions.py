import librosa
import numpy as np
from keras.models import load_model
import soundfile

# Загрузка обученной модели
model = load_model('..\\for_audio\\my_model_for_audio')
def extract_features(data):
    result = np.array([])

    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    result = np.hstack((result, zcr))

    stft = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft).T, axis=0)
    result = np.hstack((result, chroma_stft))

    mfcc = np.mean(librosa.feature.mfcc(y=data, n_mfcc=13).T, axis=0)
    result = np.hstack((result, mfcc))

    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms))

    mel = np.mean(librosa.feature.melspectrogram(y=data).T, axis=0)
    result = np.hstack((result, mel))

    return result
def get_features(audio_path):
    # Извлечение характеристик из аудиофайла
    data, sample_rate = librosa.load(audio_path, offset=0.6)
    res1 = extract_features(data)
    result = np.array(res1)
    # noise_data = data + 0.005 * np.random.normal(0, 1, len(data))
    # res2 = extract_features(noise_data)
    # result = np.vstack((result, res2))
    # n_steps = 4
    # data_stretch_pitch = librosa.effects.pitch_shift(data, sr=sample_rate, n_steps=n_steps, bins_per_octave=12)
    # res3 = extract_features(data_stretch_pitch)
    # np.vstack((result, res3))
    return result  # Возвращаем извлеченные характеристики

def predict_emotion(audio_features):
    # Преобразование данных для подачи в модель
    # Например, обработка извлеченных характеристик для подачи в модель

    data_for_model = np.expand_dims(audio_features, axis=0)  # Пример
    # data_for_model = np.transpose(data_for_model, (0, 2, 1))
    # Предсказание эмоции с помощью модели
    predicted_emotion = model.predict(data_for_model)
    return predicted_emotion  # Возвращаем предсказанную эмоцию

def audio_emotions(audio_path):
    audio_features = get_features(audio_path)
    predicted_emotion = predict_emotion(audio_features)
    return predicted_emotion