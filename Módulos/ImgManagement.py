#Importación de módulos
import cv2
import numpy as np
from PIL import Image

#-------------------------------------------------------
#Funciones

#Función que escala imagen para que se ajuste a la ventana con tamaño winDim
#image es un objeto PIL.Image
#winDim es una tupla (x, y) de la ventana en la que la imagen se ajusta
#Devuelve imagen como objeto PIL.Image, o un mensaje de error si alguna de las dimensiones es menor o igual a 0
#Devuelve tambien el factor de escala por si se necesita
def resizeConstRatio(image, winDim):
    x, y = image.size
    xM, yM = winDim

    if xM <= 0 or yM <= 0:
        return "DIMENSIONES_NO_VALIDAS", -1

    scaleFactor = 1

    relX, relY = (x / xM, y / yM)

    if relX > 1:
        if relY > 1:
            if relX > relY:
                scaleFactor = 1 / relX
            else:
                scaleFactor = 1 / relY

        else:
            scaleFactor = 1 / relX
    else:
        if relY > 1:
            scaleFactor = 1 / relY

        else:
            if relX > relY:
                scaleFactor = 1 / relX
            else:
                scaleFactor = 1 / relY

    newImgSize = (round(x * scaleFactor), round(y * scaleFactor))
    return image.resize(newImgSize, Image.ANTIALIAS), scaleFactor



























