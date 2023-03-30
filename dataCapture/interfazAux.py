import cv2
import PySimpleGUI as sg



def rectangle(frame):
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
    key = cv2.waitKey(20)
    return frame, crop




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

block = [[sg.Text('Categorías:', font='Any 10')],
            [sg.T('A: No hay ninguna cara', pad=pad)],
            [sg.T('B: Hay cara pero no es reconocida', pad=pad)],
            [sg.T('C: Aparece la cara de Pablo', pad=pad)],
            [sg.T('D: Aparece la cara de Juan', pad=pad)],
            [sg.T('E: Aparece la cara de Juanmi', pad=pad)],
            [sg.T('', key='aaa', pad=pad)]]

# Define the window layout
layout = [
    [sg.Column(top_banner, size=(1350, 50), pad=(5,5), background_color=DARK_HEADER_COLOR)],
    [sg.Column(camera, size=(650,530),pad=BPAD, background_color=BORDER_COLOR),
    sg.Column(block, size=(650,530), pad=BPAD, background_color=BORDER_COLOR)]
]