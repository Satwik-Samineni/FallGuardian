import numpy as np
from keras.models import Sequential
from keras.layers import *
import pandas as pd
import glob

data = pd.read_csv("/content/falldetectiondata.csv")

data.head(100)

np.unique(data["class"])

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense, Flatten, Reshape, Conv1D, MaxPooling1D
from keras.utils import to_categorical

# Extract features (X) and labels (y)
X = data.iloc[:, 1:-1].values  # Assuming the features are in the first 23 columns
y = data.iloc[:, -1].values   # Assuming the labels are in the last column
print(y.shape,X.shape)

# Standardize features

# Convert labels to one-hot encoding
y.shape

def create_baseline():
    model = Sequential()

    model.add(Conv1D(filters=64, kernel_size=3, padding='same', activation='relu', input_shape=(6, 1)))
    model.add(Conv1D(filters=32, kernel_size=3, padding='same', activation='relu'))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid', kernel_regularizer='l2'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
# Train the model

model = create_baseline()

hist = model.fit(X,y,epochs=10,validation_data=(X,y))

import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import seaborn as sns

y_pred = model.evaluate(X,y)

y_pred

# Plotting train and validation accuracy across epochs
plt.figure(figsize=(10, 6))
plt.plot(hist.history['accuracy'], label='Train Accuracy')
plt.plot(hist.history['val_accuracy'], label='Validation Accuracy')
plt.title('Train and Validation Accuracy Across Epochs')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()


#This tflite Model For Testing In Raspberry Pi
import tensorflow as tf
from tensorflow.keras.models import load_model
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_quant_model = converter.convert()
open("converted_model.tflite", "wb").write(tflite_quant_model)

#This Can Be Used For Google Colab Testing
from keras.models import load_model

model.save('Fall_Detection.h5')