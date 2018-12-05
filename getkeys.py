# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 15:35:47 2018

@author: Admin
"""

# getkeys.py
# Citation: Box Of Hats (https://github.com/Box-Of-Hats )

import win32api as wapi
import time

keyList = ["\b"]
for char in "WASD QFELP":
    keyList.append(char)

def key_check():
    keys = []
    for key in keyList:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys