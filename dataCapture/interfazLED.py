import PySimpleGUI as sg
import cv2
import random
import time

updateFreq = 25


    
def main():
    sg.theme("dark grey 9")

    BORDER_COLOR = '#C7D5E0'
    DARK_HEADER_COLOR = '#1B2838'
    BPAD = ((20,10), (20, 10))
    BPAD = ((20,10), (20, 10))

    cont = 0

    top_banner = [[sg.Text('Reconocimiento Facial'+ ' '*60, font='Any 20', background_color=DARK_HEADER_COLOR),
               sg.Text('Nombres', font='Any 20', background_color=DARK_HEADER_COLOR)]]
    
    camera = [[sg.Text('Camera', font='Any 10', background_color=DARK_HEADER_COLOR)],
            [sg.Image(filename="", key="camara")]]
    
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

    # Create the window and show it without the plot
    window = sg.Window("OpenCV Integration", layout, location=(250, 200))

    cap = cv2.VideoCapture(0) # 0 = default camera

    while True:
        cont += 1

        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
        ret, frame = cap.read()
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()
        window["camara"].update(data=imgbytes)
        window['aaa'].update(cont)
        if cont%updateFreq ==0:    
            
    window.close()

main()