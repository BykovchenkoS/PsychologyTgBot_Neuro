import librosa
from matplotlib import pyplot as plt

from for_audio import CremaD_df


def display_all_emotions(dataframe):

    """ Построим волновые графики и спектрограммы для аудио с разнми эмоциями и сравним их визуально  """

    fig, axs = plt.subplots(nrows=len(dataframe['Emotions'].unique()), ncols=2, figsize=(12, 8))

    for i, emotion in enumerate(dataframe['Emotions'].unique()):
        path = dataframe[dataframe['Emotions'] == emotion]['Path'].values[0]
        data, sampling_rate = librosa.load(path)

        axs[i, 0].set_title('Waveplot for audio with {} emotion'.format(emotion), size=12)
        axs[i, 0].set_ylabel('Amplitude')
        librosa.display.waveshow(data, sr=sampling_rate, ax=axs[i, 0])

        X = librosa.stft(data)
        Xdb = librosa.amplitude_to_db(abs(X))
        axs[i, 1].set_title('Spectrogram for audio with {} emotion'.format(emotion), size=12)
        librosa.display.specshow(Xdb, sr=sampling_rate, x_axis='time', y_axis='hz', ax=axs[i, 1])
        axs[i, 1].set_ylabel('Frequency (Hz)')
        axs[i, 1].set_xlabel('Time')

    plt.tight_layout()
    plt.show()


display_all_emotions(CremaD_df)
