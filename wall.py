import random
import pygame
import cv2 as cv
import numpy as np

STEP = 2

def Map_Maker(x , y):
    Vis[x][y] = True
    dir = [(0 , 1) , (0 , -1) , (1 , 0) , (-1 , 0)]
    random.shuffle(dir)
    for dx,dy in dir:
        flag = True
        # for i in range(1 , STEP + 1):
        a = x + dx * STEP
        b = y + dy * STEP
        if a < 0 or a >= COL_NUMBER or b < 0 or b >= ROW_NUMBER or Vis[a][b]:
            flag = False
        if flag:
            for i in range(1 , STEP + 1):
                a = x + dx * i
                b = y + dy * i
                Map[a][b] = (255,255,255)
            Map_Maker(x + STEP * dx , y + STEP * dy)

SCALE = 16
ROW_NUMBER = 30
COL_NUMBER = 30
START_X = random.randint(1 , ROW_NUMBER)
START_Y = random.randint(1 , COL_NUMBER)
Map = np.zeros((ROW_NUMBER , COL_NUMBER , 3) , dtype=np.uint8)
Vis = np.zeros((ROW_NUMBER , COL_NUMBER) , dtype=bool)
Map_Show = np.zeros((ROW_NUMBER * SCALE , COL_NUMBER * SCALE , 3) , dtype=np.uint8)
Map[START_X , START_Y] = (255,255,255)
Vis[START_X , START_Y] = True
Map_Maker(START_X , START_Y)
for i in range(ROW_NUMBER * SCALE):
    for j in range(COL_NUMBER * SCALE):
        Map_Show[i][j] = Map[i // SCALE][j // SCALE]


RUNNING = True
clock = pygame.time.Clock()

Position_Ghost = [-1 , -1]
Position_Player = [START_X * SCALE + SCALE // 2 , START_Y * SCALE + SCALE // 2]
Speed_Ghost = 1
Speed_Player = 1

for i in range(ROW_NUMBER):
    for j in range(COL_NUMBER):
        if all(Map[i , j] == (255,255,255)):
            Position_Ghost = [i * SCALE + SCALE // 2 , j * SCALE + SCALE // 2]
            break
    if Position_Ghost[0] != -1:
        break
screen = pygame.display.set_mode((ROW_NUMBER * SCALE, COL_NUMBER * SCALE))
while RUNNING:
    screen.fill((0 , 0 , 0))

    for i in range(ROW_NUMBER):
        for j in range(COL_NUMBER):
            if all(Map[i][j] == (255,255,255)):
                pygame.draw.rect(screen , (255,255,255) , (j * SCALE , i * SCALE , SCALE , SCALE))
    pygame.draw.circle(screen , (0 , 255 , 0) , (Position_Ghost[1] , Position_Ghost[0]) , SCALE // 2)
    pygame.draw.circle(screen , (255 , 0 , 0) , (Position_Player[1] , Position_Player[0]) , SCALE // 2)
    

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if Position_Player[1] and all(Map_Show[Position_Player[0] , Position_Player[1] - Speed_Player] == (255,255,255)):
            Position_Player[1] -= Speed_Player
    if keys[pygame.K_RIGHT]:
        if Position_Player[1] != COL_NUMBER - Speed_Player and all(Map_Show[Position_Player[0] , Position_Player[1] + Speed_Player] == (255,255,255)):
            Position_Player[1] += Speed_Player
    if keys[pygame.K_UP]:
        if Position_Player[0] and all(Map_Show[Position_Player[0] - Speed_Player , Position_Player[1]] == (255,255,255)):
            Position_Player[0] -= Speed_Player
    if keys[pygame.K_DOWN]:
        if Position_Player[0] != ROW_NUMBER - Speed_Player and all(Map_Show[Position_Player[0] + Speed_Player , Position_Player[1]] == (255,255,255)):
            Position_Player[0] += Speed_Player
    clock.tick(60)

    
# def Map_Maker(up , down , left , right , flag):
#     if up >= down - 3 or left >= right - 3:
#         return
#     # print(up , down , left , right , flag)
#     if flag:
#         t = random.randint(up , down - 1)
#         for i in range(left , right):
#             if random.randint(1 , 10) <= 5:
#                 Map[t][i] = (255,255,255)
#                 if i != left:
#                     Map[t][i-1] = (255,255,255)
#                 if i+1 != right:
#                     Map[t][i+1] = (255,255,255)
#             # Map[t][i] = (255,255,255) if random.randint(1 , 10) > 3 else (0 , 0 , 0)
#         Map_Maker(up , t , left , right , flag ^ 1)
#         Map_Maker(t + 1 , down , left , right , flag ^ 1)
#     else:
#         t = random.randint(left , right - 1)
#         for i in range(up , down):
#             if random.randint(1 , 10) <= 5:
#                 Map[i][t] = (255,255,255)
#                 if i != up:
#                     Map[i-1][t] = (255,255,255)
#                 if i+1 != down:
#                     Map[i+1][t] = (255,255,255)
#         Map_Maker(up , down , left , t , flag ^ 1)
#         Map_Maker(up , down , t + 1 , right , flag ^ 1)