import json
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
from results import Results

def load(filename: str):
    """Loads a trained CNN model and the corresponding preprocessing information.
    Args:
        filename: Relative path to the file without the extension.
    """
    model = tf.keras.models.load_model(filename + '.h5')

    with open(filename + '.json') as f:
        model_name = json.load(f)
    return model

def predict(model,test_dir,dataset_name:str, save: bool = True):
    """Evaluates a new set of images using the trained CNN.
    Args:
        test_dir: Relative path to the validation directory (e.g., 'dataset/test').
        dataset_name: Dataset descriptive name.
        save: Save results to an Excel file.
    """

    print('Reading test data...')
    test_datagen = ImageDataGenerator(rescale=1./255)

    test_generator = test_datagen.flow_from_directory(
        testDirectory,
        target_size = targetSize,
        batch_size=1,  # A batch size of 1 ensures that all test images are processed
        class_mode='categorical',
        shuffle=False
    )

    # Predict categories
    predictions =model.predict(test_generator)
    predicted_labels = np.argmax(predictions, axis=1).ravel().tolist()
    #print(type(test_generator.class_indices))
   
    # Format results and compute classification statistics
    results = Results(test_generator.class_indices, dataset_name=dataset_name)
    accuracy, confusion_matrix, classification = results.compute(test_generator.filenames, test_generator.classes,
                                                                     predicted_labels)
    # Display and save results
    results.print(accuracy, confusion_matrix)



targetSizeWidth = 112
targetSizeHeight = 112
targetSize = (targetSizeWidth, targetSizeHeight)
batchSize = 32
#Path where the model has been stored. It ends with the model file without the extension
directory_filename='D:/OneDrive/Colegio_Uni/Uni/MBD/No estructurados/FaceDetection/ModeloPablo20'
testDirectory='D:/DatosMBD/validation'



cnn=load(directory_filename)
predict(cnn,testDirectory,'validation')