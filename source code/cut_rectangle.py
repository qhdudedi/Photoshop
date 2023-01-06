import cv2
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
click = False
st_x, st_y,w,h = 0,0,0,0 
from Window_Main import *
def rectangle(self):
    click = False   # 마우스 클릭된 상태 (false = 클릭x)
    st_x, st_y,w,h = 0,0,0,0    # 마우스 시작된 좌표 초기화 및 최초로 마우스 왼쪽 버튼 누른 위치를 저장하기 위해 사용
    img = cv2.cvtColor(self.rightimg, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img,(421,481))
    def drag_r(event, x, y, flags, param):              #drag_gray() 함수 선언
        global click, st_x, st_y                           # 전역변수 click,st_x,st_y 선언
        result_img = img.copy()                            # 결과 이미지에 원본 이미지 copy
        if event == cv2.EVENT_LBUTTONDOWN:                 # 마우스 좌클릭이 눌렸을 경우
            click = True
            st_x, st_y = x, y                              # x,y에 st_x,st_y 값 넣기

        elif event == cv2.EVENT_MOUSEMOVE:                 # 좌클릭된 마우스가 움직이고 있을 때
            if click == True:
                cv2.rectangle(result_img, (st_x, st_y), (x, y), (0, 0, 0), 2)           #rectangle()함수로 gray처리될 이미지에 처리될 부분 사각형으로 표시
                cv2.imshow('IMAGE', result_img)                                         # 사각형으로 표시된 이미지 출력

        elif event == cv2.EVENT_LBUTTONUP:                 # 좌클릭된 마우스가 떼어졌을 경우
            click = False
            cv2.destroyWindow('IMAGE')                      # 원하는 윈도우 창 닫기
            h = y - st_y                                    # 처리될 영역 사각형의 높이 구하기
            w = x - st_x                                    # 처리될 영역 사각형의 너비 구하기
            roi = img[st_y:st_y+h, st_x:st_x+w]             
            result_img[st_y:st_y+h, st_x:st_x+w] = roi

            # cv2.imshow('RESULT_IMG', result_img)
            
            cv2.imshow('SELECT_IMG', roi)
            key = cv2.waitKey()
            if key == ord('s'):                             # 's' 키 입력 시 사진이 img폴더에 저장되는 조건문
                save_img = roi
                self.savefile, _ = QFileDialog.getSaveFileName(self, 'save', './img', '파일(*.jpg;*.jpeg;*.png;*)')
                cv2.imwrite(self.savefile, save_img)  #imwrite()함수로 추출한 이미지를 폴더에 저장
                cv2.destroyWindow('SELECT_IMG')             # 사진이 저장되는 동시에 윈도우 창 제거
    
    cv2.imshow('IMAGE', img)
    cv2.setMouseCallback('IMAGE', drag_r)                #setMouseCallback()함수로 선언한 함수 불러오기
    cv2.waitKey(0)
cv2.destroyAllWindows()

