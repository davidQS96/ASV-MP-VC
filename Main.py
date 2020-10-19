#Bibliotecas

#Importación de módulos
from tkinter import * #Para GUI (filedialog, etc)
from PIL import ImageTk, Image #Manejo de imágenes
from skimage import io
from skimage import color
import numpy as np

#Importación de módulos creados por nosotros
import Módulos.GuiManagement as gm
import Módulos.FileManagement as fm
import Módulos.VidManagement as vm
import Módulos.ImgManagement as im

#-------------------------------------------------------
#Funciones

def getVidDir():
    res = fm.browseVidFile(root)
    errorStrVar = cs.getElemFromCurr("errorStrVar")
    pathStrVar = cs.getElemFromCurr("pathStrVar")
    nameStrVar = cs.getElemFromCurr("nameStrVar")
    imagePI = cs.getElemFromCurr("imagePI")

    imageLbl = cs.getWidgFromCurr("imageLbl")

    if res == "ARCHIVO_NO_VIDEO":
        errorStrVar.set("El archivo elegido no es soportado por el programa.") #288, 180
        return -1

    elif res == "NO_CARGADO":
        errorStrVar.set("No se pudo cargar el archivo, inténtelo nuevamente.")
        return -1


    errorStrVar.set("")
    pathStrVar.set("Dirección: " + res)

    name = fm.getNameFromPath(res)
    
    nameStrVar.set("Nombre: " + name)

    image = vm.getFirstFrame(res)

    if image == "PRIMER_CUADRO_NO_GENERADO":
        errorStrVar.set("No se pudo generar una vista previa del video.")
        return -1

    image = im.resizeConstRatio(image, (288, 180))

    if image == "DIMENSIONES_NO_VALIDAS":
        errorStrVar.set("Todas las dimensiones dadas deben ser mayores a 0.")
        return -1

    imagePI = ImageTk.PhotoImage(image)
    imageLbl.configure(image = imagePI)
    imageLbl.image = imagePI
    
    return 0
                

#-------------------------------------------------------
#Funciones para cada ventana

#Esta función muestra la ventana inicial del programa 
def selectWindow():

    #Directorio y nombre del video    
    pathStrVar = StringVar()
    cs.addNewGlobElem(pathStrVar, "pathStrVar")
    nameStrVar = StringVar()
    cs.addNewGlobElem(nameStrVar, "nameStrVar")

    #Widgets y similares
    titleLbl = Label(root, text = cs.globalElems["title"])

    #http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
    #https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python#:~:text=To%20display%20images%20in%20labels,is%20present%20in%20tkinter%20package.&text=%22PhotoImage()%22%20function%20returns%20the%20image%20object.&text=To%20display%20image%20in%20Python,GIF%20and%20PGM%2FPPM%20formats.
    imagePI = ImageTk.PhotoImage(Image.open("Archivos de programa/vistaPrevia.png"))
    imageLbl = Label(root, image = imagePI)
    imageLbl.image = imagePI # keep a reference!

    vidNameLbl = Label(root, textvariable = nameStrVar)    
    filePathLbl = Label(root, textvariable = pathStrVar)
    browseBtn = Button(root, text = "Buscar video", command = getVidDir)
    nextBtn = Button(root, text = "Siguiente", command = None)
    errorStrVar = StringVar("")
    errorLbl = Label(root, textvariable = errorStrVar)

    #Agrega Widgets a padre
    cs.addNewWidgetToCurr(titleLbl, "titleLbl")
    cs.addNewWidgetToCurr(imageLbl,"imageLbl")
    cs.addNewWidgetToCurr(vidNameLbl,"vidNameLbl")
    cs.addNewWidgetToCurr(filePathLbl,"filePathLbl")
    cs.addNewWidgetToCurr(browseBtn,"browseBtn")
    cs.addNewWidgetToCurr(errorLbl,"errorLbl")
    cs.addNewWidgetToCurr(nextBtn,"nextBtn")

    cs.addNewElemToCurr(pathStrVar, "pathStrVar")
    cs.addNewElemToCurr(nameStrVar, "nameStrVar")
    cs.addNewElemToCurr(imagePI, "imagePI")
    cs.addNewElemToCurr(errorStrVar,"errorStrVar")

    #Coloca widgets en pantalla
    cs.currWindowSet.packAllChildren()


#-------------------------------------------------------
#Programa principal
    
#Pantalla raíz
root = Tk()

#Crea instancia global de CurrentState y guarda root
cs = gm.CurrentStateTk()
cs.addNewWindow(root, "root")
cs.addNewGlobElem("Miniproyecto: Uso de visión para mediciones en entornos", "title")

#Se abre pantalla inicial
selectWindow()

#Comienza loop para mantener GUI
root.mainloop()



































