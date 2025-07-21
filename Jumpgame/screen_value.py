import pygame, ctypes, os

# 게임 초기화 정보
pygame.init()
user32 = ctypes.windll.user32
user_width = user32.GetSystemMetrics(0) * 0.95  # 가로 해상도
user_height = user32.GetSystemMetrics(1) * 0.9 # 세로 해상도
screen_width = user_width
screen_height = user_height

# 체력바 기본
hp_bs = 0

# 체력 이미지 로드 및 devil_speed 계산 함수
def get_hp_image_and_speed(devil_left, devil_top, speed_plus, devil_speed):
    global hp_bs
    hp100 = pygame.Rect(devil_left + 12, devil_top - 25, 135, 135)

    if hp_bs == 0:
        hp100_img = pygame.image.load(os.path.join('pictures', 'hp98.png'))

    elif hp_bs == 1:
        hp100_img = pygame.image.load(os.path.join('pictures', 'hp84.png'))
        if devil_speed < 0:
            devil_speed = -0.3
        else:
            devil_speed = 0.3

    elif hp_bs == 2:
        hp100_img = pygame.image.load(os.path.join('pictures', 'hp70.png'))
        if devil_speed < 0:
            devil_speed = -0.3 - (speed_plus * (hp_bs - 1))
        else:
            devil_speed = 0.3 + (speed_plus * (hp_bs - 1))
    elif hp_bs == 3:
        hp100_img = pygame.image.load(os.path.join('pictures', 'hp56.png'))
        if devil_speed < 0:
            devil_speed = -0.3 - (speed_plus * (hp_bs - 1))
        else:
            devil_speed = 0.3 + (speed_plus * (hp_bs - 1))
    elif hp_bs == 4:
        hp100_img = pygame.image.load(os.path.join('pictures', 'hp42.png'))
        if devil_speed < 0:
            devil_speed = -0.3 - (speed_plus * (hp_bs - 1))
        else:
            devil_speed = 0.3 + (speed_plus * (hp_bs - 1))
    elif hp_bs == 5:
        hp100_img = pygame.image.load(os.path.join('pictures', 'hp28.png'))
        if devil_speed < 0:
            devil_speed = -0.3 - (speed_plus * (hp_bs - 1))
        else:
            devil_speed = 0.3 + (speed_plus * (hp_bs - 1))
    elif hp_bs == 6:
        hp100_img = pygame.image.load(os.path.join('pictures', 'hp14.png'))
        if devil_speed < 0:
            devil_speed = -0.3 - (speed_plus * (hp_bs - 1))
        else:
            devil_speed = 0.3 + (speed_plus * (hp_bs - 1))
    else:
        hp100_img = pygame.image.load(os.path.join('pictures', 'hp0.png'))


    return hp100, hp100_img, devil_speed