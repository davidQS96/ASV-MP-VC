#Bibliotecas

#Importación de módulos
from tkinter import * #Para GUI (filedialog, etc)
from PIL import ImageTk, Image #Manejo de imágenes
from skimage import io
from skimage import color
import numpy as np
import cv2

#Importación de módulos creados por nosotros
import Módulos.GuiManagement as gm
import Módulos.FileManagement as fm
import Módulos.VidManagement as vm
import Módulos.ImgManagement as im

#-------------------------------------------------------
#Funciones

#Esta funcion guarda la ruta de un archivo valido, e imprime en pantalla el mismo, el nombre y una imagen previa
#Resulta en error en donde se de
#Ademas, permite continuar con el programa si todo salio bien
def getVidDir():
    res         = fm.browseVidFile(root)
    errorStrVar = cs.getElemFromCurr("errorStrVar")
    pathStrVar  = cs.getElemFromCurr("pathStrVar")
    nameStrVar  = cs.getElemFromCurr("nameStrVar")
    imagePI     = cs.getElemFromCurr("imagePI")

    imageLbl = cs.getWidgFromCurr("imageLbl")

    if res == "ARCHIVO_NO_VIDEO":
        errorStrVar.set("El archivo elegido no es soportado por el programa.")
        cs.globalElems["canContinue"] = False
        return -1

    elif res == "NO_CARGADO":
        errorStrVar.set("No se pudo cargar el archivo, inténtelo nuevamente.")
        cs.globalElems["canContinue"] = False
        return -1


    errorStrVar.set("")
    pathStrVar.set("Dirección: " + res)

    name = fm.getNameFromPath(res)

    nameStrVar.set("Nombre: " + name)

    image = vm.getFirstFrame(res)

    if image == "PRIMER_CUADRO_NO_GENERADO":
        errorStrVar.set("No se pudo generar una vista previa del video.")
        return -1

    image, scaleFactor = im.resizeConstRatio(image, (288, 180))

    if image == "DIMENSIONES_NO_VALIDAS":
        errorStrVar.set("Todas las dimensiones dadas deben ser mayores a 0.")
        cs.globalElems["canContinue"] = False
        return -1

    cs.addNewGlobElem(scaleFactor, "scaleFactor")

    imagePI = ImageTk.PhotoImage(image)
    imageLbl.configure(image = imagePI)
    imageLbl.image = imagePI

    cs.globalElems["canContinue"] = True

    return 0


### https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
#Esta funcion muestra la ventana con el video a analizar
def showVidWindow():
    pathStrVar = cs.globalElems["pathStrVar"]
    cap = cv2.VideoCapture("vid1_Trim.mp4")

    scaleFactor = cs.globalElems["scaleFactor"] * 2 #Se duplica para que se vea mas grande

    while True:
        rect, frame = cap.read()
        nframe = vm.rescale_frame(frame, scale = scaleFactor)
        cv2.imshow('nframe', nframe)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break




#-------------------------------------------------------
#Funciones para cada ventana

#Esta función muestra la ventana inicial se selección del programa
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
    nextBtn = Button(root, text = "Siguiente", command = stateWindow)
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


#Funcion abre la ventana 2 del programa sobre tabulacion del estado de las pistas
def stateWindow():
    pathStrVar = cs.globalElems["pathStrVar"]
    canContinue = cs.globalElems["canContinue"]

    #Verificacion de archivo correcto
    if(not canContinue or pathStrVar.get() == ""):
        errorStrVar = cs.getElemFromCurr("errorStrVar")
        errorStrVar.set("Elija primero un video válido")

        cs.globalElems["canContinue"] = False
        return -1


    stateWd = Toplevel(root)
    cs.addNewWindow(stateWd, "stateWd")

    title = cs.globalElems["title"]

    #Widgets y similares
    titleLbl = Label(stateWd, text = title)

    backBtn = Button(stateWd, text = "Volver", command = cs.showPrevWindow)
    nextBtn = Button(stateWd, text = "Siguiente", command = None)

    #Agrega Widgets a padre
    cs.addNewWidgetToCurr(titleLbl, "titleLbl")
    cs.addNewWidgetToCurr(backBtn, "backBtn")
    cs.addNewWidgetToCurr(nextBtn,"nextBtn")


    #Coloca widgets en pantalla
    cs.currWindowSet.packAllChildren()

    showVidWindow() #Carga aqui para que se pueda cargar lo anterior







#-------------------------------------------------------
#Programa principal

#Pantalla raíz
root = Tk()

#Crea instancia global de CurrentState y guarda root
cs = gm.CurrentStateTk()
cs.addNewWindow(root, "root")
cs.addNewGlobElem("Miniproyecto: Uso de visión para mediciones en entornos", "title")
cs.addNewGlobElem(False, "canContinue")

#Se abre pantalla inicial
selectWindow()

#Comienza loop para mantener GUI
root.mainloop()



































