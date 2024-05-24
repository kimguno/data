########################
###     data        ###
#######################

import os
import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf
import pathlib

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

data_dir="C:/waytoMap/fruitCNN/fruits"
data_dir = pathlib.Path(data_dir)
image_count = len(list(data_dir.glob('*/*.jpg')))

batch_size=64
img_height=180
img_width=180

train_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=99,
    image_size=(img_height, img_width),
    batch_size=batch_size
)
val_ds = tf.keras.utils.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=99,
    image_size=(img_height, img_width),
    batch_size=batch_size
)
class_names = train_ds.class_names
num_classes = len(class_names)
# print(class_names)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
    layers.RandomBrightness(factor=0.3),
    layers.RandomZoom(.5 , .2)
])

model = Sequential([
    data_augmentation,
    layers.Rescaling(1./255, input_shape=(img_height, img_width, 10)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),
    # layers.Dropout(0.2),
    layers.Conv2D(32, 3, padding='same', activation='relu', kernel_initializer='he_normal'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),
    # layers.Dropout(0.2),
    layers.Conv2D(64, 3, padding='same', activation='relu', kernel_initializer='he_normal'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),
    # layers.Dropout(0.2),
    layers.Conv2D(128, 3, padding='same', activation='relu', kernel_initializer='he_normal'),
    layers.BatchNormalization(),
    layers.MaxPooling2D(),
    # layers.Dropout(0.2),
    layers.Conv2D(256, 3, padding='same', activation='relu', kernel_initializer='he_normal'),
    layers.BatchNormalization(),
    layers.GlobalAveragePooling2D(),
    layers.Flatten(),
    layers.Dropout(0.6),
    layers.Dense(256, activation='relu', kernel_initializer='he_normal'),
    layers.Dense(128, activation='relu', kernel_initializer='he_normal'),
    layers.Dense(64, activation='relu', kernel_initializer='he_normal'),
    layers.Dense(32, activation='relu', kernel_initializer='he_normal'),
    layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

from keras.callbacks import EarlyStopping, ModelCheckpoint
early_stopping = EarlyStopping(monitor='val_accuracy', min_delta=0.01,patience = 80)
model_checkpoint = ModelCheckpoint('fruitCNN.keras', monitor='val_accuracy', mode='max', verbose=1, save_best_only=True)

epochs=2000
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    callbacks = [early_stopping, model_checkpoint]
)

# model.save('fruitCNN.keras')

# acc = history.history['accuracy']
# val_acc = history.history['val_accuracy']

# loss = history.history['loss']
# val_loss = history.history['val_loss']

# epochs_range = range(epochs)

# plt.figure(figsize=(8,8))

# plt.subplot(1,2,1)
# plt.plot(epochs_range, acc, label='Training Accuracy')
# plt.plot(epochs_range, val_acc, label='Validadtion Accuracy')
# plt.legend(loc='lower right')
# plt.title('Training and Validation Accuracy')

# plt.subplot(1,2,2)
# plt.plot(epochs_range, loss, label='Training Loss')
# plt.plot(epochs_range, val_loss, label='Validadtion Loss')
# plt.legend(loc='upper right')
# plt.title('Training and Validation Loss')

# plt.show()

# base(epchs=15) : loss: 0.0188 - accuracy: 0.9977 - val_loss: 3.7636 - val_accuracy: 0.4841
# autotune(epchs=15) : loss: 0.0219 - accuracy: 0.9960 - val_loss: 3.9260 - val_accuracy: 0.4068
# data_augment(epchs=15) : loss: 1.2797 - accuracy: 0.5756 - val_loss: 1.4045 - val_accuracy: 0.5386
# +1 dense(epchs=33) : loss: 0.9694 - accuracy: 0.6744 - val_loss: 1.5189 - val_accuracy: 0.5182
# earlystop(epochs=15) : loss: 1.4471 - accuracy: 0.4915 - val_loss: 1.4695 - val_accuracy: 0.4841
# +1 Convolution Layers(epchs=6) : loss: 1.7578 - accuracy: 0.3528 - val_loss: 1.8906 - val_accuracy: 0.3205
# relu to softmax(epochs=8)(x) : loss: 2.2262 - accuracy: 0.1625 - val_loss: 2.2340 - val_accuracy: 0.1614
# loss: 1.1999 - accuracy: 0.5591 - val_loss: 1.4360 - val_accuracy: 0.5250

# data +300(epochs=30) : loss: 0.6898 - accuracy: 0.7638 - val_loss: 1.0846 - val_accuracy: 0.6850
# dropout 0.2(epochs=33)(x) : loss: 0.6341 - accuracy: 0.7835 - val_loss: 1.4306 - val_accuracy: 0.5664
# +1 conv : loss: 0.6332 - accuracy: 0.7841 - val_loss: 1.3882 - val_accuracy: 0.5947
# dropout(0.3)(epochs=44) : loss: 0.5958 - accuracy: 0.7956 - val_loss: 1.1010 - val_accuracy: 0.6956
# +1 dense(epochs=44)(x) : loss: 0.6735 - accuracy: 0.7742 - val_loss: 1.3613 - val_accuracy: 0.5779
# -2 conv(epochs=27)(x) : loss: 0.8539 - accuracy: 0.7080 - val_loss: 1.1259 - val_accuracy: 0.6372
# dropout(0.4)(epochs=23)(x) : loss: 0.9791 - accuracy: 0.6704 - val_loss: 1.2838 - val_accuracy: 0.5646
# dropout(0.4)(epochs=)(x) : loss: 0.9791 - accuracy: 0.6704 - val_loss: 1.2838 - val_accuracy: 0.5646
# dropout(0.2)(epochs=32)(x) : loss: 0.7278 - accuracy: 0.7587 - val_loss: 1.3242 - val_accuracy: 0.5947