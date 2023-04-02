# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 07:56:17 2023

@author: franc
"""
with open("results\\log.txt", "r+") as f:
    data = f.read()
    f.seek(0)
    f.write(str(int(data)+1))
    