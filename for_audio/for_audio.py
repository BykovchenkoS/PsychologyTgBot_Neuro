import pandas as pd
import numpy as np

import os
import sys

import librosa
import librosa.display
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

from IPython.display import Audio

import keras
from keras.callbacks import ReduceLROnPlateau
from keras.models import Sequential
from keras.layers import Dense, Conv1D, MaxPooling1D, Flatten, Dropout, BatchNormalization
from keras.utils import np_utils, to_categorical
from keras.callbacks import ModelCheckpoint

import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")
warnings.filterwarnings("ignore", category=DeprecationWarning)

crema_d_directory = "../cremad/AudioWAV/"
crema_d_files = os.listdir(crema_d_directory)

file_emotion = []
file_path = []

# Цикл для обработки файлов и извлечения информации об эмоциях и путях к файлам
for file in crema_d_files:
    # Строка с эмоцией из имени файла
    emotion = file.split('_')[2]

    if emotion == 'SAD':
        file_emotion.append('sad')
    elif emotion == 'ANG':
        file_emotion.append('angry')
    elif emotion == 'DIS':
        file_emotion.append('disgust')
    elif emotion == 'FEA':
        file_emotion.append('fear')
    elif emotion == 'HAP':
        file_emotion.append('happy')
    elif emotion == 'NEU':
        file_emotion.append('neutral')
    else:
        file_emotion.append('Unknown')

    file_path.append(crema_d_directory + file)

CremaD_df = pd.DataFrame({'Emotions': file_emotion, 'Path': file_path})


