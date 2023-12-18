import librosa
import numpy as np
import pandas as pd

from for_audio import CremaD_df


def extract_features(data):
    """

    Извлечение характеристик из аудио:

        Zero Crossing Rate (ZCR): Средняя частота пересечения нуля в сигнале.
                                    Отражает количество раз, когда сигнал меняет знак.

        Chroma_stft: Средние значения компонентов Хроматического преобразования с использованием
                        кратковременного преобразования Фурье (STFT). Это характеристика, связанная с цветностью звука.

        MFCC (Mel-frequency cepstral coefficients): Средние значения коэффициентов MFCC, представляющих
                                                        спектральные особенности сигнала, основанные на мел-шкале.

        Root Mean Square (RMS) value: Среднеквадратичное значение сигнала, отражает амплитуду сигнала.

        Mel Spectrogram: Среднее значение мел-спектрограммы, представляющей спектрограмму сигнала в мел-шкале.


    """

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


def get_features(path):
    data, sample_rate = librosa.load(path, duration=2.5, offset=0.6)
    res1 = extract_features(data)
    result = np.array(res1)
    noise_data = data + 0.005 * np.random.normal(0, 1, len(data))
    res2 = extract_features(noise_data)
    result = np.vstack((result, res2))
    new_data = librosa.effects.time_stretch(data, rate=1.5)
    n_steps = 4
    data_stretch_pitch = librosa.effects.pitch_shift(data, sr=sample_rate, n_steps=n_steps, bins_per_octave=12)
    res3 = extract_features(data_stretch_pitch)
    result = np.vstack((result, res3))

    return result


X = []
Y = []

# Цикл для извлечения признаков из аудиофайлов и их меток
for path, emotion in zip(CremaD_df['Path'], CremaD_df['Emotions']):
    # Получение признаков для каждого аудиофайла
    features = get_features(path)

    # Добавление признаков и меток в соответствующие списки
    for ele in features:
        X.append(ele)
        Y.append(emotion)

# Преобразование данных в DataFrame
Features = pd.DataFrame(X)

# Добавление меток к признакам в DataFrame
Features['labels'] = Y

# Сохранение признаков и меток в файл CSV
Features.to_csv('features.csv', index=False)
