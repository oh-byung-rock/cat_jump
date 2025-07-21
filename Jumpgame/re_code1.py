import pygame, sys
from pygame.locals import * # pygame에 있는 모든기능을 사용

# player 와 배경 구현하기 , x버튼 클릭하면 게임종료

def main():
    # 게임 초기화 정보
    pygame.init()
    screen_width = 1800
    screen_height = 900

    # 제목 생성
    pygame.display.set_caption('cat game')

    # screen 객체
    screen = pygame.display.set_mode((screen_width,screen_height))
    bgImag1 = pygame.image.load('pictures/background.jpg')
    bgImag1 = pygame.transform.scale(bgImag1, (screen_width, screen_height))

    # 플레이어 생성
    player = pygame.Rect( 10, 470, 105, 120 ) # (x좌표, y좌표, 가로,세로)
    player_img = pygame.image.load('pictures/cat.png') # 이미지 선택
    player_img = pygame.transform.scale(player_img, (105,120)) # 이미지 크기 조정

    # 전반적인 게임 속도
    clock = pygame.time.Clock()

    # 게임 실행 관련 코드
    while True:
        dt = clock.tick(60) # 1초에 60번(hz) 업데이트

        # 우측상단 x 표시 누르면 시스템 종료하기
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # blit는 bit block transfer의 약자로 조정한 이미지를 화면에 나태내는 기능
        screen.blit(bgImag1, (0, 0))
        screen.blit(player_img, player)

        # 1초에 60번 화면 업데이트
        pygame.display.update()
main()