import pygame, sys, random, ctypes, os
from pygame.locals import *  # pygame에 있는 모든기능을 사용
from create2 import create2
import configure
import sqlite3


# FileNotFoundError 에러 발생시 대처방법
# Alt + Shift + F10 눌러서 경로를 C:/Users/병록/cat_jump/Jumpgame/refactoring 에서 C:/Users/병록/cat_jump/Jumpgame/ 으로

# 3단계 추가

# sqlite3 연동을 위한 코드
# DB 초기화 함수 (최초 1회)
def initialize_db():
    conn = sqlite3.connect('game_data.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS stage_unlocks (
            stage INTEGER PRIMARY KEY,
            status TEXT
        )
    ''')

    cur.execute('SELECT COUNT(*) FROM stage_unlocks')
    if cur.fetchone()[0] == 0:
        cur.executemany('INSERT INTO stage_unlocks (stage, status) VALUES (?, ?)', [
            (1, 'yes'),
            (2, 'lock'),
            (3, 'lock')
        ])

    conn.commit()
    conn.close()

# 현재 각 스테이지 해금 여부를 불러오는 함수
def get_stage_status():
    conn = sqlite3.connect('game_data.db')
    cur = conn.cursor()
    cur.execute('SELECT stage, status FROM stage_unlocks ORDER BY stage')
    status_list = cur.fetchall()
    conn.close()
    return status_list


# 특정 스테이지 해금 (조건 달아 게임 내에서 호출 가능)
def unlock_stage(stage_number):
    conn = sqlite3.connect('game_data.db')
    cur = conn.cursor()
    cur.execute('SELECT status FROM stage_unlocks WHERE stage = ?', (stage_number,))
    result = cur.fetchone()

    if result and result[0] == 'lock':
        cur.execute('UPDATE stage_unlocks SET status = "yes" WHERE stage = ?', (stage_number,))
        print(f"{stage_number}스테이지가 해금되었습니다.")

    conn.commit()
    conn.close()


# 실행파일 만들기 위한 코드
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

# 사운드 관련 (숫자는 이해하지말고 그냥 쓰기)
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 512)


def select_screen():
    screen = pygame.display.set_mode((configure.screen_width, configure.screen_height))
    pygame.display.set_caption("Select Stage")

    player1 = pygame.Rect((configure.screen_width)*0.1, (configure.screen_height)*0.1, 400, 800)
    player2 = pygame.Rect((configure.screen_width)*0.4, (configure.screen_height)*0.1, 400, 800)
    player3 = pygame.Rect((configure.screen_width)*0.7, (configure.screen_height)*0.1, 400, 800)


    while True:
        screen.fill((0, 0, 0))  # 기본 배경

        font = pygame.font.SysFont('Segoe UI', 30, True, False)  # italic : 글자 기울어서 표현

        # 마우스 위치
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if player1.collidepoint(mouse_x, mouse_y):
            player1_cu = True
            player_img1 = pygame.image.load(os.path.join('pictures', 'default_wen1.png'))  # 이미지 할당
        else:
            player1_cu = False
            player_img1 = pygame.image.load(os.path.join('pictures', 'default_wen.png'))  # 이미지 할당

        if player2.collidepoint(mouse_x, mouse_y):
            player2_cu = True
            player_img2 = pygame.image.load(os.path.join('pictures', 'new_wen_can_choice1.png'))  # 이미지 할당
        else:
            player2_cu = False
            player_img2 = pygame.image.load(os.path.join('pictures', 'new_wen_can_choice.png'))  # 이미지 할당

        if player3.collidepoint(mouse_x, mouse_y):
            player3_cu = True
            player_img3 = pygame.image.load(os.path.join('pictures', 'retre_choice.png'))  # 이미지 할당
        else:
            player3_cu = False
            player_img3 = pygame.image.load(os.path.join('pictures', 'retre_choice1.png'))  # 이미지 할당

        player_img1 = pygame.transform.scale(player_img1, (400, 800))  # 이미지 크기 조정
        player_img2 = pygame.transform.scale(player_img2, (400, 800))  # 이미지 크기 조정
        player_img3 = pygame.transform.scale(player_img3, (400, 800))  # 이미지 크기 조정

        screen.blit(player_img1, player1)
        screen.blit(player_img2, player2)
        screen.blit(player_img3, player3)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and (player1_cu or player2_cu or player3_cu):
                if player1_cu:
                    main(0, 1,0)  # 게임 본편 진입
                elif player2_cu:
                    main(0, 1,1)  # 게임 본편 진입
                elif player3_cu:
                    main(0, 1,2)  # 게임 본편 진입
                return  # select_screen 종료

        status_list = get_stage_status()
        for idx, (s, st) in enumerate(status_list):
            line = f"Stage {s}: {st}"
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (20, 20 + idx * 40))

        pygame.display.update()


# 함수에서 매개변수를 선언하면 반드시 매개변수를 넣어줘야합니다.
# 하지만 이를 무시하고싶다면 *speed_plus처럼 하면됩니다.
# 하지만 단점이 매개변수를 튜플로 인식하여 연산에서 사용할수없게 됩니다.
def main(speed_plus, stage,char_num):
    initialize_db()

    char = [ [ "cat.png", "cat_left.png", "cat_right.png","cat_jump.png" ],
             ["new_wen_front.png", "wendy_left_final.png", "wendy_right_final.png","cat_jump.png"],
             ["retre_front.png", "retre_left.png", "retre_right.png","retre_jump.png"]]

    # screen 이란 객체를 생성
    screen = pygame.display.set_mode((configure.screen_width, configure.screen_height))
    # 제목 생성
    pygame.display.set_caption('cat game')
    # 배경이미지(추가)
    bgImage = pygame.image.load(os.path.join('pictures', 'background.jpg'))
    bgImage = pygame.transform.scale(bgImage, (configure.screen_width, configure.screen_height))
    bgImage2 = pygame.image.load(os.path.join('pictures', 'background_eve.jpg'))
    bgImage2 = pygame.transform.scale(bgImage2, (configure.screen_width, configure.screen_height))

    # 플레이어 생성(추가)
    # 가로 105, 세로 120 객체를 생성, 이후 객체의 왼쪽상단점의 위치를 다음 좌표로 설정
    player = pygame.Rect(10, 470, 105, 120)  # 중력이 있어서 안바꿔도됨
    player_img = pygame.image.load(os.path.join('pictures', char[char_num][0]))  # 이미지 할당
    player_img = pygame.transform.scale(player_img, (105, 120))  # 이미지 크기 조정

    # 경로가 바뀌어서 폴더를 못읽어오는 에러 발생
    # 해결 : 절대 경로 기입
    # 기존 : player_img = pygame.image.load('../pictures/cat.png')
    # 수정 : player_img = pygame.image.load(os.path.join('pictures', 'cat.jpg'))

    devil = pygame.Rect(configure.screen_width, configure.screen_height - 135 - 142, 135,
                        135)  # 135(캐릭터높이) 142(바닥높이) 5(여유)
    devil_img = pygame.image.load(os.path.join('pictures', 'devil.png'))

    foothold = pygame.Rect((configure.screen_width + 105) / 2, (configure.screen_height) / 2, 345, 81)
    foothold_img = pygame.image.load(os.path.join('pictures', 'foothold.png'))
    foothold_img = pygame.transform.scale(foothold_img, (345, 81))  # 가로, 세로

    player_img_left = pygame.image.load(os.path.join('pictures', char[char_num][1]))
    player_img_left = pygame.transform.scale(player_img_left, (105, 120))

    player_img_right = pygame.image.load(os.path.join('pictures', char[char_num][2]))
    player_img_right = pygame.transform.scale(player_img_right, (105, 120))

    player_img_jump = pygame.image.load(os.path.join('pictures', char[char_num][3]))
    player_img_jump = pygame.transform.scale(player_img_jump, (105, 120))

    # 게임 속도
    clock = pygame.time.Clock()
    speed = 0.7
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
    dbjump_sound.set_volume(0.5)  # 0.0 ~ 1.0

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

    select_screen = pygame.Surface((configure.screen_width, configure.screen_height), pygame.SRCALPHA)
    select_screen.fill((0, 0, 0))
    # 폰트 객체
    font = pygame.font.SysFont('Segoe UI', 30, True, False)  # italic : 글자 기울어서 표현
    score = 0

    # 스타
    stars = []
    star_speed = 10  # 별 속도
    is_attack = False  # 공격 여부

    # 충돌 시 방향 전환을 방지하는 플래그
    # devil_direction_changed = False

    # 버튼 클릭 처리
    back_cu = False
    esc_cu = False
    new_cu = False
    exit_cu = False
    next_cu = False
    do_over_cu = False
    test_cu = False

    # 승리 및 게임오버
    gameover = False
    wendywin = False

    configure.hp_bs = 0

    feed_img, feed_img1, feeds, feeds1 = create2(configure.screen_width, configure.screen_height, foothold, feeds,
                                                 feeds1)

    # 별 떨어지기 (추가)
    def play_star():
        stars2 = []
        start = random.randint(200, int(configure.screen_width * 0.3))
        for _ in range(2):
            if start > configure.screen_width * 0.9:
                continue
            c = random.randint(3, 6)
            end = min(start + (200 * c), int(configure.screen_width * 0.9))
            b = random.randint(start, end)
            start = b + (50 * c)
            stars2.append({"rect": pygame.Rect(b, 0, 67, 61), "tt": 30})  # 87,81
        return stars2

    stars2 = play_star()
    star_speed2, star_left_speed2 = 5, 2

    # 게임 실행에대해 처리되는 코드
    while True:
        dt = clock.tick(60)  # 1초에 60번(hz) 업데이트

        # 기능구현 1단계 : x 표시 누르면 시스템 종료하기
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == TIMER_EVENT:
                feed_img, feed_img1, feeds, feeds1 = create2(configure.screen_width, configure.screen_height, foothold,
                                                             feeds, feeds1)
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
                main(0, 1,char_num)

            if event.type == MOUSEBUTTONDOWN and exit_cu:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN and next_cu:
                if stage == 1:
                    unlock_stage(2)
                    main(0.05, 2,char_num)
                elif stage == 2:
                    unlock_stage(3)
                    main(0.05, 3,char_num)

            if event.type == MOUSEBUTTONDOWN and do_over_cu:
                configure.hp_bs = 0
                if stage == 1:
                    main(0, 1,char_num)
                elif stage == 2:
                    main(0.05, 2,char_num)
                else:
                    main(0.05, 3,char_num)

            if event.type == MOUSEBUTTONDOWN and test_cu:
                main(0, 1,char_num)

        # 플레이어의 움직임 하나하나의 프레임마다 배경을 적용해야되서 while 안에 선언
        # case1. 배경 이미지가 없는 경우
        # screen.fill((255,255,255))

        # case2. 배경 이미지가 있는 경우
        # blit는 bit block image transfer 의 약자로
        # dest는 destination 목적지란 의미지만, 여기서는 이미지가 화면에 배치될 위치를 나타냅니다.
        if stage == 3:
            screen.blit(bgImage2, (0, 0))
        else:
            screen.blit(bgImage, (0, 0))

        hp100, hp100_img, devil_speed, hp_bs = configure.get_hp_image_and_speed(devil.left, devil.top, speed_plus,
                                                                                devil_speed)

        print('티수', hp_bs)
        if hp_bs >= 7:
            print("한번깸")
            paused = True
            wendywin = True

        # 키보드로 플레이어 조종
        key = pygame.key.get_pressed()
        if paused == False:
            if key[K_LEFT] and player.left >= 0:
                player.left = player.left - speed * dt
                va = 1
            elif key[K_RIGHT] and player.right <= configure.screen_width:
                player.right = player.right + speed * dt
                va = 2
            else:
                va = 0

            print("top", player.top)
            print("dvleft", devil.left)
            print("plri", player.right)
            # 악당 움직이기 (플레이어의 움직임에 따라)
            if devil.right + 100 < player.left and devil_speed > 0 and player.bottom > foothold.bottom:
                # if devil_speed > 0 and not devil_direction_changed: 원래코드
                if devil_speed > 0:
                    devil_speed = -devil_speed
                    # devil_direction_changed = True  # 방향 전환 후 플래그 활성화
            elif player.right < devil.left - 100 and devil_speed < 0 and player.bottom > foothold.bottom:
                # if devil_speed < 0 and not devil_direction_changed:
                if devil_speed < 0:
                    devil_speed = -devil_speed
            #         devil_direction_changed = True
            # else:
            #     devil_direction_changed = False

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

        # 별 아래로 내리기(추가)
        if stage == 3:
            new_stars2 = []

            for star in stars2:
                star["rect"].top += star_speed2  # 별이 아래로 이동
                star["rect"].left -= star_left_speed2  # 별이 왼쪽으로 이동

                if star["rect"].colliderect(player):
                    gameover = True
                    paused = True
                elif star["rect"].top >= configure.screen_height * 0.8:
                    new_stars2 = []
                else:
                    new_stars2.append(star)

                if star["tt"] > 0:
                    star["tt"] -= 1
                    star_img2 = pygame.image.load('pictures/meteo_star.png')
                else:
                    star_img2 = pygame.image.load('pictures/meteo.png')

                screen.blit(star_img2, star["rect"])

            stars2 = new_stars2 if new_stars2 else play_star()

        # 점프 구현
        player.top = player.top + y_vel
        y_vel += 0.9
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
        elif player.colliderect(foothold) and y_vel < 0:  # 점프할때
            player.top = foothold.bottom
            y_vel = 1

        if key[K_SPACE] and jump_count > 0 and not is_jumping:
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

        if va == 1:
            screen.blit(player_img_left, player)  # 이미지를 플레이어 객체에 그리기, 어려운말로 랜더링(묘사하다라는 사전적 의미)
        elif va == 2:
            screen.blit(player_img_right, player)
        elif va == 3:
            screen.blit(player_img_jump, player)
        else:
            screen.blit(player_img, player)
        screen.blit(foothold_img, foothold)

        # 먹이 추가 및 제거
        # 2층
        for f in feeds:
            if player.colliderect(f):
                print('제거1')
                feeds.remove(f)
                score += 1

            screen.blit(feed_img, f)

        # 1층
        for f in feeds1:
            if player.colliderect(f):
                print('제거2')
                feeds1.remove(f)
                score += 1
            if stage != 1:
                if devil.colliderect(f):
                    if configure.hp_bs > 0:
                        configure.hp_bs -= 1
                    feeds1.remove(f)
            screen.blit(feed_img1, f)

        # 점수 메시지
        score_message = font.render('SCORE : ' + str(score), True, (0, 0, 0))
        screen.blit(score_message, (10, 10))  # 왼쪽 상단에 메시지를 위치선언
        screen.blit(devil_img, devil)
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
                win = pygame.Rect((configure.screen_width - 400) / 2, (configure.screen_height - 580) / 2, 400, 200)
                win_img = pygame.image.load(os.path.join('menu', 'wendywin.png'))
                win_img = pygame.transform.scale(win_img, (400, 200))
                screen.blit(win_img, win)

                if stage == 1 or stage == 2:
                    next = pygame.Rect((configure.screen_width + 350) / 2, (configure.screen_height - 415 + wwa) / 2,
                                       400, 200)
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

                do_over = pygame.Rect((configure.screen_width + 350) / 2, (configure.screen_height - 415 + wwa) / 2,
                                      400, 200)
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
            new = pygame.Rect((configure.screen_width - 225) / 2, (configure.screen_height - 415 + wwa) / 2, 150, 70)
            if new.collidepoint(mouse_x, mouse_y):
                new_cu = True
                new_img = pygame.image.load(os.path.join('menu', 'new_yc.png'))
            else:
                new_cu = False
                new_img = pygame.image.load(os.path.join('menu', 'new_nc.png'))
            screen.blit(new_img, new)

            # 게임종료
            exit = pygame.Rect((configure.screen_width - 225) / 2, (configure.screen_height - 105 + wwa) / 2, 225, 105)
            if exit.collidepoint(mouse_x, mouse_y):
                exit_cu = True
                exit_img = pygame.image.load(os.path.join('menu', 'exit_yc.png'))
                exit_img = pygame.transform.scale(exit_img, (225, 105))
            else:
                exit_cu = False
                exit_img = pygame.image.load(os.path.join('menu', 'exit_nc.png'))
                exit_img = pygame.transform.scale(exit_img, (225, 105))
            screen.blit(exit_img, exit)

            if esc_cu:
                # 뒤로가기
                back = pygame.Rect((configure.screen_width - 225) / 2, (configure.screen_height + 205) / 2, 225, 105)
                if back.collidepoint(mouse_x, mouse_y):
                    back_cu = True
                    back_img = pygame.image.load(os.path.join('menu', 'back_yc.png'))
                else:
                    back_cu = False
                    back_img = pygame.image.load(os.path.join('menu', 'back_nc.png'))
                screen.blit(back_img, back)

        # 플레이어의 행동에대해 결과를 화면에 업데이트 하기위해 선언
        pygame.display.update()


# main(0,1)
select_screen()