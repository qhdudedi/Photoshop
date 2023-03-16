import cv2
import numpy as np
from PyQt5.QtCore import *
from Window_Main import *
def addlogo(self):
    logoImg = cv2.imread('img/icon/smile.png', cv2.IMREAD_UNCHANGED) 
    img = cv2.cvtColor(self.rightimg, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, dsize=(401, 391))
    
   
    ret, mask = cv2.threshold(logoImg[:,:,3], 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
   
    logoImg = cv2.cvtColor(logoImg, cv2.COLOR_BGRA2BGR) # BGRA : BGR + ALPHA(투명도)
    h, w = logoImg.shape[:2] #잘라내기
    roi = img[10:10+h, 10:10+w ] 
    
   
    logoImg_fg = cv2.bitwise_and(logoImg, logoImg, mask=mask)
    img_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    
    dst = cv2.bitwise_or(logoImg_fg ,img_bg)

    img[10:10+h, 10:10+w] = dst       
    cv2.imshow('dst',img)
    save_img = img
    self.savefile, _ = QFileDialog.getSaveFileName(self, 'save', './img', '파일(*.jpg;*.jpeg;*.png;*)')
    cv2.imwrite(self.savefile, save_img)  
    cv2.destroyWindow('dst')             
    cv2.waitKey(0)

    

