import cv2
import os
import numpy as np 
import interfazAux

cv2.namedWindow("Camara Frontal")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

nombre = 'JuanMerino' 

path = f'C:\\Users\\pcard\\OneDrive\\Colegio_Uni\\Uni\\MBD\\No estructurados\\FaceDetection\\data\\{nombre}'

if not os.path.exists(path):
    os.makedirs(path)
else:
    print('Las imagenes se guardarán en un directorio ya existente, por lo que se sobreescribirán las ya generadas.')

count = 0
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