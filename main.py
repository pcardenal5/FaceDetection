#This python file is mean to englobe an use all the different modules he have created during the project

import PySimpleGUI as sg
import cv2
import interface.interfazAux as iAux
import time
import argparse

# Crea un objeto ArgumentParser
parser = argparse.ArgumentParser()

# Agrega el argumento -path
parser.add_argument('-path', type=str, help='Ruta completa a la carpeta principal FaceDetection')

# Parsea los argumentos de la línea de comandos
args = parser.parse_args()
directory_filename='/cnn/ModeloPablo20'
# Accede al valor del argumento -path
directory_filename = args.path + directory_filename
cont = 0
updateFreq = 50

layout = iAux.layout
# Create the window and show it without the plot
window = sg.Window("Interfaz de reconocimiento facial", layout, location=(0, 0))
cnn=iAux.load(directory_filename)
cap = cv2.VideoCapture(0) # 0 = default camera

while True:
    cont += 1

    event, values = window.read(timeout=10)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    ret, frame = cap.read()

    frame, crop = iAux.rectangle(frame,cont)
    
    imgbytes = cv2.imencode(".png", frame)[1].tobytes()
    window["camara"].update(data=imgbytes)
    window['aaa'].update(cont)
    if cont%updateFreq ==0:    
        iAux.UpdateLed(window, crop,cnn)

window.close()