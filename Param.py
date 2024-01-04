import pygame
import numpy as np
SCALE = 32
ROW_NUMBER = 10
COL_NUMBER = 10
Color_Red      = (255,0,0)
Color_Green    = (0,255,0)
Color_White    = (255,255,255)
Color_Black    = (0 , 0 , 0)
Color_Black_2  = (45,45,45)
Color_Pink     = (255,192,203)
Color_Yellow   = (238,238,68)
Color_Green    = (50,160,50)
Color_Gray     = (200,200,200)
Color_Blue     = (128,128,255)  
dir = [(0 , 1) , (0 , -1) , (1 , 0) , (-1 , 0)]
udlr = [pygame.K_UP , pygame.K_DOWN , pygame.K_LEFT , pygame.K_RIGHT]
Map = np.zeros((ROW_NUMBER , COL_NUMBER) , dtype=np.uint8)
image_apple = pygame.image.load(r"picture\apple.png")
# Map_Show = np.zeros((ROW_NUMBER * SCALE , COL_NUMBER * SCALE , 3) , dtype=np.uint8)
        