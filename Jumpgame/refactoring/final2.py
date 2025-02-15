import pygame, sys, random, ctypes, os
from pygame.locals import * # pygame에 있는 모든기능을 사용
from create import create
import configure

# 실행파일 만들기 위한 코드
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

# 사운드 관련 (숫자는 이해하지말고 그냥 쓰기)
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050,-16,2,512)

# 함수에서 매개변수를 선언하면 반드시 매개변수를 넣어줘야합니다.
# 하지만 이를 무시하고싶다면 *speed_plus처럼 하면됩니다.
# 하지만 단점이 매개변수를 튜플로 인식하여 연산에서 사용할수없게 됩니다.
def main(speed_plus,stage):
    # screen 이란 객체를 생성
    screen = pygame.display.set_mode((configure.screen_width,configure.screen_height))
    # 제목 생성
    pygame.display.set_caption('cat game')
    bgImage = pygame.image.load(os.path.join('pictures', 'background.jpg'))
    bgImage = pygame.transform.scale(bgImage, (configure.screen_width, configure.screen_height))

    # 플레이어 생성
    # 가로 105, 세로 120 객체를 생성, 이후 객체의 왼쪽상단점의 위치를 다음 좌표로 설정
    player = pygame.Rect( 10, 470, 105,120) # 중력이 있어서 안바꿔도됨
    player_img = pygame.image.load(os.path.join('pictures', 'cat.png')) # 이미지 할당
    # 경로가 바뀌어서 폴더를 못읽어오는 에러 발생
    # 해결 : 절대 경로 기입
    # 기존 : player_img = pygame.image.load('../pictures/cat.png')
    # 수정 : player_img = pygame.image.load(os.path.join('pictures', 'cat.jpg'))

    player_img = pygame.transform.scale(player_img, (105,120)) # 이미지 크기 조정

    devil = pygame.Rect(configure.screen_width,configure.screen_height-135-142,135,135) # 135(캐릭터높이) 142(바닥높이) 5(여유)
    devil_img = pygame.image.load(os.path.join('pictures', 'devil.png'))

    foothold = pygame.Rect((configure.screen_width + 105) / 2, (configure.screen_height) / 2, 345, 81)
    foothold_img = pygame.image.load(os.path.join('pictures', 'foothold.png'))
    foothold_img = pygame.transform.scale(foothold_img, (345, 81)) # 가로, 세로

    player_img_left = pygame.image.load(os.path.join('pictures', 'cat_left.png'))
    player_img_left = pygame.transform.scale(player_img_left, (105, 120))

    player_img_right = pygame.image.load(os.path.join('pictures', 'cat_right.png'))
    player_img_right = pygame.transform.scale(player_img_right, (105, 120))

    player_img_jump = pygame.image.load(os.path.join('pictures', 'cat_jump.png'))
    player_img_jump = pygame.transform.scale(player_img_jump, (105, 120))

    # 게임 속도
    clock = pygame.time.Clock()
    speed = 0.5
    devil_speed = 0.3

    # 중력 표현
    y_vel = 0

    # 방향에 따른 이미지 표현
    va = 0

    # 2단 점프 구현
    jump_count = 2  # 기본 2회 점프 가능 (더블 점프)
    is_jumping = False  # 점프 상태 플래그
    jump_timer = 0

    # 2단 점프 소리 구현
    dbjump_sound = pygame.mixer.Sound(os.path.join('pictures', 'one.mp3'))
    dbjump_sound.set_volume(0.5) # 0.0 ~ 1.0

    # 먹이 1층 2층 구분
    feeds1 = []
    feeds = []

    # 2초 후 함수실행을 위해
    TIMER_EVENT = pygame.USEREVENT + 1
    timer_active = False

    # devil 충돌 후 이벤트
    paused = False
    overlay = pygame.Surface((configure.screen_width, configure.screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))

    overlay1 = pygame.Surface((configure.screen_width, configure.screen_height), pygame.SRCALPHA)
    overlay1.fill((0, 0, 0))
    # 폰트 객체
    font = pygame.font.SysFont('Segoe UI',30,True,False) # italic : 글자 기울어서 표현
    score = 0

    # 스타
    stars = []
    star_speed = 10  # 별 속도
    is_attack = False  # 공격 여부

    # 충돌 시 방향 전환을 방지하는 플래그
    devil_direction_changed = False

    # 버튼 클릭 처리
    back_cu = False
    esc_cu = False
    new_cu = False
    exit_cu = False
    next_cu = False
    do_over_cu = False

    # 승리 및 게임오버
    gameover = False
    wendywin = False

    feed_img, feed_img1, feeds, feeds1 = create(configure.screen_width, configure.screen_height, foothold,feeds,feeds1)
    # 게임 실행에대해 처리되는 코드
    while True:
        dt = clock.tick(60) # 1초에 60번(hz) 업데이트

        # 기능구현 1단계 : x 표시 누르면 시스템 종료하기
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == TIMER_EVENT:
                feed_img, feed_img1, feeds, feeds1 = create(configure.screen_width, configure.screen_height, foothold,feeds,feeds1)
                pygame.time.set_timer(TIMER_EVENT, 0)
                timer_active = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    paused = True
                    esc_cu = True

            if event.type == MOUSEBUTTONDOWN and back_cu:
                paused = False
                esc_cu = False

            if event.type == MOUSEBUTTONDOWN and new_cu:
                main(0,1)

            if event.type == MOUSEBUTTONDOWN and exit_cu:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and next_cu:
                main(0.05,2)

            if event.type == MOUSEBUTTONDOWN and do_over_cu:
                configure.hp_bs = 0
                if stage == 1 :
                    main(0,1)
                else:
                    main(0.05, 2)

        # 플레이어의 움직임 하나하나의 프레임마다 배경을 적용해야되서 while 안에 선언
        # case1. 배경 이미지가 없는 경우
        # screen.fill((255,255,255))

        # case2. 배경 이미지가 있는 경우
        # blit는 bit block image transfer 의 약자로
        # dest는 destination 목적지란 의미지만, 여기서는 이미지가 화면에 배치될 위치를 나타냅니다.
        screen.blit(bgImage, (0,0))

        # 체력바
        hp100 = pygame.Rect(devil.left + 12, devil.top - 25, 135, 135)
        if configure.hp_bs == 0:
            hp100_img = pygame.image.load(os.path.join('pictures', 'hp98.png'))

        elif configure.hp_bs == 1:
            hp100_img = pygame.image.load(os.path.join('pictures', 'hp84.png'))
            if devil_speed < 0:
                devil_speed = -0.3
            else:
                devil_speed = 0.3

        elif configure.hp_bs == 2:
            hp100_img = pygame.image.load(os.path.join('pictures', 'hp70.png'))
            if devil_speed < 0:
                devil_speed = -0.3 - (speed_plus * (configure.hp_bs-1))
            else:
                devil_speed = 0.3 + (speed_plus * (configure.hp_bs-1))
        elif configure.hp_bs == 3:
            hp100_img = pygame.image.load(os.path.join('pictures', 'hp56.png'))
            if devil_speed < 0:
                devil_speed = -0.3 - (speed_plus * (configure.hp_bs - 1))
            else:
                devil_speed = 0.3 + (speed_plus * (configure.hp_bs - 1))
        elif configure.hp_bs == 4:
            hp100_img = pygame.image.load(os.path.join('pictures', 'hp42.png'))
            if devil_speed < 0:
                devil_speed = -0.3 - (speed_plus * (configure.hp_bs - 1))
            else:
                devil_speed = 0.3 + (speed_plus * (configure.hp_bs - 1))
        elif configure.hp_bs == 5:
            hp100_img = pygame.image.load(os.path.join('pictures', 'hp28.png'))
            if devil_speed < 0:
                devil_speed = -0.3 - (speed_plus * (configure.hp_bs - 1))
            else:
                devil_speed = 0.3 + (speed_plus * (configure.hp_bs - 1))
        elif configure.hp_bs == 6:
            hp100_img = pygame.image.load(os.path.join('pictures', 'hp14.png'))
            if devil_speed < 0:
                devil_speed = -0.3 - (speed_plus * (configure.hp_bs - 1))
            else:
                devil_speed = 0.3 + (speed_plus * (configure.hp_bs - 1))
        else:
            hp100_img = pygame.image.load(os.path.join('pictures', 'hp0.png'))
            configure.hp_bs = 0
            paused = True
            wendywin = True

        # 키보드로 플레이어 조종
        key = pygame.key.get_pressed()
        if paused == False:
            if key[K_LEFT] and player.left >= 0 :
                player.left = player.left - speed * dt
                va = 1
            elif key[K_RIGHT] and player.right <= configure.screen_width:
                player.right = player.right + speed * dt
                va = 2
            else :
                va = 0

            print("top",player.top)
            print("dvleft", devil.left)
            print("plri", player.right)
            # 악당 움직이기 (플레이어의 움직임에 따라)
            if devil.right + 100 < player.left and devil_speed > 0 and player.bottom > foothold.bottom:
                if devil_speed > 0 and not devil_direction_changed:
                    devil_speed = -devil_speed
                    devil_direction_changed = True  # 방향 전환 후 플래그 활성화
            elif player.right < devil.left - 100 and devil_speed < 0 and player.bottom > foothold.bottom:
                if devil_speed < 0 and not devil_direction_changed:
                    devil_speed = -devil_speed
                    devil_direction_changed = True
            else:
                devil_direction_changed = False

            devil.left -= devil_speed * dt

            if devil.right >= configure.screen_width:
                devil.right = configure.screen_width
                devil_speed *= -1
            elif devil.left <= 0:
                devil.left = 0
                devil_speed *= -1
            elif devil.colliderect(player):
                gameover = True
                paused = True

            # 스타 공격
            if key[K_q] and key[K_RIGHT] and score > 0 and not is_attack:
                star = {
                    "rect": pygame.Rect(player.right, player.top + 20, 60, 60),
                    "direction": "right"
                }
                star_img = pygame.image.load(os.path.join('pictures', 'star.png'))
                screen.blit(star_img, star["rect"])
                stars.append(star)  # 별 리스트에 추가
                score -= 1
                is_attack = True  # 잔상처럼 연속 생성 방지

            elif key[K_q] and key[K_LEFT] and score > 0 and not is_attack:
                star = {
                    "rect": pygame.Rect(player.left, player.top + 20, 60, 60),
                    "direction": "left"
                }
                star_img = pygame.image.load(os.path.join('pictures', 'star.png'))
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
                    # if star["direction"] == "right" and devil_speed > 0:
                    #     devil_speed *= -1
                    # elif star["direction"] == "left" and devil_speed < 0:
                    #     devil_speed *= -1
                    configure.hp_bs += 1
                    continue  # 충돌한 별은 리스트에 추가하지 않음 (즉시 삭제됨)
                if star["direction"] == "right" and star["rect"].right < 1750:  # 화면을 벗어나지 않으면 계속 이동
                    new_stars.append(star)
                if star["direction"] == "left" and star["rect"].left > 50:  # 화면을 벗어나지 않으면 계속 이동
                    new_stars.append(star)

                screen.blit(star_img, star["rect"])  # 별 이미지 그리기


            stars = new_stars  # 리스트 갱신

        # if key[K_RIGHT] and player.right <= configure.screen_width:
        #     player.right = player.right + speed * dt
        #     va = 2
        # else :
        #     va = 0

        # 점프 구현
        player.top = player.top + y_vel
        y_vel += 1
        if player.bottom >= (configure.screen_height * 0.85):
            player.bottom = (configure.screen_height * 0.85)
            y_vel = 0
            jump_count = 2
            jump_timer = 0

        # 점프 구현 (착지)
        # y_vel이 양수인것은 중력작용
        elif player.colliderect(foothold) and y_vel > 0:
            player.bottom = foothold.top
            y_vel = 0
            jump_count = 2
            jump_timer = 0

        # 점프 구현 (점프)
        elif player.colliderect(foothold) and y_vel < 0: # 점프할때
            player.top = foothold.bottom
            y_vel = 1

        if key[K_SPACE] and jump_count > 0 and not is_jumping :
            if jump_count == 2:
                y_vel = -20  # 첫 점프 18
            elif jump_count == 1:
                dbjump_sound.play()
                y_vel = -22  # 두 번째 점프 20
                jump_timer = 60

            jump_count -= 1  # 점프 횟수 감소
            is_jumping = True  # 점프 상태 시작

        # 점프 키에서 손을 떼면 is_jumping 초기화
        if not key[K_SPACE]:
            is_jumping = False

        if jump_timer > 0:
            va = 3
            jump_timer -= 1

        if va == 1 :
            screen.blit(player_img_left, player)  # 이미지를 플레이어 객체에 그리기, 어려운말로 랜더링(묘사하다라는 사전적 의미)
        elif va == 2 :
            screen.blit(player_img_right, player)
        elif va == 3 :
            screen.blit(player_img_jump, player)
        else :
            screen.blit(player_img, player)
        screen.blit(foothold_img, foothold)

        # 먹이 추가 및 제거
        # 2층
        for f in feeds:
            if player.colliderect(f):
                print('제거1')
                feeds.remove(f)
                score += 1

            screen.blit(feed_img,f)

        # 1층
        for f in feeds1:
            if player.colliderect(f):
                print('제거2')
                feeds1.remove(f)
                score += 1
            if stage == 2 :
                if devil.colliderect(f):
                    if configure.hp_bs > 0 :
                       configure.hp_bs -= 1
                    feeds1.remove(f)
            screen.blit(feed_img1,f)

        # 점수 메시지
        score_message = font.render('SCORE : ' + str(score) , True, (0,0,0))
        screen.blit(score_message,(10,10)) # 왼쪽 상단에 메시지를 위치선언
        screen.blit(devil_img,devil)
        screen.blit(hp100_img, hp100)

        # 먹이 다먹으면 재생성
        if len(feeds) == 0 and len(feeds1) == 0 and not timer_active:
            print('야호')
            pygame.time.set_timer(TIMER_EVENT, 2000)
            timer_active = True

        # 악당 충돌
        if paused:
            # 마우스가 버튼 위로 올린걸 감지
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # 메뉴바 추가
            if wendywin or gameover:
                wwa = 420
            else:
                wwa = 0

            if wendywin:
                screen.blit(overlay1, (0, 0))
                win = pygame.Rect((configure.screen_width-400) / 2, (configure.screen_height-580)/2, 400, 200)
                win_img = pygame.image.load(os.path.join('menu', 'wendywin.png'))
                win_img = pygame.transform.scale(win_img, (400, 200))
                screen.blit(win_img, win)

                if stage == 1 :
                    next = pygame.Rect((configure.screen_width + 350) / 2, (configure.screen_height-415+wwa)/2, 400, 200)
                    if next.collidepoint(mouse_x, mouse_y):
                        next_cu = True
                        next_img = pygame.image.load(os.path.join('menu', 'next_yc.png'))
                    else:
                        next_cu = False
                        next_img = pygame.image.load(os.path.join('menu', 'next_nc.png'))
                    screen.blit(next_img, next)
            elif gameover:
                screen.blit(overlay1, (0, 0))
                lose = pygame.Rect((configure.screen_width - 400) / 2, (configure.screen_height - 580) / 2, 350, 160)
                lose_img = pygame.image.load(os.path.join('menu', 'gameover.png'))
                lose_img = pygame.transform.scale(lose_img, (400, 200))
                screen.blit(lose_img, lose)

                do_over = pygame.Rect((configure.screen_width + 350) / 2, (configure.screen_height-415+wwa)/2, 400, 200)
                if do_over.collidepoint(mouse_x, mouse_y):
                    do_over_cu = True
                    do_over_img = pygame.image.load(os.path.join('menu', 'do_over_yc.png'))
                else:
                    do_over_cu = False
                    do_over_img = pygame.image.load(os.path.join('menu', 'do_over_nc.png'))

                screen.blit(do_over_img, do_over)
            else:
                y_vel = 0  # 고양이가 충돌하자마자 공중에 멈추게하기
                screen.blit(overlay, (0, 0))

            # for event in pygame.event.get():
            #     if event.type == MOUSEBUTTONDOWN and back_cu:
            #         paused = False
            #         esc_cu = False

            # 새게임
            new = pygame.Rect((configure.screen_width-225) / 2, (configure.screen_height-415+wwa)/2, 150, 70)
            if new.collidepoint(mouse_x, mouse_y):
                new_cu = True
                new_img = pygame.image.load(os.path.join('menu', 'new_yc.png'))
            else:
                new_cu = False
                new_img = pygame.image.load(os.path.join('menu', 'new_nc.png'))
            screen.blit(new_img,new)

            # 게임종료
            exit = pygame.Rect((configure.screen_width-225) / 2, (configure.screen_height-105+wwa)/2, 225, 105)
            if exit.collidepoint(mouse_x, mouse_y):
                exit_cu = True
                exit_img = pygame.image.load(os.path.join('menu', 'exit_yc.png'))
                exit_img = pygame.transform.scale(exit_img, (225, 105))
            else:
                exit_cu = False
                exit_img = pygame.image.load(os.path.join('menu', 'exit_nc.png'))
                exit_img = pygame.transform.scale(exit_img, (225, 105))
            screen.blit(exit_img,exit)

            if esc_cu :
                # 뒤로가기
                back = pygame.Rect((configure.screen_width-225) / 2, (configure.screen_height + 205)/2, 225, 105)
                if back.collidepoint(mouse_x, mouse_y):
                    back_cu = True
                    back_img = pygame.image.load(os.path.join('menu', 'back_yc.png'))
                else:
                    back_cu = False
                    back_img = pygame.image.load(os.path.join('menu', 'back_nc.png'))
                screen.blit(back_img, back)

        # 플레이어의 행동에대해 결과를 화면에 업데이트 하기위해 선언
        pygame.display.update()
main(0,1)