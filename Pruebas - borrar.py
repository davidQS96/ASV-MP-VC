from PIL import ImageTk
import PIL.Image
import skimage
import cv2
import numpy as np
from tkinter import *



import Módulos.VidManagement as vm
import Módulos.ImgManagement as im




image = vm.getFirstFrame("vid1.mp4")

root = Tk()
    
image = im.resizeConstRatio(image, (1000, 200))

imagePI = ImageTk.PhotoImage(image)
imageLbl = Label(root, image = imagePI)
imageLbl.image = imagePI

imageLbl.pack()
