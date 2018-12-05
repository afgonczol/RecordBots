# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 09:04:52 2018

@author: Admin
"""


import numpy as np
from mss.windows import MSS as mss
import cv2
import time
import keras

from directkeys import PressKey, ReleaseKey, W, A, S, D, Q, E, SPACE_BAR, L, P
from getkeys import key_check

import random

def screen_record(): 
    last_time = time.time()
    while(True):
        # 800x600 windowed mode
        printscreen =  np.array(ImageGrab.grab(bbox=(0,40,800,640)))
        print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        
def _process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # edge detection
    #processed_img =  cv2.Canny(processed_img, threshold1 = 200, threshold2=300)
    #processed_img = cv2.Laplacian(processed_img,cv2.CV_64F, 10, 9)
    
    return processed_img

def process_img(image):
    original_image = image
    # convert to gray
    processed_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contrast = 1
    brightness = 0
    out = cv2.addWeighted(processed_img, contrast, processed_img, 0, brightness)
    return out
    
def _left():
    ReleaseKey(D)
    PressKey(W)
    PressKey(A)
    
def _right():
    ReleaseKey(A)
    PressKey(W)
    PressKey(D)

def _straight():
    ReleaseKey(D)
    ReleaseKey(A)
    PressKey(W)
    
def ohe_buttons(key):
    #forward, left, right, boost, jump
    #W, A, D, L, SPACE_BAR
    buttons = np.zeros(5)
    if not key:
        return buttons
    
    b_list = ['W', 'A', 'D', 'L', ' ']
    
    for i, b in enumerate(b_list):
        buttons[i] = int(b in key)
        
    return buttons.astype('int')

def press_buttons(buttons):
 #Convert from OHE to pressing/releasing keys
     keys = [W, A, D, L, SPACE_BAR]
     
     for b, k in zip(buttons, keys):
         if b:
             PressKey(k)
         else:
             ReleaseKey(k)

         


def main():
    
    #Give myself time to switch windows
    #Screen should be in top left
    for _ in range(4):
        time.sleep(1)
    
    
    #last_time = time.time()
    model = keras.models.load_model('model10e14trainb.model')

    training_data = []
    training_files = 0
    with mss() as sct:
        
        while True:
            bbox = (150,240,650,490)
            screen =  np.array(sct.grab(bbox))
            #print('Frame took {} seconds'.format(time.time()-last_time))
            #key = key_check()
            #buttons = ohe_buttons(key)
            #print(ohe_buttons(key))
            #last_time = time.time()
            new_screen = process_img(screen)
            cv2.imshow('window', new_screen)
            new_screen = cv2.resize(new_screen, (100,50))
            #print(np.array(new_screen).shape)
            
            buttons = model.predict(np.array(new_screen).reshape(1,50,100,1)/255)
            buttons = np.around(buttons)[0]
            #print(buttons)
            press_buttons(buttons)
                
            
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        
main()