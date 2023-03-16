import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cut_rectangle import *
from logo import *

form_class = uic.loadUiType('source code\main.ui')[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):              
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Photoshop')
        self.setWindowIcon(QIcon('img\icon\smile.png'))
        self.initUi()
        self.show()

    def initUi(self):
        self.actionNEW.setIcon(QIcon('img\icon\plus.png'))
        self.actionEXIT.setIcon(QIcon('img\icon\exit.png'))
        self.actionRECTANGLE.setIcon(QIcon('img\icon\erec.png'))
        self.actionNEW.triggered.connect(self.open_file)
        self.actionEXIT.triggered.connect(QCoreApplication.instance().quit)  
        self.actionRECTANGLE.triggered.connect(self.cutImg)
        self.btn_contour.clicked.connect(self.contour)
        self.btn_gray.clicked.connect(self.grayImg)
        self.btn_original.clicked.connect(self.grayImg)
        self.btn_Blur.clicked.connect(self.editImg)
        self.btn_Sharp.clicked.connect(self.editImg)
        self.BlurSlider.valueChanged.connect(self.editImg)
        self.SharpSlider.valueChanged.connect(self.editImg)
        self.btn_Bright.clicked.connect(self.brightImg)
        self.BCSlider.valueChanged.connect(self.brightImg)
        self.btn_Rotate.clicked.connect(self.rotateImg)
        self.btn_up.clicked.connect(self.flipImg)
        self.btn_left.clicked.connect(self.flipImg2)
        self.btn_ori.clicked.connect(self.oriImg)
        self.btn_logo.clicked.connect(self.logoImg)
        self.btn_save.clicked.connect(self.save_file)
        
    def open_file(self):
        new_img = QFileDialog.getOpenFileName       
        self.file, _ = new_img(self, 'Open', './img')
        self.showImg()                                 
        self.loadImage()                                
    def save_file(self):
        save_img = cv2.cvtColor(self.rightimg, cv2.COLOR_BGR2RGB)       
        self.savefile, _ = QFileDialog.getSaveFileName(self, 'save', './img', '파일(*.jpg;*.jpeg;*.png;*)')    
        cv2.imwrite(self.savefile, save_img)                       
        
    def loadImage(self):                                        
        loadimg = cv2.imread(self.file)                        
        editimg = loadimg.copy()                                
        self.orgImg = cv2.cvtColor(editimg, cv2.COLOR_BGR2RGB) 

        self.rightimg = self.orgImg.copy()                     
        new_img = self.rightimg                                 
        self.result = QImage(new_img.data, new_img.shape[1], new_img.shape[0], QImage.Format_RGB888)   
        self.pixmappre = QPixmap.fromImage(self.result)                                                 
        self.edit_img.setPixmap(self.pixmappre.scaled(self.width(), self.height(), Qt.KeepAspectRatio)) 

    def showImg(self):                                                              
        self.pixmap = QPixmap(self.file)                            
        self.ori_img.setPixmap(self.pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)) 

    def updateImg(self):                                        
        new_img = self.rightimg
        self.result = QImage(new_img.data, new_img.shape[1], new_img.shape[0], QImage.Format_RGB888)       
        self.pixmappre = QPixmap.fromImage(self.result)                                                     
        self.edit_img.setPixmap(self.pixmappre.scaled(self.width(), self.height(), Qt.KeepAspectRatio))     
    
    def editImg(self):                                            
        try:                        
            if self.btn_Blur.isChecked() == True:                   
                self.rightimg = self.rightimg.copy()               
                blur_img = self.rightimg                            
                i = self.BlurSlider.value()                         
                blur = cv2.blur(blur_img, (i, i))                  
                self.rightimg = blur                               
                self.updateImg()                                    
            if self.btn_Sharp.isChecked() == True:                  
                self.rightimg = self.orgImg.copy()                  
                shar_img = self.rightimg                           
                j = self.SharpSlider.value()                       
                sharpenImg = np.array([[-1, -1, -1], [-1, j, -1], [-1, -1, -1]])      
                shar = cv2.filter2D(shar_img, -1, sharpenImg)                           
                self.rightimg = shar                                                   
                self.updateImg()                                                         
        except:                                                     
            print("-")

    def brightImg(self):                                            
        try:
            if self.btn_Bright.isChecked() == True:                
                self.rightimg = self.orgImg.copy()                  
                self.rightimg = self.rightimg.copy()
                loadimg = self.rightimg
                k = self.BCSlider.value()                           
                array = np.full(loadimg.shape,(k,k,k), dtype= np.uint8)     
                loadimg = cv2.add(loadimg,array)                           
                self.rightimg = loadimg                                     
                self.updateImg()                                            
            if self.btn_Bright.isChecked() == False:
                self.updateImg()
        except:
            print("=")
    def grayImg(self):                                                  
        try:
            if self.btn_gray.isChecked() == True:                     
                loadimg = self.rightimg
                gray = cv2.cvtColor(loadimg, cv2.COLOR_BGR2GRAY)            
                editimg = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)            
                self.rightimg = editimg
                self.updateImg()                                            
            if self.btn_original.isChecked() == True:                 
                self.oriImg(self)                                       
        except:
            print("=")
    def contour(self):
        cont_img = cv2.cvtColor(self.rightimg,cv2.COLOR_BGR2GRAY)           
        cont_img = cv2.resize(cont_img,(421,481))                           
        edge = cv2.Canny(cont_img, 150,200)                                 
        cv2.imshow('img',edge)

    def rotateImg(self):                                                
        rot_img = self.rightimg                                             
        rot_img = cv2.rotate(rot_img, cv2.ROTATE_90_CLOCKWISE)          
        self.rightimg = rot_img
        self.updateImg()                                                
    def flipImg(self):                                                  
        flip_img = self.rightimg                                       
        flip_img = cv2.flip(flip_img, 0)
        self.rightimg = flip_img                                        
        self.updateImg()
    def flipImg2(self):                                                 
        flip_img = self.rightimg                                        
        flip_img = cv2.flip(flip_img, 1)                               
        self.rightimg = flip_img
        self.updateImg()
    def oriImg(self):                                                  
        self.rightimg = self.orgImg.copy()                           
        self.updateImg()   
    def cutImg(self):                                                 
        rectangle(self)                                                 
        
    def logoImg(self):                                               
        addlogo(self)                                       
   
if __name__ == "__main__":                                            
    import sys
    app = QApplication([])                                             
    ex = MainWindow()
    sys.exit(app.exec_())                                              


