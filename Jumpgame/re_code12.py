import pygame, sys
from pygame.locals import * # pygame에 있는 모든기능을 사용
import re_store
from re_helper import load_image, load_sound, load_image_menu
from re_store import create_feeds

# 악당에 닿으면 GAMEOVER창 띄우기

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

    # 악당 생성
    devil = pygame.Rect(re_store.screen_width-135,re_store.screen_height-135-142,135,135) # 135(캐릭터높이) 142(바닥높이) 5(여유)
    devil_img = load_image('devil.png')

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
    devil_speed = 0.3  # 악당 속도

    # 2단 점프 구현
    jump_count = 2  # 최대 2단점프
    is_jumping = False # 점프 상태 플래그
    jump_timer = 0 # 2단 점프시 이미지 타이머

    # 방향에 따른 이미지 표현
    va = 0

    # 2단 점프 소리 구현
    dbjump_sound = load_sound('one.mp3')
    dbjump_sound.set_volume(0.5) # 0.0 ~ 1.0

    # 폰트 객체, 먹이 점수 표기 _ 한국어 쓰고 싶으면 name을 malgungothic 으로
    font = pygame.font.SysFont('malgungothic',30,True,False) # italic : 글자 기울어서 표현
    score = 0

    # GAMEOVER 창 만들기
    overlay1 = pygame.Surface((re_store.screen_width, re_store.screen_height), pygame.SRCALPHA)
    overlay1.fill((0, 0, 0))

    # gameover 상태
    gameover = False

    # 스타(추가)
    stars = []
    star_speed = 10  # 별 속도
    is_attack = False  # 공격 여부

    # 2초 후 함수실행을 위해
    TIMER_EVENT = pygame.USEREVENT + 1
    timer_active = False

    feeds1, feed_img1, feeds, feed_img = create_feeds(foothold)

    # 게임 실행 관련 코드
    while True:
        dt = clock.tick(60)  # 1초에 60번(hz) 업데이트

        # 우측상단 x 표시 누르면 시스템 종료하기
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # TIMER_EVENT 동작
            if event.type == TIMER_EVENT:
                feeds1, feed_img1, feeds, feed_img = create_feeds(foothold)
                pygame.time.set_timer(TIMER_EVENT, 0)
                timer_active = False

        # 평상시에는 배경화면으로 나타내기 (추가_수정)
        if gameover == False :
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

        # 악당 움직이기 (플레이어의 움직임에 따라) (추가_수정)
        if devil.right + 100 < player.left and devil_speed > 0 and player.bottom > foothold.bottom:
        # devil의 오른쪽 영역보다 player의 왼쪽이 더 큰 경우 = 악당보다 오른쪽에 player가 있는경우
        # devil_speed는 양수 (오른쪽에서 왼쪽으로 진행중)
        # player가 foothold보다 밑에 있는 경우
            if devil_speed > 0:
                devil_speed = -devil_speed

        elif player.right < devil.left - 100 and devil_speed < 0 and player.bottom > foothold.bottom:
            if devil_speed < 0:
                devil_speed = -devil_speed

        # 악당 좌우이동구현
        devil.left -= devil_speed * dt

        if devil.right >= re_store.screen_width:
            devil.right = re_store.screen_width
            devil_speed *= -1
        elif devil.left <= 0:
            devil.left = 0
            devil_speed *= -1

        # 악당과 플레이어가 충돌했을때
        elif devil.colliderect(player):
            gameover = True

        # 스타 공격(추가)
        if key[K_q] and key[K_RIGHT] and score > 0 and not is_attack:
            star = {
                "rect": pygame.Rect(player.right, player.top + 20, 60, 60),
                "direction": "right"
            }

            star_img = load_image('star.png')
            screen.blit(star_img, star["rect"])
            stars.append(star)  # 별 리스트에 추가
            score -= 1
            is_attack = True  # 잔상처럼 연속 생성 방지

        elif key[K_q] and key[K_LEFT] and score > 0 and not is_attack:
            star = {
                "rect": pygame.Rect(player.left, player.top + 20, 60, 60),
                "direction": "left"
            }
            star_img = load_image('star.png')
            screen.blit(star_img, star["rect"])
            stars.append(star)  # 별 리스트에 추가
            score -= 1
            is_attack = True  # 잔상처럼 연속 생성 방지

        if not key[K_q] and key[K_RIGHT]:
            is_attack = False
        if not key[K_q] and key[K_LEFT]:
            is_attack = False

        new_stars = []

        for star in stars:
            # 별 이동
            if star["direction"] == "right":
                star["rect"].right += star_speed
            else:
                star["rect"].left -= star_speed

            # 충돌 감지
            if star["rect"].colliderect(devil):
                # configure.hp_bs += 1
                print("충돌하였습니다.")
                continue  # 충돌한 별은 리스트에 추가하지 않음 (즉시 삭제됨)
            if star["direction"] == "right" and star["rect"].right < 1750:  # 화면을 벗어나지 않으면 계속 이동
                new_stars.append(star)
            if star["direction"] == "left" and star["rect"].left > 50:  # 화면을 벗어나지 않으면 계속 이동
                new_stars.append(star)

            screen.blit(star_img, star["rect"])  # 별 이미지 그리기

        stars = new_stars  # 리스트 갱신
        # ------------------------------------
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

        # 먹이 추가 및 제거
        # 2층
        for f in feeds:
            if player.colliderect(f):
                print('2층 먹이 제거')
                feeds.remove(f)
                score += 1

            screen.blit(feed_img, f)

        # 1층
        for f in feeds1:
            if player.colliderect(f): #
                print('1층 먹이 제거')
                feeds1.remove(f)
                score += 1
            screen.blit(feed_img1, f)

        # 점수 메시지
        score_message = font.render('SCORE : ' + str(score) , True, (0,0,0))
        screen.blit(score_message,(10,10)) # 왼쪽 상단에 메시지를 위치선언

        # 악당 화면구현
        screen.blit(devil_img, devil)

        # 악당과 충돌시 GAMEOVER
        if gameover == True :
            screen.blit(overlay1, (0, 0))
            lose = pygame.Rect((re_store.screen_width - 400) / 2, (re_store.screen_height - 580) / 2, 350, 160)
            lose_img = load_image_menu('gameover.png')
            lose_img = pygame.transform.scale(lose_img, (400, 200))
            screen.blit(lose_img, lose)

        # 먹이 다먹으면 재생성
        if len(feeds) == 0 and len(feeds1) == 0 and not timer_active:
            print('야호')
            pygame.time.set_timer(TIMER_EVENT, 2000)
            timer_active = True

        # 플레이어의 행동에대해 결과를 화면에 업데이트 하기위해 선언
        pygame.display.update()

main()