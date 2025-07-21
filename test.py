import random
import sys, os
import pygame
from pygame.locals import *

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

pygame.init()
clock = pygame.time.Clock()

# 화면 설정
screen_width = 500
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
score = 0

player_width = 50
player_height = 50
moveSpeed = 5

# 플레이어 초기 위치
h = screen_width // 2
v = screen_height - player_height
hl = player_width // 2
hr = screen_width - (player_width // 2)
hh = random.randrange(hl, hr)

# 이미지 불러오기 및 크기 조정
bgImag1 = pygame.image.load('Jumpgame/pictures/background.jpg')
# bgImag1 = pygame.image.load('menu/Road.png')
bgImag1 = pygame.transform.scale(bgImag1, (screen_width, screen_height))

player = pygame.image.load('Jumpgame/pictures/cat.png')
# player = pygame.image.load('menu/Player.png')
player = pygame.transform.scale(player, (player_width, player_height))
player_rect = player.get_rect()
player_rect.topleft = (h, v)

player2 = pygame.image.load('Jumpgame/pictures/cat.png')
# player2 = pygame.image.load('menu/Player.png')
player2 = pygame.transform.scale(player2, (player_width, player_height))
player2_rect = player2.get_rect()
player2_rect.topleft = (hh, 0)

# 게임 끝내기 기능
def GameOver():
    pygame.quit()
    sys.exit()

# 게임 루프
while True:
    pygame.display.set_caption("Crazy Driver - Score " + str(score))
    screen.blit(bgImag1, (0, 0))
    screen.blit(player2, player2_rect)
    screen.blit(player, player_rect)

    # 적을 아래쪽으로 움직이기
    player2_rect.move_ip(0, moveSpeed)

    # 화면 밖으로 나갔는지 확인하기
    if player2_rect.top > screen_height:
        hl = player_width // 2
        hr = screen_width - (player_width // 2)
        h = random.randrange(hl, hr)
        v = 0
        player2_rect.center = (h, v)
        moveSpeed += 2
        score += 1

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        player_rect.move_ip(-moveSpeed, 0)
        if player_rect.left < 0:
            player_rect.left = 0
    if keys[K_RIGHT]:
        player_rect.move_ip(moveSpeed, 0)
        if player_rect.right > screen_width:
            player_rect.right = screen_width

    # 충돌 확인하기
    if player_rect.colliderect(player2_rect):
        # 충돌! 게임 오버
        GameOver()

    pygame.display.update()
    clock.tick(60)

