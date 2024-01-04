import random
import pygame
import cv2 as cv
from Param import *
from collections import deque

dir = [(-1 , 0) , (1 , 0) , (0 , -1) , (0 , 1)]

def ShortestPath(PlayPosition):
    Dist = np.zeros((ROW_NUMBER , COL_NUMBER) , dtype=np.uint8)
    Dist[PlayPosition[0] , PlayPosition[1]] = 1
    Queue = deque([(PlayPosition[0] , PlayPosition[1])])
    while Queue:
        x , y = Queue.popleft()
        for dx,dy in dir:
            a , b = x + dx , y + dy
            if 0 <= a < ROW_NUMBER and 0 <= b < COL_NUMBER and Map[a , b] != 0 and Dist[a , b] == 0:
                Dist[a , b] = Dist[x , y] + 1
                Queue.append((a , b))
    return Dist

class Ghost(object):
    def __init__(self):
        self.Position = [-1 , -1]
        self.Speed = 1
        self.Option = 1
    def Move(self , i):
        a = self.Position[0] + dir[i][0] * self.Speed
        b = self.Position[1] + dir[i][1] * self.Speed
        check = 0
        fix_dir = 0 # 碰撞修正
        crash_dir = [(1 , 1) , (-1 , -1) , (-1 , 1) , (1 , -1)]
        for j in range(4):
            c = a + crash_dir[j][0] * (SCALE // 2 - 1)
            d = b + crash_dir[j][1] * (SCALE // 2 - 1)
            if not (c >= 0 and c < ROW_NUMBER * SCALE and d >= 0 and d < COL_NUMBER * SCALE and Map[int(c / SCALE) , int(d / SCALE)] != 0):
                check += 1
                fix_dir = j ^ 1

        if check == 0:
            self.Position = [a , b]
        # elif check == 1:
        #     self.Position[0] += crash_dir[fix_dir][0] * self.Speed
        #     self.Position[1] += crash_dir[fix_dir][1] * self.Speed

class Player(Ghost):
    def __init__(self):
        super(Player , self).__init__()
        self.ImgPath = [r"D:\download\PMGame\picture\cdr_white32_left.png",
                        r"D:\download\PMGame\picture\cdr_white32_right.png"]
        self.Direction = 3
        self.image = pygame.image.load(self.ImgPath[self.Direction - 2])
        self.Speed = 2
    def Run(self , i):
        self.Move(i)
        if i != self.Direction:
            self.Direction = i
            if self.Direction > 1:
                self.image = pygame.image.load(self.ImgPath[self.Direction - 2])

class Ghost_Red(Ghost):
    def __init__(self):
        super(Ghost_Red , self).__init__()
        self.ImgPath = [r"D:\download\PMGame\picture\Ghost_Red_White_32_left.png",
                        r"D:\download\PMGame\picture\Ghost_Red_White_32_Right.png",
                        r"D:\download\PMGame\picture\Ghost_Blue_White_32_left.png",
                        r"D:\download\PMGame\picture\Ghost_Blue_White_32_Right.png"]
        self.Direction = 3
        self.image  = pygame.image.load(self.ImgPath[self.Direction - 2])
        self.imageb = pygame.image.load(self.ImgPath[self.Direction])
    def Get_Direction(self , PlayPosition):
        Dist = ShortestPath(PlayPosition)
        for i in range(4):
            a , b = int(self.Position[0] / SCALE) + dir[i][0] , int(self.Position[1] / SCALE) + dir[i][1]
            if 0 <= a < ROW_NUMBER and 0 <= b < COL_NUMBER and Dist[a][b] == Dist[int(self.Position[0] / SCALE) , int(self.Position[1] / SCALE)] + self.Option * 2 - 3:
                return i
        return -1
        
    def Raider(self , PlayPosition):
        mydir = self.Get_Direction([int(PlayPosition[0] / SCALE) , int(PlayPosition[1] / SCALE)])
        if mydir != self.Direction:
            self.Direction = mydir
            if self.Direction > 1:
                self.image  = pygame.image.load(self.ImgPath[self.Direction - 2])
                self.imageb = pygame.image.load(self.ImgPath[self.Direction])
        self.Move(mydir)

class Ghost_Pink(Ghost):
    def __init__(self):
        super(Ghost_Pink , self).__init__()
        self.Limit = 7
        self.ImgPath = [r"D:\download\PMGame\picture\Ghost_Pink_White_32_left.png",
                        r"D:\download\PMGame\picture\Ghost_Pink_White_32_Right.png",
                        r"D:\download\PMGame\picture\Ghost_Blue_White_32_left.png",
                        r"D:\download\PMGame\picture\Ghost_Blue_White_32_Right.png"]
        self.Direction = 3
        self.image  = pygame.image.load(self.ImgPath[self.Direction - 2])
        self.imageb = pygame.image.load(self.ImgPath[self.Direction])

    def Get_Direction(self , PlayPosition):
        if abs(int(self.Position[0] / SCALE) - PlayPosition[0]) + abs(int(self.Position[1] / SCALE) - PlayPosition[1]) > self.Limit:
            Dist = ShortestPath(PlayPosition)
            for i in range(4):
                a , b = int(self.Position[0] / SCALE) + dir[i][0] , int(self.Position[1] / SCALE) + dir[i][1]
                if 0 <= a < ROW_NUMBER and 0 <= b < COL_NUMBER and Dist[a][b] == Dist[int(self.Position[0] / SCALE) , int(self.Position[1] / SCALE)] + self.Option * 2 - 3:
                    return i
        else:
            a , b = int(self.Position[0] / SCALE) + dir[self.Direction][0] , int(self.Position[1] / SCALE) + dir[self.Direction][1]
            if a < 0 or a >= ROW_NUMBER or b < 0 or b >= COL_NUMBER or Map[a,  b] == 0:
                random_dir = [0 , 1 , 2 , 3]
                random.shuffle(random_dir)
                for i in random_dir:
                    a , b = int(self.Position[0] / SCALE) + dir[i][0] , int(self.Position[1] / SCALE) + dir[i][1]
                    if 0 <= a < ROW_NUMBER and 0 <= b < COL_NUMBER and Map[a , b] != 0:
                        return i
            else:
                return self.Direction
        return -1

    def Raider(self , PlayPosition):
        mydir = self.Get_Direction([int(PlayPosition[0] / SCALE) , int(PlayPosition[1] / SCALE)])
        if mydir != self.Direction:
            self.Direction = mydir
            if self.Direction > 1:
                self.image  = pygame.image.load(self.ImgPath[self.Direction - 2])
                self.imageb = pygame.image.load(self.ImgPath[self.Direction])
        self.Move(mydir)
