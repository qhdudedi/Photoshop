import cv2
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
click = False
st_x, st_y,w,h = 0,0,0,0 
from Window_Main import *
def rectangle(self):
    click = False   
    st_x, st_y,w,h = 0,0,0,0    
    img = cv2.cvtColor(self.rightimg, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img,(421,481))
    def drag_r(event, x, y, flags, param):              
        global click, st_x, st_y                          
        result_img = img.copy()                            
        if event == cv2.EVENT_LBUTTONDOWN:                 
            click = True
            st_x, st_y = x, y                              

        elif event == cv2.EVENT_MOUSEMOVE:               
            if click == True:
                cv2.rectangle(result_img, (st_x, st_y), (x, y), (0, 0, 0), 2)           
                cv2.imshow('IMAGE', result_img)                                         

        elif event == cv2.EVENT_LBUTTONUP:                 
            click = False
            cv2.destroyWindow('IMAGE')                      
            h = y - st_y                                   
            w = x - st_x                                    
            roi = img[st_y:st_y+h, st_x:st_x+w]             
            result_img[st_y:st_y+h, st_x:st_x+w] = roi

            # cv2.imshow('RESULT_IMG', result_img)
            
            cv2.imshow('SELECT_IMG', roi)
            key = cv2.waitKey()
            if key == ord('s'):                             
                save_img = roi
                self.savefile, _ = QFileDialog.getSaveFileName(self, 'save', './img', '파일(*.jpg;*.jpeg;*.png;*)')
                cv2.imwrite(self.savefile, save_img)  
                cv2.destroyWindow('SELECT_IMG')            
    
    cv2.imshow('IMAGE', img)
    cv2.setMouseCallback('IMAGE', drag_r)               
    cv2.waitKey(0)
cv2.destroyAllWindows()

