# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 09:04:52 2018

@author: Admin
"""


import numpy as np
from mss.windows import MSS as mss
import cv2
import time

from directkeys import PressKey, ReleaseKey, W, A, S, D, Q, E, SPACE_BAR
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
    
def left():
    ReleaseKey(D)
    PressKey(W)
    PressKey(A)
    
def right():
    ReleaseKey(A)
    PressKey(W)
    PressKey(D)

def straight():
    ReleaseKey(D)
    ReleaseKey(A)
    PressKey(W)
    
def ohe_buttons(key):
    #forward, left, right, boost, jump
    #W, A, D, E, SPACE_BAR
    buttons = np.zeros(5)
    if not key:
        return buttons
    
    b_list = ['W', 'A', 'D', 'E', ' ']
    
    for i, b in enumerate(b_list):
        buttons[i] = int(b in key)
        
    return buttons
    


def main():
    
    #Give myself time to switch windows
    for _ in range(4):
        time.sleep(1)
    
    
    last_time = time.time()
    
    move = straight
    with mss() as sct:
        
        while True:
            bbox = (0,40,800,640)
            screen =  np.array(sct.grab(bbox))
            #print('Frame took {} seconds'.format(time.time()-last_time))
            key = key_check()
            print(ohe_buttons(key))
            last_time = time.time()
            new_screen = process_img(screen)
            cv2.imshow('window', new_screen)
            
            
            if random.random() < .01:
                PressKey(SPACE_BAR)
            else:
                ReleaseKey(SPACE_BAR)
            
            if random.random() < .05:
                random_number = random.random()
                threshold = .1
                if random_number < threshold:
                    move = left
                elif random_number < 1- threshold:
                    move = straight
                else:
                    move = right
            
            move()

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        
main()