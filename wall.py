import random
import pygame
import cv2 as cv
import numpy as np
from Param import *

class Wall(object):
    def __init__(self):
        self.START_X = random.randint(0 , ROW_NUMBER - 1)
        self.START_Y = random.randint(0 , COL_NUMBER - 1)
        self.Vis = np.zeros((ROW_NUMBER , COL_NUMBER) , dtype=bool)
        self.STEP = 2

    def Map_Maker(self , x , y):
        self.Vis[x][y] = True
        dir = [(1 , 0) , (-1 , 0) , (0 , 1) , (0 , -1)]
        random.shuffle(dir)
        for dx,dy in dir:
            flag = True
            a = x + dx * self.STEP
            b = y + dy * self.STEP
            if a < 0 or a >= COL_NUMBER or b < 0 or b >= ROW_NUMBER or self.Vis[a][b]:
                flag = False
            if flag:
                for i in range(1 , self.STEP + 1):
                    a = x + dx * i
                    b = y + dy * i
                    Map[a][b] = 2
                self.Map_Maker(x + self.STEP * dx , y + self.STEP * dy)
    
    def Create_Wall(self):
        Map[self.START_X , self.START_Y] = 1
        self.Vis[self.START_X , self.START_Y] = True
        self.Map_Maker(self.START_X , self.START_Y)
        for i in range(ROW_NUMBER):
            for j in range(COL_NUMBER):
                if Map[i , j] == 0 and random.randint(1 , 10) <= 4:
                    Map[i , j] = 2
                    
