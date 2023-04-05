import PySimpleGUI as sg
import cv2
import interfazAux as iAux
import time
cont = 0
updateFreq = 50
directory_filename='C:/Users/juano/Documents/Master MBD/Segundo_Cuatrimestre/Datos no estructurados/RepoGit/FaceDetection/cnn/ModeloPablo20'
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