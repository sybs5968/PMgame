import random
import cv2 as cv
import numpy as np
from Wall import *
from Ghost import *
from Param import *

def PintLetters(str , siz):
    global screen
    font = pygame.font.SysFont("Arial" , siz , bold=True)
    text_gameover = font.render(str , True , Color_Red)
    rect_gemeover = text_gameover.get_rect(center = (ROW_NUMBER * SCALE // 2 , COL_NUMBER * SCALE // 2))
    screen.blit(text_gameover , rect_gemeover)
    pygame.display.update()
    pygame.time.wait(3000)

pygame.init()
pygame.font.init()
clock   = pygame.time.Clock()
screen  = pygame.display.set_mode((ROW_NUMBER * SCALE, COL_NUMBER * SCALE))

GameMap = Wall()
GameMap.Create_Wall()

Player = Player()
Ghost_Red = Ghost_Red()
Ghost_Pink = Ghost_Pink()

Player.Speed = 2
Ghost_Red.Speed = 0.5
Ghost_Pink.Speed = 0.5

Player.Position = [GameMap.START_X * SCALE + SCALE // 2 , GameMap.START_Y * SCALE + SCALE // 2]
for i in range(ROW_NUMBER):
    for j in range(COL_NUMBER):
        if Map[i , j] != 0:
            Ghost_Red.Position = [i * SCALE + SCALE // 2 , j * SCALE + SCALE // 2]
            break
    if Ghost_Red.Position[0] != -1:
        break

for i in range(ROW_NUMBER - 1 , 0 , -1):
    for j in range(COL_NUMBER):
        if Map[i , j] != 0:
            Ghost_Pink.Position = [i * SCALE + SCALE // 2 , j * SCALE + SCALE // 2]
            break
    if Ghost_Pink.Position[0] != -1:
        break

RUNNING = True
Pause = True
Apple_Number = 0
Time_Counter1 = 0 # 果实刷新
Time_Counter2 = 0 # 大力丸药效
Time_Counter3 = 0 # 红鬼复活时间
Time_Counter4 = 0 # 粉鬼复活时间

while RUNNING:
    screen.fill(Color_White)
    # Time_Counter3 = -100
    if Time_Counter1 == 500:
        Time_Counter1 -= 500
        if Apple_Number <= 1:
            a,b = random.randint(0 , ROW_NUMBER-1) , random.randint(0 , COL_NUMBER-1)
            while True:
                if [a,b] == Player.Position or [a,b] == Ghost_Red.Position or [a,b] == Ghost_Pink.Position or Map[a,b] == 0:
                    a,b = random.randint(0 , ROW_NUMBER-1) , random.randint(0 , COL_NUMBER-1)
                    continue
                else:
                    break
            Map[a,b] = 3
            Apple_Number += 1

    if Time_Counter2 == -1:
        Ghost_Red.Option = 1
        Ghost_Pink.Option = 1

    if Time_Counter3 == -1:
        for i in range(ROW_NUMBER):
            for j in range(COL_NUMBER):
                if Map[i , j] != 0:
                    Ghost_Red.Position = [i * SCALE + SCALE // 2 , j * SCALE + SCALE // 2]
                    break
            if Ghost_Red.Position[0] != -1:
                break
    if Time_Counter4 == -1:
        for i in range(ROW_NUMBER - 1 , 0 , -1):
            for j in range(COL_NUMBER):
                if Map[i , j] != 0:
                    Ghost_Pink.Position = [i * SCALE + SCALE // 2 , j * SCALE + SCALE // 2]
                    break
            if Ghost_Pink.Position[0] != -1:
                break    

    remain = False
    for i in range(ROW_NUMBER):
        for j in range(COL_NUMBER):
            if Map[i][j] == 0:
                pygame.draw.rect(screen , Color_Black    , (j * SCALE , i * SCALE , SCALE , SCALE) , 1)
                pygame.draw.rect(screen , Color_Black_2  , (j * SCALE + 1 , i * SCALE + 1 , SCALE - 1 , SCALE - 1))
            elif Map[i][j] == 1:
                pygame.draw.rect(screen , Color_Gray     , (j * SCALE , i * SCALE , SCALE , SCALE) , 1)
            elif Map[i][j] == 2:
                remain = True
                pygame.draw.rect(screen , Color_Gray     , (j * SCALE , i * SCALE , SCALE , SCALE) , 1)
                pygame.draw.circle(screen , Color_Blue , (j * SCALE + SCALE // 2 , i * SCALE + SCALE // 2) , SCALE // 4)
            elif Map[i][j] == 3:
                pygame.draw.rect(screen , Color_Gray     , (j * SCALE , i * SCALE , SCALE , SCALE) , 1)
                screen.blit(image_apple , (j * SCALE , i * SCALE))

    screen.blit(Player.image     , (Player.Position[1]     - SCALE // 2 , Player.Position[0]     - SCALE // 2))
    if Time_Counter3 >= 0:
        if Ghost_Red.Option == 1:
            screen.blit(Ghost_Red.image   , (Ghost_Red.Position[1]  - SCALE // 2 , Ghost_Red.Position[0]  - SCALE // 2))
        else:
            screen.blit(Ghost_Red.imageb  , (Ghost_Red.Position[1]  - SCALE // 2 , Ghost_Red.Position[0]  - SCALE // 2))
    if Time_Counter4 >= 0:
        if Ghost_Pink.Option == 1:
            screen.blit(Ghost_Pink.image  , (Ghost_Pink.Position[1] - SCALE // 2 , Ghost_Pink.Position[0] - SCALE // 2))
        else:
            screen.blit(Ghost_Pink.imageb , (Ghost_Pink.Position[1] - SCALE // 2 , Ghost_Pink.Position[0] - SCALE // 2))
    
    pygame.display.update()
    if remain == False:
        PintLetters("You Win!" , 72)
        RUNNING = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    keys = pygame.key.get_pressed()
    
    if any(keys):
        Pause = False
    
    if Pause:
        continue
    
    if keys[pygame.K_p]:
        Pause = True

    for i in range(4):
        if keys[udlr[i]]:
            Player.Run(i)
            a,b = int(Player.Position[0] / SCALE) , int(Player.Position[1] / SCALE)
            if Map[a,b] == 3:
                Ghost_Red.Option = 2
                Ghost_Pink.Option = 2
                Time_Counter2 = -301
                Apple_Number -= 1
            Map[a,b] = 1
    
    Ghost_Red.Raider(Player.Position)
    Ghost_Pink.Raider(Player.Position)
    
    if abs(Ghost_Red.Position[0] - Player.Position[0]) < SCALE and abs(Ghost_Red.Position[1] - Player.Position[1]) < SCALE and Time_Counter3 >= 0:
        if Ghost_Red.Option == 1:
            PintLetters("Game Over!" , 36)
            RUNNING = False
        else:
            Ghost_Red.Position = [-1,-1]
            Time_Counter3 = -500
    
    if abs(Ghost_Pink.Position[0] - Player.Position[0]) < SCALE and abs(Ghost_Pink.Position[1] - Player.Position[1]) < SCALE and Time_Counter4 >= 0:
        if Ghost_Pink.Option == 1:
            PintLetters("Game Over!" , 36)
            RUNNING = False
        else:
            Ghost_Pink.Position = [-1,-1]
            Time_Counter4 = -500
    
    clock.tick(60)
    Time_Counter1 += 1
    Time_Counter2 += 1
    Time_Counter3 += 1
    Time_Counter4 += 1
