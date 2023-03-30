import PySimpleGUI as sg
import cv2
import os
import interfazAux as iAux

cont = 0

layout = iAux.layout
# Create the window and show it without the plot
window = sg.Window("Interfaz de reconocimiento facial", layout, location=(0, 0))

cap = cv2.VideoCapture(0) # 0 = default camera

while True:
    cont += 1

    event, values = window.read(timeout=10)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    ret, frame = cap.read()

    frame, crop = iAux.rectangle(frame)
    
    imgbytes = cv2.imencode(".png", frame)[1].tobytes()
    window["camara"].update(data=imgbytes)
    window['aaa'].update(cont)

window.close()