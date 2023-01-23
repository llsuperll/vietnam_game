import pygame
from pygame import *
from random import *

font.init()

clock = time.Clock()
FPS = 60
lost = 0
score = 0

win_width = 700
win_hight = 500
window = display.set_mode((win_width, win_hight))
display.set_caption('Shoot')
background = transform.scale(image.load('data/viet.jpg'), (win_width, win_hight))

font1 = font.Font(None, 36)

mixer.init()
mixer.music.load('data/beat.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()

amo = sprite.Group()
k = 0


def change_score():
    global score
    score += 1


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, speed, x_size, y_size):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (x_size, y_size))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = speed
        self.x_size = x_size
        self.y_size = y_size

    def spawn(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        if key_pressed[K_d] and self.rect.x < 605:
            self.rect.x += self.speed
        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bull = Bullet('data/patron.png', heli.rect.x + 55, heli.rect.y, 5, 15, 25)
        amo.add(bull)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 400:
            self.rect.y = 0
            self.rect.x = randint(5, 600)
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


heli = Player('data/vert.png', 325, 380, 10, 125, 125)
monsters = sprite.Group()
game = True
while game:
    if not monsters:
        for i in range(10):
            guk = Enemy('data/guk.png', randint(5, 600), 0, randint(1, 5), 125, 125)
            monsters.add(guk)
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                heli.fire()
                k += 1
    collided_guks = pygame.sprite.groupcollide(amo, monsters, True, True)
    if collided_guks:
        for guk in collided_guks:
            change_score()
    key_pressed = key.get_pressed()
    window.blit(background, (0, 0))
    text_lose = font1.render('Пропущено:' + str(lost), 1, (0, 0, 0))
    window.blit(text_lose, (10, 10))
    text_strike = font1.render('Счет:' + str(score), 1, (0, 0, 0))
    window.blit(text_strike, (10, 40))
    text_bullet = font1.render('Выпущено пуль:' + str(k), 1, (0, 0, 0))
    window.blit(text_bullet, (10, 70))
    heli.spawn()
    heli.update()
    amo.update()
    amo.draw(window)
    monsters.draw(window)
    monsters.update()
    clock.tick(FPS)
    display.update()

pygame.quit()
print("Ok")
