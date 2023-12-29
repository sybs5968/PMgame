import random
import cv2 as cv
import numpy as np
import pygame

def Map_Maker(x, y):
    visited[x][y] = True
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(directions)
    for dx, dy in directions:
        nx, ny = x + dx * 2, y + dy * 2
        if 0 <= nx < ROW_NUMBER and 0 <= ny < COL_NUMBER and not visited[nx][ny]:
            Map[x + dx][y + dy] = (255, 255, 255)
            Map[nx][ny] = (255, 255, 255)
            Map_Maker(nx, ny)

# 初始化 Pygame
pygame.init()

# 设置屏幕大小
SCALE = 10
ROW_NUMBER = 50
COL_NUMBER = 50
WIDTH, HEIGHT = COL_NUMBER * SCALE, ROW_NUMBER * SCALE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("迷宫游戏")

# 创建迷宫
Map = np.zeros((ROW_NUMBER * 2 + 1, COL_NUMBER * 2 + 1, 3), dtype=np.uint8)
visited = np.zeros((ROW_NUMBER, COL_NUMBER), dtype=bool)
start_x, start_y = random.randint(0, ROW_NUMBER - 1), random.randint(0, COL_NUMBER - 1)
Map_Maker(start_x * 2 + 1, start_y * 2 + 1)

# 将迷宫数据转换为屏幕绘制用的数据
Map_Show = np.zeros((ROW_NUMBER * SCALE, COL_NUMBER * SCALE, 3), dtype=np.uint8)
for i in range(ROW_NUMBER * 2 + 1):
    for j in range(COL_NUMBER * 2 + 1):
        Map_Show[i // 2 * SCALE:(i // 2 + 1) * SCALE, j // 2 * SCALE:(j // 2 + 1) * SCALE] = Map[i][j]

# 设置玩家和鬼的初始位置
player_pos = [1, 1]
ghost_pos = [ROW_NUMBER * SCALE - 1, COL_NUMBER * SCALE - 1]
player_speed = SCALE
ghost_speed = SCALE // 2

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))

    # 绘制迷宫
    for i in range(ROW_NUMBER * SCALE):
        for j in range(COL_NUMBER * SCALE):
            if all(Map_Show[i, j] == [255, 255, 255]):
                pygame.draw.rect(screen, (255, 255, 255), (j, i, 1, 1))

    # 绘制玩家和鬼
    pygame.draw.circle(screen, (0, 255, 0), (player_pos[1], player_pos[0]), SCALE // 2)
    pygame.draw.circle(screen, (255, 0, 0), (ghost_pos[1], ghost_pos[0]), SCALE // 2)

    # 更新屏幕
    pygame.display.flip()

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 控制玩家移动
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if all(Map_Show[player_pos[0], player_pos[1] - player_speed] == [255, 255, 255]):
            player_pos[1] -= player_speed
    if keys[pygame.K_RIGHT]:
        if all(Map_Show[player_pos[0], player_pos[1] + player_speed] == [255, 255, 255]):
            player_pos[1] += player_speed
    if keys[pygame.K_UP]:
        if all(Map_Show[player_pos[0] - player_speed, player_pos[1]] == [255, 255, 255]):
            player_pos[0] -= player_speed
    if keys[pygame.K_DOWN]:
        if all(Map_Show[player_pos[0] + player_speed, player_pos[1]] == [255, 255, 255]):
            player_pos[0] += player_speed

    # 控制鬼追逐玩家
    if player_pos[1] < ghost_pos[1]:
        if all(Map_Show[ghost_pos[0], ghost_pos[1] - ghost_speed] == [255, 255, 255]):
            ghost_pos[1] -= ghost_speed
    elif player_pos[1] > ghost_pos[1]:
        if all(Map_Show[ghost_pos[0], ghost_pos[1] + ghost_speed] == [255, 255, 255]):
            ghost_pos[1] += ghost_speed

    if player_pos[0] < ghost_pos[0]:
        if all(Map_Show[ghost_pos[0] - ghost_speed, ghost_pos[1]] == [255, 255, 255]):
            ghost_pos[0] -= ghost_speed
    elif player_pos[0] > ghost_pos[0]:
        if all(Map_Show[ghost_pos[0] + ghost_speed, ghost_pos[1]] == [255, 255, 255]):
            ghost_pos[0] += ghost_speed

    clock.tick(60)

pygame.quit()
