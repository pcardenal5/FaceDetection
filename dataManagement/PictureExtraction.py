import cv2
import os
import numpy as np 
from ..interface import interfazAux

cv2.namedWindow("Camara Frontal")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

nombre = 'JuanO' 

path = f'C:\\Users\\juano\\Documents\\Master MBD\\Segundo_Cuatrimestre\\Datos no estructurados\\RepoGit\\FaceDetection\\data\\JuanO'

if not os.path.exists(path):
    os.makedirs(path)
    count = 0
else:
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f))]
    l = len(files)
    count = l
    print(f'Se han encontrado {l} imágenes en el directorio. Se crearán nuevas')


while rval:
    cv2.imshow("Camara Frontal", frame)
    count +=1
    rval, frame = vc.read()
    frame, crop = interfazAux.rectangle(frame)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    cv2.imwrite(os.path.join(path , f"{nombre}{count}.jpg"), crop)
    
cv2.destroyWindow("Camara Frontal")
vc.release()