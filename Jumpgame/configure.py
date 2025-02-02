import pygame, ctypes

# 게임 초기화 정보
pygame.init()
user32 = ctypes.windll.user32
user_width = user32.GetSystemMetrics(0) * 0.95  # 가로 해상도
user_height = user32.GetSystemMetrics(1) * 0.9 # 세로 해상도
screen_width = user_width
screen_height = user_height

# 체력바 기본
hp_bs = 0