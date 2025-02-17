import pygame, configure, os, loginscreen

pygame.init()

# 만약 이미지 경로를 못읽는다면 shift + shift 를 누르고 Edit Configurations
# 해당 working directory 경로를 C:/Users/병록/cat_jump/Jumpgame/refactoring 에서 C:/Users/병록/cat_jump/Jumpgame 으로 수정
# 참고로 제가 현재 실행하고있는 파일의 위치는 C:/Users/병록/cat_jump/Jumpgame/refactoring/loginscreen.py 입니다.

def sign_up_screen():
    screen = pygame.display.set_mode((configure.screen_width * 0.75, configure.screen_height * 0.75))
    pygame.display.set_caption('wendy game')

    bgImage = pygame.image.load(os.path.join('pictures', 'signupscreen.png'))
    bgImage = pygame.transform.scale(bgImage, (configure.screen_width * 0.75, configure.screen_height * 0.75))

    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    # 위치 및 크기 설정
    id_x, id_y = loginscreen.scaled_id_pw()[0]['x'], loginscreen.scaled_id_pw()[0]['y']
    id_width, id_height = loginscreen.scaled_id_pw()[0]['width'], loginscreen.scaled_id_pw()[0]['height']

    pw_x, pw_y = loginscreen.scaled_id_pw()[1]['x'], loginscreen.scaled_id_pw()[1]['y']
    pw_width, pw_height = loginscreen.scaled_id_pw()[1]['width'], loginscreen.scaled_id_pw()[1]['height']

    input_id = pygame.Rect(id_x, id_y, id_width, id_height)
    input_pw = pygame.Rect(pw_x, pw_y, pw_width, pw_height)

    send_button_rect = pygame.Rect(200, 180, 100, 40)

    font = pygame.font.Font(None, 36)
    user_text_id = ""
    user_text_pw = ""

    active_id = False
    active_pw = False

    running = True
    while running:
        dt = clock.tick(60)

        screen.blit(bgImage, (0, 0))

        # 입력창 그리기
        pygame.draw.rect(screen, WHITE, input_id, 2)
        pygame.draw.rect(screen, BLACK, input_pw, 1)

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
                running = False

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

sign_up_screen()

