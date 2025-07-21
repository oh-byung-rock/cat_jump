import pygame, ctypes, os, random
from re_helper import load_image

# 게임 초기화 정보
pygame.init()
user32 = ctypes.windll.user32
user_width = user32.GetSystemMetrics(0) * 0.95  # 가로 해상도
user_height = user32.GetSystemMetrics(1) * 0.9 # 세로 해상도
screen_width = user_width
screen_height = user_height

# 리팩토링
def create_feeds(foothold_rect):
    feeds1 = []
    feeds = []

    # 1층
    a = int(round(screen_width * 0.11, 0))
    d = 7
    e = 0
    for i in range(d):
        if a > screen_width * 0.93:
            break
        c = random.randint(4, 8)
        if a + (75 * c) > screen_width * 0.93:
            break
        b = random.randint(a, a + (75 * c))
        feed1 = pygame.Rect(b, screen_height * 0.75, 70, 80)
        feeds1.append(feed1)
        a = b + 80
        e += 1

    feed_img1 = load_image('feed.png')
    feed_img1 = pygame.transform.scale(feed_img1, (70, 80))
    print('1층 생성', e)

    # 2층
    a1 = foothold_rect.left
    e1 = 0
    for i in range(d - e):
        if a1 > foothold_rect.right - 75:
            break
        c1 = random.randint(1, 3)
        if a1 + (75 * c1) > foothold_rect.right - 75:
            break
        b1 = random.randint(a1, a1 + (75 * c1))
        feed = pygame.Rect(b1, screen_height * 0.4, 70, 80)
        feeds.append(feed)
        a1 = b1 + 80
        e1 += 1

    feed_img = load_image('feed.png')
    feed_img = pygame.transform.scale(feed_img, (70, 80))
    print('2층 생성', e1)

    return feeds1, feed_img1, feeds, feed_img
