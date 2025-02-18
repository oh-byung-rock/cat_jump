import pygame, configure, os, sys

pygame.init()

# 만약 이미지 경로를 못읽는다면 shift + shift 를 누르고 Edit Configurations
# 해당 working directory 경로를 C:/Users/병록/cat_jump/Jumpgame/refactoring 에서 C:/Users/병록/cat_jump/Jumpgame 으로 수정
# 참고로 제가 현재 실행하고있는 파일의 위치는 C:/Users/병록/cat_jump/Jumpgame/refactoring/loginscreen.py 입니다.

def scaled_id_pw(id_y1,pw_y1):
    if id_y1 == 1 and pw_y1 == 1 :
        id_y1 = 289.9202672558585
        pw_y1 = 338.4862833846612
    elif id_y1 == 2 and pw_y1 == 2 :
        id_y1 = 355.9202672558585
        pw_y1 = 404.4862833846612

    # 기준이 되는 원래 Pygame 창 크기
    base_width = 1368
    base_height = 729

    # ID 객체 (기존 값)
    id_x = 511.78515731903485
    id_y = id_y1
    id_width = 325.2532681896757
    id_height = 28.710889740039597

    # PW 객체 (기존 값)
    pw_x = 511.78515731903485
    pw_y = pw_y1
    pw_width = 325.2532681896757
    pw_height = 28.710889740039597

    # Sign in 객체 (기존 값)
    sing_in_x = 503.7042 + 37.6
    sing_in_y = pw_y1 + 70
    sing_in_width = 169.86 * 1.42
    sing_in_height = 52.2

    # 현재 화면 크기 (변화하는 값)
    new_width = configure.screen_width * 0.75
    new_height = configure.screen_height * 0.75

    # 비율을 적용한 새로운 위치 및 크기
    new_id = {
        "x": (id_x / base_width) * new_width,
        "y": (id_y / base_height) * new_height,
        "width": (id_width / base_width) * new_width,
        "height": (id_height / base_height) * new_height,
    }

    new_pw = {
        "x": (pw_x / base_width) * new_width,
        "y": (pw_y / base_height) * new_height,
        "width": (pw_width / base_width) * new_width,
        "height": (pw_height / base_height) * new_height,
    }

    font_size = round((new_pw["height"] / 28.710889740039597) * 36)
    new_font_size = max(font_size, 1)

    new_sign_in = {
        "x": (sing_in_x / base_width) * new_width,
        "y": (sing_in_y / base_height) * new_height,
        "width": (sing_in_width / base_width) * new_width,
        "height": (sing_in_height / base_height) * new_height,
    }

    return new_id, new_pw, new_font_size, new_sign_in

def loginscreen():
    screen = pygame.display.set_mode((configure.screen_width * 0.75 , configure.screen_height * 0.75 ))
    pygame.display.set_caption('wendy game')

    bgImage = pygame.image.load(os.path.join('sign', 'sign_in_no.png'))
    bgImage = pygame.transform.scale(bgImage, (configure.screen_width * 0.75, configure.screen_height * 0.75))

    sign_in = pygame.image.load(os.path.join('sign', 'sign_in_nc.png'))
    sign_in = pygame.transform.scale(sign_in, (scaled_id_pw(1,1)[3]['width'], scaled_id_pw(1,1)[3]['height']))

    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    # 위치 및 크기 설정
    id_x, id_y = scaled_id_pw(1,1)[0]['x'], scaled_id_pw(1,1)[0]['y']
    print('id',scaled_id_pw(1,1)[0])
    print('pw',scaled_id_pw(1,1)[1])
    print('current',configure.screen_width * 0.75,configure.screen_height * 0.75)
    id_width, id_height = scaled_id_pw(1,1)[0]['width'], scaled_id_pw(1,1)[0]['height']

    pw_x, pw_y = scaled_id_pw(1,1)[1]['x'], scaled_id_pw(1,1)[1]['y']
    pw_width, pw_height = scaled_id_pw(1,1)[1]['width'], scaled_id_pw(1,1)[1]['height']

    input_id = pygame.Rect(id_x, id_y, id_width, id_height)
    input_pw = pygame.Rect(pw_x, pw_y, pw_width, pw_height)

    send_button_rect = pygame.Rect(200, 180, 100, 40)

    font = pygame.font.Font(None, scaled_id_pw(1,1)[2])
    user_text_id = ""
    user_text_pw = ""

    active_id = False
    active_pw = False

    while True:
        dt = clock.tick(60)

        screen.blit(bgImage, (0, 0))
        screen.blit(sign_in, (scaled_id_pw(1,1)[3]['x'], scaled_id_pw(1,1)[3]['y']))

        # 입력창 그리기
        # 문제발생 : 테두리가 있는 입력창이 발생
        # '입력창 문제해결' 코드로 해결
        # pygame.draw.rect(screen, WHITE, input_id)
        # pygame.draw.rect(screen, BLACK, input_pw)

        # '입력창 문제해결'
        # 투명한 Surface 생성 (입력창 크기와 동일)
        transparent_surface = pygame.Surface((input_id.width, input_id.height), pygame.SRCALPHA)
        transparent_surface.fill((255, 255, 255, 0))  # 완전 투명

        # 투명 Surface 배치 (입력창을 투명하게)
        screen.blit(transparent_surface, (input_id.x, input_id.y))
        screen.blit(transparent_surface, (input_pw.x, input_pw.y))  # 비밀번호 입력창도 동일

        # 전송 버튼 그리기
        pygame.draw.rect(screen, BLUE, send_button_rect)
        button_text = font.render("전송", True, WHITE)
        screen.blit(button_text, (send_button_rect.x + 25, send_button_rect.y + 5))

        # 입력된 텍스트 렌더링
        text_surface_id = font.render(user_text_id, True, BLACK)
        screen.blit(text_surface_id, (input_id.x + 10, input_id.y + 10))

        text_surface_pw = font.render(user_text_pw, True, BLACK)
        screen.blit(text_surface_pw, (input_pw.x + 10, input_pw.y + 10))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_id.collidepoint(event.pos):
                    active_id = True
                    active_pw = False  # 아이디 입력창 클릭 시 비밀번호 입력창 비활성화
                elif input_pw.collidepoint(event.pos):
                    active_pw = True
                    active_id = False  # 비밀번호 입력창 클릭 시 아이디 입력창 비활성화
                else:
                    active_id = False
                    active_pw = False

                if send_button_rect.collidepoint(event.pos):  # 전송 버튼 클릭
                    print("입력된 아이디:", user_text_id)
                    print("입력된 비밀번호:", user_text_pw)
                    user_text_id = ""
                    user_text_pw = ""

            if event.type == pygame.KEYDOWN:
                if active_id:
                    if event.key == pygame.K_RETURN:
                        print("입력된 아이디:", user_text_id)
                        user_text_id = ""
                    elif event.key == pygame.K_BACKSPACE:
                        user_text_id = user_text_id[:-1]
                    else:
                        user_text_id += event.unicode

                elif active_pw:
                    if event.key == pygame.K_RETURN:
                        print("입력된 비밀번호:", user_text_pw)
                        user_text_pw = ""
                    elif event.key == pygame.K_BACKSPACE:
                        user_text_pw = user_text_pw[:-1]
                    else:
                        user_text_pw += event.unicode

    pygame.display.update()

if __name__ == "__main__":
    loginscreen()  # 직접 실행할 때만 실행


