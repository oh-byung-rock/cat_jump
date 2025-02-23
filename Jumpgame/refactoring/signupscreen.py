import pygame, configure, os, sys
from loginscreen import scaled_id_pw

pygame.init()

# 만약 이미지 경로를 못읽는다면 shift + shift 를 누르고 Edit Configurations
# 해당 working directory 경로를 C:/Users/병록/cat_jump/Jumpgame/refactoring 에서 C:/Users/병록/cat_jump/Jumpgame 으로 수정
# 참고로 제가 현재 실행하고있는 파일의 위치는 C:/Users/병록/cat_jump/Jumpgame/refactoring/loginscreen.py 입니다.

def sign_up_screen():
    screen = pygame.display.set_mode((configure.screen_width * 0.75, configure.screen_height * 0.75))
    pygame.display.set_caption('wendy game')

    bgImage = pygame.image.load(os.path.join('pictures', 'sign_up_screen.png'))
    bgImage = pygame.transform.scale(bgImage, (configure.screen_width * 0.75, configure.screen_height * 0.75))

    # check 버튼
    check = pygame.Rect(scaled_id_pw(1, 1, 0)[3]['x'], scaled_id_pw(1, 1, 2)[3]['y']
                          , scaled_id_pw(1, 1, 0)[3]['width'], scaled_id_pw(1, 1, 0)[3]['height'])

    check_img = pygame.image.load(os.path.join('sign', 'check_nc.png'))
    check_img = pygame.transform.scale(check_img, (scaled_id_pw(1, 1, 0)[3]['width'],
                                                       scaled_id_pw(1, 1, 0)[3]['height']))

    clock = pygame.time.Clock()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    # 위치 및 크기 설정
    id_x, id_y = scaled_id_pw(2,2,0)[0]['x'], scaled_id_pw(2,2,0)[0]['y']
    id_width, id_height = scaled_id_pw(2,2,0)[0]['width'], scaled_id_pw(2,2,0)[0]['height']

    pw_x, pw_y = scaled_id_pw(2,2,0)[1]['x'], scaled_id_pw(2,2,0)[1]['y']
    pw_width, pw_height = scaled_id_pw(2,2,0)[1]['width'], scaled_id_pw(2,2,0)[1]['height']

    input_id = pygame.Rect(id_x, id_y, id_width, id_height)
    input_pw = pygame.Rect(pw_x, pw_y, pw_width, pw_height)

    send_button_rect = pygame.Rect(pw_x, pw_y * 1.17, 100, 40)

    font = pygame.font.Font(None, scaled_id_pw(2,2,0)[2])
    user_text_id = ""
    user_text_pw = ""

    active_id = False
    active_pw = False

    while True:
        dt = clock.tick(60)

        screen.blit(bgImage, (0, 0))

        # 입력창 그리기
        # 문제발생 : 테두리가 있는 입력창이 발생
        # '입력창 문제해결' 코드로 해결
        # pygame.draw.rect(screen, BLACK, input_id, 2)
        # pygame.draw.rect(screen, BLACK, input_pw, 2)

        # '입력창 문제해결'
        # 투명한 Surface 생성 (입력창 크기와 동일)
        transparent_surface = pygame.Surface((input_id.width, input_id.height), pygame.SRCALPHA)
        transparent_surface.fill((255, 255, 255, 0))  # 완전 투명

        # 투명 Surface 배치 (입력창을 투명하게)
        screen.blit(transparent_surface, (input_id.x, input_id.y))
        screen.blit(transparent_surface, (input_pw.x, input_pw.y))  # 비밀번호 입력창도 동일

        # 버튼에 마우스 닿으면 이미지 변경
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if check.collidepoint(mouse_x, mouse_y):
            check_img = pygame.image.load(os.path.join('sign', 'check_yc.png'))
            check_img = pygame.transform.scale(check_img,(scaled_id_pw(1, 1,0)[3]['width'], scaled_id_pw(1, 1,0)[3]['height']))
        else:
            check_img = pygame.image.load(os.path.join('sign', 'check_nc.png'))
            check_img = pygame.transform.scale(check_img,(scaled_id_pw(1, 1,0)[3]['width'], scaled_id_pw(1, 1,0)[3]['height']))

        screen.blit(check_img, (scaled_id_pw(1, 1, 0)[3]['x'], scaled_id_pw(1, 1, 2)[3]['y'])) # ★

        # 전송 버튼 그리기
        pygame.draw.rect(screen, BLUE, send_button_rect)
        button_text = font.render("전송", True, WHITE)
        screen.blit(button_text, (send_button_rect.x + 25, send_button_rect.y + 5))

        # 입력된 텍스트 렌더링
        text_surface_id = font.render(user_text_id, True, BLACK)
        # 입력창 커서가 시작되는 시점
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
                    from login import insert_mongo
                    insert_mongo(user_text_id, user_text_pw)
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


