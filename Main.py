#Bibliotecas

#Importación de módulos
from tkinter import * #Para GUI (filedialog, etc)
from PIL import ImageTk, Image #Manejo de imágenes
# from skimage import io
# from skimage import color
from threading import * #Para abrir procesos de tkinter y cv2 al mismo tiempo
import numpy as np
import cv2
import os
import threading as thr #Tareas en paralelo, para abrir ventanas de tk y cv2 al mismo tiempo

#Importación de módulos creados por nosotros
import Módulos.GuiManagement as gm
import Módulos.FileManagement as fm
import Módulos.VidManagement as vm
import Módulos.ImgManagement as im
import Módulos.DeteccObjetos as do

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

    cs.globalElems["vidPath"]

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
    cs.globalElems["vidPath"] = res

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
    vidPath = cs.globalElems["vidPath"]

    currDir = os.getcwd()
    relPath = os.path.relpath(vidPath, currDir)

    cap = cv2.VideoCapture(relPath)

    scaleFactor = cs.globalElems["scaleFactor"] * 2 #Se duplica para que se vea mas grande

    while True:
        ret, frame = cap.read()

        #https://stackoverflow.com/questions/47788247/python-opencv-how-do-i-detect-when-a-video-finishes-playing
        if ret: #ret es verdadero si videocapture no ha leido todos los frames del video aun
            nframe = vm.rescale_frame(frame, scale = scaleFactor)
            cv2.imshow('Video analizado', nframe)

            if cv2.waitKey(1) & 0xFF == ord('q') or cs.globalElems["ableToCloseVidWindow"]:
                break

        else:
            while cv2.waitKey(1) & 0xFF != ord('q') and not cs.globalElems["ableToCloseVidWindow"]:
                pass

            break

def showLoadingWindow():
    loadingWd = Toplevel(root)
    Label(loadingWd, text = "Analizando video ...", padx = 20, pady = 20).pack()
    cs.addNewGlobElem(loadingWd, "loadingWd")


#Esta funcion convierte los datos obtenidos de DeteccObjetos a datos faciles de interpretar y mostrar en el GUI
#generatedNDArray es una lista tipo ndarray con la info generada
#Devuelve la info de objetos detectados
def translateGenerated(generatedNDArray):
    trackDict = {"1": "Pista 1 (amarilla)", "2": "Pista 2 (azul)", "3": "Pista 3 (roja)"}
    directDict = {"0": "Der. a izq.", "1": "Izq. a der."}

    cont = 1
    generatedList = []

    for track in generatedNDArray:
        trackInfo = track.tolist() #Convierte ndarray a lista

        #Cambio de primer elemento
        if trackInfo[0] != 1:
            cont += 1
            continue

        trackInfo[0] = trackDict[str(cont)]
        temp = str(trackInfo[1])
        trackInfo[1] = directDict[str(int(trackInfo[2]))]
        trackInfo[2] = temp

        generatedList += [trackInfo]

        cont += 1

    return generatedList




#Funcion para eliminar la actual ventana y volver a la anterior
def showPrevWindow():
    cs.globalElems["ableToCloseVidWindow"] = True
    cs.showPrevWindow()

#Funcion para reiniciar todo el proceso de seleccion desde 0
def reopenSelectWindow():
    cs.globalElems["ableToCloseVidWindow"] = True
    cs.showPrevWindow() #Esto borra la ultima ventana, pero muestra la anterior
    selectWindow() #Al correr esto nuevamente, se reinicia el interfaz


#Funcion para permitir que se cierre ventana de opencv tambien
def closingStateWindow():
    cs.globalElems["ableToCloseVidWindow"] = True
    root.destroy()

def exitProgram():
    cs.globalElems["ableToCloseVidWindow"] = True
    root.destroy()



#-------------------------------------------------------
#Funciones para cada ventana

#Esta función muestra la ventana inicial se selección del programa
def selectWindow():

    for widget in root.winfo_children():
        widget.pack_forget()

    #Directorio y nombre del video
    pathStrVar = StringVar()
    cs.addNewGlobElem(pathStrVar, "pathStrVar")
    nameStrVar = StringVar()
    cs.addNewGlobElem(nameStrVar, "nameStrVar")

    vidPath = ""
    cs.addNewGlobElem(vidPath, "vidPath")

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
    cs.addNewGlobElem(False, "ableToCloseVidWindow")

    #Verificacion de archivo correcto
    if(not canContinue or pathStrVar.get() == ""):
        errorStrVar = cs.getElemFromCurr("errorStrVar")
        errorStrVar.set("Elija primero un video válido")

        cs.globalElems["canContinue"] = False
        return -1

    print("Analizando video...")

    stateWd = Toplevel(root)
    stateWd.protocol("WM_DELETE_WINDOW", closingStateWindow) #Accion cuando se cierra la ventana
    cs.addNewWindow(stateWd, "stateWd")

    title = cs.globalElems["title"]

    #Widgets y similares
    titleLbl = Label(stateWd, text = title)

    #Tabla de datos
    stateTbl = gm.TkDataTable(stateWd, 7, 3)
    stateTbl.addHeaders(["No. Pista", "Dirección", "Velocidad (cm/s)"])

    vidPath = cs.globalElems["vidPath"]

    currDir = os.getcwd()
    relPath = os.path.relpath(vidPath, currDir)

    #Se generan los datos del estado de cada pista
    dataList = do.contornos(relPath)

    trueDataList = translateGenerated(dataList)
    cont = 1

    for track in trueDataList:
        stateTbl.addRow(track, cont + 1)
        cont += 1

    #nextBtn = Button(stateWd, text = "Cargar otro video", command = reopenSelectWindow)
    #backBtn = Button(stateWd, text = "Volver", command = showPrevWindow)
    exitBtn = Button(stateWd, text = "Salir", command = exitProgram)

    #Agrega Widgets a padre
    cs.addNewWidgetToCurr(titleLbl, "titleLbl")
    cs.addNewWidgetToCurr(stateTbl, "stateTbl")
    #cs.addNewWidgetToCurr(nextBtn,"nextBtn")
   # cs.addNewWidgetToCurr(backBtn, "backBtn")
    cs.addNewWidgetToCurr(exitBtn, "exitBtn")


    #Coloca widgets en pantalla
    cs.currWindowSet.packAllChildren()

    thr.Thread(target=showVidWindow).start() #Carga aqui para que se pueda cargar lo anterior



#-------------------------------------------------------
#Programa principal

#Pantalla raíz
root = Tk()

icon = PhotoImage(file = "Archivos de programa/icono.png")
root.iconphoto(True, icon)


#Crea instancia global de CurrentState y guarda root
cs = gm.CurrentStateTk()
cs.addNewWindow(root, "root")
cs.addNewGlobElem("Miniproyecto: Uso de visión para mediciones en entornos", "title")
cs.addNewGlobElem(False, "canContinue")

root.title("Miniproyecto")

#Se abre pantalla inicial
selectWindow()


#Comienza loop para mantener GUI
root.mainloop()



































