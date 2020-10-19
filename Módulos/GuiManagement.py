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


    #Metodo destructor
    def __del__(self):
        self.window.destroy()
        

    #Metodo para asegurarse de eliminar ventana
    def destroy(self):
        self.__del__()


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


