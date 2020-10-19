import skimage as sk
from skimage import io

path = "D:/OneDrive - Estudiantes ITCR/Documentos/TEC/2020 - 2S/Sistemas de Visión Gr. 1/Tareas Parciales/Tarea 1/T1-Repositorio/Imágenes Prueba/vistaPrevia.png"

img = io.imread(path)

print(type(img))

lista = img.tolist()

print(lista)


