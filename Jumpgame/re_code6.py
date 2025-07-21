import pygame, sys
from pygame.locals import * # pygame에 있는 모든기능을 사용
import re_store
from re_helper import load_image, load_sound, load_image_menu

# 발판 나타내기

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

    # 플레이어 왼쪽 모습 생성
    player_img_left = load_image('cat_left.png')
    player_img_left = pygame.transform.scale(player_img_left, (105, 120))

    # 플레이어 오른쪽 모습 생성
    player_img_right = load_image('cat_right.png')
    player_img_right = pygame.transform.scale(player_img_right, (105, 120))

    # 플레이어 2단 점프 모습 생성
    player_img_jump = load_image('cat_jump.png')
    player_img_jump = pygame.transform.scale(player_img_jump, (105, 120))

    # 발판 생성
    foothold = pygame.Rect((re_store.screen_width + 105) / 2, (re_store.screen_height) / 2, 345, 81)
    foothold_img = load_image('foothold.png')
    foothold_img = pygame.transform.scale(foothold_img, (345, 81))  # 가로, 세로

    # 전반적인 게임 속도
    clock = pygame.time.Clock()

    # 중력 표현
    y_vel = 0

    # 속도
    speed = 0.5

    # 2단 점프 구현
    jump_count = 2  # 최대 2단점프
    is_jumping = False # 점프 상태 플래그
    jump_timer = 0 # 2단 점프시 이미지 타이머

    # 방향에 따른 이미지 표현
    va = 0

    # 2단 점프 소리 구현
    dbjump_sound = load_sound('one.mp3')
    dbjump_sound.set_volume(0.5) # 0.0 ~ 1.0

    # 게임 실행 관련 코드
    while True:
        dt = clock.tick(60)  # 1초에 60번(hz) 업데이트

        # 우측상단 x 표시 누르면 시스템 종료하기
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(bgImag1, (0, 0))
        screen.blit(foothold_img, foothold)

        # 키보드로 플레이어 조종
        key = pygame.key.get_pressed()

        # 플레이어 좌우로 움직이기
        if key[K_LEFT] and player.left >= 0:
            player.left = player.left - speed * dt
            va = 1  # 왼쪽 상태값
        elif key[K_RIGHT] and player.right <= re_store.screen_width:
            player.right = player.right + speed * dt
            va = 2  # 오른쪽 상태값
        else:
            va = 0  # 기본값

        # 점프 구현
        player.top = player.top + y_vel
        y_vel += 1

        if player.bottom >= re_store.screen_height * 0.85:
            player.bottom = re_store.screen_height * 0.85
            y_vel = 0
            jump_count = 2

        # 발판 바닥 위로 못뛰게
        # y_vel > 0 는 plyer가 떨어지는것을 의미 (중력적용)
        elif player.colliderect(foothold) and y_vel > 0:
            player.bottom = foothold.top
            y_vel = 0
            jump_count = 2
            jump_timer = 0

        # 발판 위로 착지
        # y_vel < 0 은 player가 점프하는것을 의미 (중력무시)
        # 점프시 y_vel이 음수가 되기 때문
        elif player.colliderect(foothold) and y_vel < 0:
            player.top = foothold.bottom
            y_vel = 0

        if key[K_SPACE] and jump_count > 0 and not is_jumping:
            if jump_count == 2:
                y_vel = -18  # 첫 점프
            elif jump_count == 1:
                dbjump_sound.play()  # 2단 점프시 사운드
                y_vel = -20  # 두 번째 점프
                jump_timer = 50  # 2단 점프 이미지 길게 (대략 0.8초)

            jump_count -= 1  # 점프 횟수 감소
            is_jumping = True  # 점프 상태 시작

        # 점프 키에서 손을 떼면 is_jumping 초기화
        if not key[K_SPACE]:
            is_jumping = False

        # 2단 점프시 타이머 작동 및 이미지 구현
        if jump_timer > 0:
            va = 3
            jump_timer -= 1

        # va 별 이미지 구현
        if va == 1:
            screen.blit(player_img_left, player)
        elif va == 2:
            screen.blit(player_img_right, player)
        elif va == 3:
            screen.blit(player_img_jump, player)
        else:
            screen.blit(player_img, player)

        # 플레이어의 행동에대해 결과를 화면에 업데이트 하기위해 선언
        pygame.display.update()

main()