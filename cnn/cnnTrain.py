#Importing libraries

import json
import tensorflow as tf
import os
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
from keras.callbacks import EarlyStopping


#Auxiliar functions
def save(model, filename: str, model_name: str):
    """Saves the model to an .h5 file and the model name to a .json file.
    Args:
        model: Model to be saved
        filename: Relative path to the file without the extension.
        
    """
    model.save(filename + '.h5')

    with open(filename + '.json', 'w', encoding='utf-8') as f:
        json.dump(model_name, f, ensure_ascii=False, indent=4, sort_keys=True)

def _plot_training(history):
    """Plots the evolution of the accuracy and the loss of both the training and validation sets.
    Args:
        history: Training history.
    """
    training_accuracy = history.history['accuracy']
    validation_accuracy = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(len(training_accuracy))

    # Accuracy
    plt.figure()
    plt.plot(epochs, training_accuracy, 'r', label='Training accuracy')
    plt.plot(epochs, validation_accuracy, 'b', label='Validation accuracy')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    # Loss
    plt.figure()
    plt.plot(epochs, loss, 'r', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()


#--------------------- Building CNN --------------------#
def create_model():
        
    cnn = tf.keras.models.Sequential()

    #We create 4 convolutional 'blocks', consisting of a convolutional and a pooling layer 
    cnn.add(tf.keras.layers.Conv2D(filters= 64 , kernel_size = 2, activation = 'relu', input_shape=[targetSize[0],targetSize[1],3]))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2 ,strides=2))

    cnn.add(tf.keras.layers.Conv2D(filters = 64, kernel_size = 2,padding='same', activation = 'relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2 ,strides=2))

    cnn.add(tf.keras.layers.Conv2D(filters = 128, kernel_size = 2,padding='same', activation = 'relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2 ,strides=2))

    cnn.add(tf.keras.layers.Conv2D(filters = 128, kernel_size = 2,padding='same', activation = 'relu'))
    cnn.add(tf.keras.layers.MaxPool2D(pool_size=2 ,strides=2))

    #finally, we flatten the final layer to make the classification output layer
    cnn.add(tf.keras.layers.Flatten())
    cnn.add(tf.keras.layers.Dense(units = 512, activation = 'relu'))

    cnn.add(tf.keras.layers.Dense(units = 5, activation = 'sigmoid'))

    return cnn

#Change accordingly to train with different data sets.
dataDir = 'D:/DatosMBD/'

#Now we set important parameters for our CNN
targetSizeWidth = 112
targetSizeHeight = 112
targetSize = (targetSizeWidth, targetSizeHeight)
batchSize = 32 

train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2) 
#We dont want the dataset to be flipped as orientation is important, so we don't include the horizontal_flip parameter
train_set = train_datagen.flow_from_directory(
        os.path.join(dataDir, '/train/'),
        target_size = targetSize,
        batch_size=batchSize,
        class_mode='categorical')


test_datagen = ImageDataGenerator(rescale=1./255)
test_set = test_datagen.flow_from_directory(
        os.path.join(dataDir, '/test/'),
        target_size = targetSize,
        batch_size = batchSize,
        class_mode = 'categorical')


#only rescaling but no transformations
validation_datagen = ImageDataGenerator(rescale=1./255)
val_set = validation_datagen.flow_from_directory(
        os.path.join(dataDir, '/validation/'),
        target_size = targetSize,
        batch_size = batchSize,
        class_mode = 'categorical')




#--------------------- Training the CNN --------------------#

#Important parameters:
epochs=20

cnn=create_model()
cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
#training the CNN on the training set and evaluating it on the test set

print("\n\nTraining CNN...")
early_stopping_monitor = EarlyStopping(patience=4)
history = cnn.fit(
    train_set,
    epochs=epochs,
    steps_per_epoch=batchSize,
    validation_data=test_set,
    validation_steps=batchSize,
    callbacks=[early_stopping_monitor]
    #callbacks=callbacks
)
if epochs > 1:
    _plot_training(history)




#Once the CNN has been trained we save it in order to use it on the interface module.
save(cnn,f'./ModeloPablo{epochs}','CNN_trainingModel')