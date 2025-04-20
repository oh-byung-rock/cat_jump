import pygame, random, os

def create2(screen_width, screen_height, foothold,feeds,feeds1):

    # 먹이 객체 리스트(1층)
    a = 200
    d = 7
    e = 0

    for i in range(d):
        if a > screen_width - 115:
            break

        c = random.randint(4, 8)
        if a + (75 * c) > screen_width - 115:
            break

        b = random.randint(a + 75, a + (75 * c))
        feed1 = pygame.Rect(b, screen_height - 142 - 80 - 20, 70, 80)  # 142(지면높이) 80(사료높이) 20(여유)
        feeds1.append(feed1)
        a = b + 80
        e = e + 1
    feed_img1 = pygame.image.load(os.path.join('pictures', 'feed.png'))
    feed_img1 = pygame.transform.scale(feed_img1, (70, 80))  # 객체 맞춰서 이미지를 조정하기
    print('1층생성', e)

    # 먹이 객체 리스트(2층)
    a1 = foothold.left
    e1 = 0
    for i in range(d - e):
        if a1 > foothold.right - 70:
            break
        c1 = random.randint(1, 3)
        if a1 + (75 * c1) > foothold.right - 70:
            break
        b1 = random.randint(a1, a1 + (75 * c1))
        feed = pygame.Rect(b1, foothold.top - 10 - 80, 70, 80)
        feeds.append(feed)
        a1 = b1 + 80
        e1 = e1 + 1
    print('2층 생성', e1)
    feed_img = pygame.image.load(os.path.join('pictures', 'feed.png'))
    feed_img = pygame.transform.scale(feed_img, (70, 80))  # 객체 맞춰서 이미지를 조정하기

    return feed_img, feed_img1, feeds, feeds1