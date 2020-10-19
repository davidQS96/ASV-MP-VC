#Importación de módulos
import os
from tkinter import filedialog #Manejo de archivos
import ntpath #Nombre de archivo

#-------------------------------------------------------
#Funciones

#Función que muestra al usuario una ventana de búsqueda de archivos
#Devuelve la dirección del archivo de video válido o string de error según sea el caso
def browseVidFile(root):
    
    currdir = os.getcwd()   

    try:
        #https://docs.python.org/3.9/library/dialog.html
        tempdir = filedialog.askopenfilename(parent = root, initialdir = currdir, title = 'Seleccione un archivo de video') #Ventana emergente
        #https://www.thetopsites.net/article/53470882.shtml
        
        if len(tempdir) > 0 and tempdir.lower().endswith(('.avi', '.mp4')): #Archivos de video soportados
            return tempdir

        else:
            #Muestra mensaje de error en caso de que no se elija un archivo adecuado
            return "ARCHIVO_NO_VIDEO"

    except:
        return "NO_CARGADO"


#https://stackoverflow.com/questions/8384737/extract-file-name-from-path-no-matter-what-the-os-path-format
#https://stackoverflow.com/questions/4477850/and-or-operators-return-value#:~:text=Python's%20or%20operator%20returns%20the,assignments%20that%20need%20fallback%20values.&text=This%20will%20print%20my_list%20%2C%20if,is%20None%20...).
#Función devuelve el nombre de archivo en la direccion path
#Path es la direccion de un archivo (o tambien de una carpeta)
def getNameFromPath(path):
    head, tail = ntpath.split(path) #Head es direccion menos nombre de archivo, tail es el resto
    return tail or ntpath.basename(head) #Si tail es vacio, devuelve el nombre base de head (Caso false or true)
    






















