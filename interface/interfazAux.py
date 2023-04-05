import cv2
import PySimpleGUI as sg
import random
from keras.utils import load_img, img_to_array
import numpy as np
import tensorflow as tf
import json
from keras.preprocessing.image import ImageDataGenerator

def rectangle(frame,cont):
    y, x, _ = frame.shape
    h = 112*2
    w = h
    startY = int((y-h)/2)
    endY = int((y+h)/2)
    startX = int((x-w)/2)
    endX = int((x+w)/2)
    color = (255,0,0)
    thickness = 2
    cv2.rectangle(frame,(startX-10, startY-10), (endX+10,endY+10), color, thickness)
    crop = frame[
            startY:endY, 
            startX:endX,
            :]
    crop = cv2.resize(crop, (112,112))
    #cv2.imwrite('C:/Users/juano/Documents/Master MBD/Segundo_Cuatrimestre/Datos no estructurados/RepoGit/FaceDetection/data/JuanM/JuanM'+str(cont)+'.jpeg', crop) 
    key = cv2.waitKey(20)
    return frame, crop

def LEDIndicator(key=None, radius=30):
    return sg.Graph(canvas_size=(radius, radius),
             graph_bottom_left=(-radius, -radius),
             graph_top_right=(radius, radius),
             pad=(0, 0), key=key)

def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)


def UpdateLed(window, crop,cnn): #cnn
    targetSizeWidth = 112
    targetSizeHeight = 112
    targetSize = (targetSizeWidth, targetSizeHeight)
    # to convert image in pii format into a numpy array format
    test_image = img_to_array(crop)
    # adding extra dimension to put this image into a batch by saying where we want to add this batch (as the first dimension)
    test_image = np.expand_dims(test_image, axis = 0)
    test_datagen = ImageDataGenerator(rescale=1./255)

    test_generator = test_datagen.flow(
        x=test_image,
        batch_size=1,  # A batch size of 1 ensures that all test images are processed
        shuffle=False
    )
    # cnn prediction on the test image
    predict = cnn.predict(test_generator)
    predicted_labels = np.argmax(predict, axis=1).ravel().tolist()
    print("New predict",predicted_labels[0])
    SetLED(window, 'no_cara', 'green' if predicted_labels[0]==4 else 'red')
    SetLED(window, 'cara_reconocida', 'green' if predicted_labels[0]==0 else 'red')
    SetLED(window, 'pablo', 'green' if predicted_labels[0]==3  else 'red')
    SetLED(window, 'juan', 'green' if predicted_labels[0]==2 else 'red')
    SetLED(window, 'juanmi', 'green' if predicted_labels[0]==1  else 'red')
def load(filename: str):
    """Loads a trained CNN model and the corresponding preprocessing information.
    Args:
        filename: Relative path to the file without the extension.
    """
    model = tf.keras.models.load_model(filename + '.h5')

    with open(filename + '.json') as f:
        model_name = json.load(f)
    return model

sg.theme("dark grey 9")

BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD = ((20,10), (20, 10))
BPAD = ((20,10), (20, 10))

BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD = ((20,10), (20, 10))
BPAD = ((20,10), (20, 10))

top_banner = [[sg.Text('Reconocimiento Facial'+ ' '*60, font='Any 20', background_color=DARK_HEADER_COLOR),
            sg.Text('Nombres', font='Any 20', background_color=DARK_HEADER_COLOR)]]

camera = [[sg.Text('Camera', font='Any 10', background_color=DARK_HEADER_COLOR)],
        [sg.Image(filename="", key="camara")]]

pad = (10,30)

block = [[sg.Text('Categorías:', font='Any 10', background_color=DARK_HEADER_COLOR)],
        [sg.T('A: No hay ninguna cara', pad=(10,30)), LEDIndicator('no_cara')],
        [sg.T('B: Hay cara pero no es reconocida', pad=(10,30)), LEDIndicator('cara_reconocida')],
        [sg.T('C: Aparece la cara de Pablo', pad=(10,30)), LEDIndicator('pablo')],
        [sg.T('D: Aparece la cara de Juan', pad=(10,30)), LEDIndicator('juan')],
        [sg.T('E: Aparece la cara de Juanmi', pad=(10,30)), LEDIndicator('juanmi')],
        [sg.T('', key='aaa', pad=(10,30))]]

# Define the window layout
layout = [
    [sg.Column(top_banner, size=(1350, 50), pad=(5,5), background_color=DARK_HEADER_COLOR)],
    [sg.Column(camera, size=(650,530),pad=BPAD, background_color=BORDER_COLOR),
    sg.Column(block, size=(650,530), pad=BPAD, background_color=BORDER_COLOR)]
]
