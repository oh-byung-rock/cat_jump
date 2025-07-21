import pygame, sys
from pygame.locals import * # pygame에 있는 모든기능을 사용
import re_store
from re_helper import load_image, load_sound, load_image_menu

# 게임을 실행파일로 변환하기

def main():
    # 게임 초기화 정보
    pygame.init()

    # 제목 생성
    pygame.display.set_caption('cat game')

    # screen 객체
    screen = pygame.display.set_mode((re_store.screen_width,re_store.screen_height))
    bgImag1 = load_image('background.jpg')
    bgImag1 = pygame.transform.scale(bgImag1, (re_store.screen_width, re_store.screen_height))

    # 플레이어 생성
    player = pygame.Rect( 10, 470, 105, 120 ) # (x좌표, y좌표, 가로,세로)
    player_img = load_image('cat.png') # 이미지 선택
    player_img = pygame.transform.scale(player_img, (105,120)) # 이미지 크기 조정

    # 전반적인 게임 속도
    clock = pygame.time.Clock()

    # 중력 표현
    y_vel = 0

    # 속도
    speed = 0.5

    # 게임 실행 관련 코드
    while True:
        dt = clock.tick(60) # 1초에 60번(hz) 업데이트

        # 우측상단 x 표시 누르면 시스템 종료하기
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        screen.blit(bgImag1, (0, 0))

        # 키보드로 플레이어 조종
        key = pygame.key.get_pressed()

        # 화면이탈방지를 위해 player.left >= 0 와 player.right <= re_store.screen_width
        if key[K_LEFT] and player.left >= 0 :
            player.left = player.left - speed * dt
        elif key[K_RIGHT] and player.right <= re_store.screen_width:
            player.right = player.right + speed * dt

        # 중력 추가
        player.top = player.top + y_vel
        y_vel += 1

        if player.bottom >= re_store.screen_height * 0.85:
            player.bottom = re_store.screen_height * 0.85
            y_vel = 0

        # 점프 기능
        if key[K_SPACE] :
            y_vel = -18

        # blit는 bit block transfer의 약자로 조정한 이미지를 화면에 나태내는 기능

        screen.blit(player_img, player)

        # 1초에 60번 화면 업데이트
        pygame.display.update()
main()

# pip install pyinstaller (설치)
# cd C:\Users\obh73\PycharmProjects\cat_jump\Jumpgame (해당 코드가 있는 파일이 있는 위치로 경로 설정)
# pyinstaller --onefile --noconsole --add-data "C:\Users\obh73\PycharmProjects\cat_jump\Jumpgame\pictures;pictures" re_code4.py

    # 만약 이미지폴더가 2개라면?
    # pyinstaller --onefile --noconsole --add-data "C:/Users/obh73/PycharmProjects/cat_jump/Jumpgame/pictures;pictures" --add-data "C:/Users/obh73/PycharmProjects/cat_jump/Jumpgame/menu;menu" re_code4.py