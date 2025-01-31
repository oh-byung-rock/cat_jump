import pygame, sys
from pygame.locals import * # pygame에 있는 모든기능을 사용

# 플레이어 좌우이동, 점프, 중력 추가

def main():
    # 게임 초기화 정보
    pygame.init()
    screen_width = 1800
    screen_height = 900

    # 제목 생성
    pygame.display.set_caption('cat game')

    # screen 객체
    screen = pygame.display.set_mode((screen_width,screen_height))
    bgImage = pygame.image.load('pictures/background.jpg')
    bgImage = pygame.transform.scale(bgImage, (screen_width, screen_height))

    # 플레이어 생성
    # 가로 105, 세로 120 객체를 생성, 이후 객체의 왼쪽상단점의 위치를 다음 좌표로 설정
    player = pygame.Rect( 10, 470, 105,120)
    player_img = pygame.image.load('pictures/cat.png') # 이미지 할당
    player_img = pygame.transform.scale(player_img, (105,120)) # 이미지 크기 조정

    # 게임 속도
    clock = pygame.time.Clock()

    # 중력 표현(추가)
    y_vel = 0

    # 속도(추가)
    speed = 0.5

    # 게임 실행에대해 처리되는 코드
    while True:
        dt = clock.tick(60) # 1초에 60번(hz) 업데이트
        # 기능구현 1단계 : x 표시 누르면 시스템 종료하기
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # 키보드로 플레이어 조종 (추가)
        key = pygame.key.get_pressed()
        # 화면이탈방지를 위해 player.left >= 0 와 player.left <= screen_width
        if key[K_LEFT] and player.left >= 0 :
            player.left = player.left - speed * dt
        elif key[K_RIGHT] and player.right <= screen_width:
            player.right = player.right + speed * dt

        # 중력 추가(추가)
        player.top = player.top + y_vel
        y_vel += 1

        if player.bottom >= 765:
            player.bottom = 765
            y_vel = 0

        # 점프 기능(추가)
        if key[K_SPACE] :
            y_vel = -18

        screen.blit(bgImage, (0, 0))
        screen.blit(player_img, player)
        # 플레이어의 행동에대해 결과를 화면에 업데이트 하기위해 선언
        pygame.display.update()
main()