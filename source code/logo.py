import cv2
import numpy as np
from PyQt5.QtCore import *
from Window_Main import *
def addlogo(self):
    #합성에 사용할 영상 읽기, 전경 영상은 4채널 png 파일
    logoImg = cv2.imread('img/icon/smile.png', cv2.IMREAD_UNCHANGED) #cv2.IMREAD_UNCHANGED : 입력 파일에 정의된 타입의 영상을 그대로 반환(알파(alpha) 채널 포함)
    img = cv2.cvtColor(self.rightimg, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, dsize=(401, 391))
    
    #알파 채널을 이용하여 mask, 역mask 생성 -> 교재 193p 참고 
    ret, mask = cv2.threshold(logoImg[:,:,3], 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)
    #--③ 전경 영상 크기로 배경 영상에서 ROI 잘라내기
    logoImg = cv2.cvtColor(logoImg, cv2.COLOR_BGRA2BGR) # BGRA : BGR + ALPHA(투명도)
    h, w = logoImg.shape[:2] #잘라내기
    roi = img[10:10+h, 10:10+w ] 
    
    #--④ 마스크 이용해서 오려내기
    logoImg_fg = cv2.bitwise_and(logoImg, logoImg, mask=mask)
    img_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

    #--⑥ 이미지 합성
    dst = cv2.bitwise_or(logoImg_fg ,img_bg)

    img[10:10+h, 10:10+w] = dst       
    cv2.imshow('dst',img)
    save_img = img
    self.savefile, _ = QFileDialog.getSaveFileName(self, 'save', './img', '파일(*.jpg;*.jpeg;*.png;*)')
    cv2.imwrite(self.savefile, save_img)  #imwrite()함수로 추출한 이미지를 폴더에 저장
    cv2.destroyWindow('dst')             # 사진이 저장되는 동시에 윈도우 창 제거

    cv2.waitKey(0)

    

