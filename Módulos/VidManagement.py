#Importación de módulos
import cv2
import numpy as np
from PIL import Image

#-------------------------------------------------------
#Funciones

#Función que devuelve un objeto Image con la imagen del primer cuadro del video seleccionado
#Path es la direccion del video
#Devuelve error si no se logro leer el video
def getFirstFrame(path):    

    #https://python-forum.io/Thread-OpenCV-extract-1st-frame-out-of-a-video-file
    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    if success:
      cv2.imwrite("Archivos de programa/firstFrame.jpg", image)     # save frame as JPEG file
      return Image.open(r"Archivos de programa/firstFrame.jpg")

    else:
        return "PRIMER_CUADRO_NO_GENERADO"



  























