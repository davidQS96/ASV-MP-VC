#Importacion de modulos
from tkinter import *


#Clases

#Esta clase se usa para mantener información de tkinter a través de la progresión del programa
class CurrentStateTk:

    #Método constructor
    def __init__(self):
        self.windowStack = {} #Lista de objetos ventana con estructura de stack (First in, Last out)
        self.numWindows = 0

        self.currWindowSet = None

        self.globalElems = {} #Lista/diccionarios con elementos que se usan en todo el programa


    #Método que agrega una ventana en el stack del programa
    #newScreen es un objeto Tk() o Toplevel()
    def addNewWindow(self, newWindow, windowName):

        if(self.numWindows > 0): #Si hay una ventana que se pueda ocultar
            self.getLastStackElement().window.withdraw() #Oculta ventana anterior

        self.currWindowSet = WindowSet(newWindow, windowName)

        self.addToWinStack(self.currWindowSet, windowName)


    #Método que agrega un elemento global
    def addNewGlobElem(self, newElem, elemName):
        self.globalElems[elemName] = newElem


    #Metodo para agregar un widget a la lista de la ventana actual
    def addNewWidgetToCurr(self, newWidget, widgetName):
        self.currWindowSet.addWidgetChild(newWidget, widgetName)


    #Metodo para obtener un widget de la ventana actual
    def getWidgFromCurr(self, widgetKey):
        return self.currWindowSet.childPackOrder[widgetKey]


    #Metodo para obtener un elemento no-widget de la ventana actual
    def getElemFromCurr(self, elemKey):
        return self.currWindowSet.otherElements[elemKey]


    #Metodo para agregar un no-widget a la lista de la ventana actual
    def addNewElemToCurr(self, newElem, elem):
        self.currWindowSet.addNonWidgChild(newElem, elem)


    #Metodo que muestra unicamente ventana anterior en stack, y destruye ventanas posteriores
    def showPrevWindow(self):
        if(self.numWindows > 1): #Verifica que hayan ventanas que se puedan remover, si =1, solo se tiene root
            tempWd = self.removeFromWinStack()
            self.currWindowSet = self.getLastStackElement()
            self.currWindowSet.window.deiconify()
            tempWd.destroy()

    #Metodo que muestra unicamente la primera ventana, es decir, root
    def showFistWindow(self):
        if(self.numWindows > 1): #Verifica que hayan ventanas que se puedan remover, si =1, solo se tiene root
            tempWd = self.removeFromWinStack()
            self.currWindowSet = self.getLastStackElement()
            self.currWindowSet.window.deiconify()
            tempWd.destroy()


    #Agrega nuevo elem al stack. Si existe la llave del elemento, lo edita
    def addToWinStack(self, newElement, objectKey):
        if not (objectKey in self.windowStack.keys()):
            self.numWindows += 1

        self.windowStack[objectKey] = newElement


    #Metodo que remueve y retorna ultimo elem en stack.
    #Si no hay items en windowStack, devuelve nulo
    def removeFromWinStack(self):
        temp = None

        if(self.numWindows > 0):
            temp = self.windowStack.popitem()[-1] #Remueve ultimo elem del stack
            self.numWindows -= 1

        return temp


    #Metodo que retorna ultima ventana objeto de lista
    def getLastStackElement(self):
        temp = self.windowsToList()
        return temp[-1]


    #Metodo que devuelve los elementos del diccionario como una lista, sin las llaves
    def windowsToList(self):
        return list(self.windowStack.values())


#Clase para agrupar ventana y widgets hijos, junto con informacion de cada uno
#Esta clase sirve principalmente para organizar clase CurrentState
class WindowSet:

    #Metodo constructor
    def __init__(self, window ,windowName):
        self.name = windowName
        self.window = window

        self.childPackOrder = {}
        self.otherElements = {}


    #Metodo para asegurarse de eliminar ventana
    def destroy(self):
        self.window.destroy()


    #Agrega widget hijo a diccionario
    def addWidgetChild(self, widget, widgetName):
        self.childPackOrder[widgetName] = widget


    #Agrega hijo no-widget a diccionario
    def addNonWidgChild(self, elem, elemName):
        self.otherElements[elemName] = elem


    #Realiza pack() a todos los hijos de ventana, en el orden en el que se agregaron
    def packAllChildren(self):
        tempItems = list(self.childPackOrder.values())

        for item in tempItems:
            item.pack()


#Clase que permite visualizar o editar datos en tabla dentro del interfaz de tkinter dentro del codigo
class TkDataTable:

    #Metodo constructor
    def __init__(self, root, numRows = 2, numColumns = 2):

        self.numRows = numRows
        self.numColumns = numColumns

        self.cells = []
        self.table = Frame(root, borderwidth = 1, relief = "solid")

        for row in range(numRows):
            rowList = []

            for col in range(numColumns):
                cellDir = {}

                strVar = StringVar()
                cellDir["strVar"] = strVar

                label = Label(self.table, textvariable = strVar, borderwidth = 1, relief = "solid", padx = 3, pady = 3)
                label.grid(column = col, row = row, sticky = N + S + E + W) #sticky en este contexto permite que cada celda rellene todo el espacio disponible que tenga
                cellDir["label"] = label

                rowList += [cellDir]

            self.cells += [rowList]

    #Metodo para agregar un encabezado a la tabla
    #headers es una lista con elementos string que apareceran en la tabla
    def addHeaders(self, headers):
        res = self.addRow(headers, 1)

        #Validacion de datos
        if type(res) == int and res < 0:
            print("TkDataTable.addHeaders: se dio un error en TkDataTable.addRow")
            return -1

        return 0

    #Metodo para agregar una fila a la tabla
    #rowElems es una lista con elementos string que apareceran en la tabla
    #rowNum es el numero de fila a agregar elementos, incluyendo encabezado
    def addRow(self, rowElems, rowNum): #rowNum
        #Verificacion de datos
        if type(rowElems) != list or len(rowElems) > self.numColumns:
            print("TkDataTable.addRow: lista de elementos no válida")
            return -1

        for elem in rowElems:
            if type(elem) != str:
                print("TkDataTable.addRow: algun elemento de lista de entrada no es tipo string")
                return -2

        if type(rowNum) != int or rowNum <= 0 or rowNum > self.numRows + 1:
            print("TkDataTable.addRow: indice de fila no existe en tabla")
            return -3

        #Busca celda en tabla y agrega elemento string
        for ix in range(len(rowElems)):
            self.cells[rowNum - 1][ix]["strVar"].set(rowElems[ix])

        return 0

    #Metodo pack para agregar a ventana
    def pack(self):
        self.table.pack()





