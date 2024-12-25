#Создай собственный Шутер!

from pygame import *
from random import randint
win_width = 700
win_height = 500
count = 0
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
kick = mixer.Sound('gluhoy-zvuk-padeniya-myagkogo-predmeta.ogg')
shot = mixer.Sound('fire.ogg')
clock = time.Clock()
FPS = 60
font.init()
font1 = font.SysFont('Arial', 36)
win = font1.render(
    'YOU WIN!', True, (255, 215, 0)
)
lose = font1.render(
    'YOU LOSE!', True, (255, 0, 0)
)
window = display.set_mode(
    (win_width, win_height)
    )
galaxy = transform.scale(
image.load("galaxy.jpg"), 
(win_width, win_height)
)
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 550:
            self.rect.x += self.speed
    def fire(self):
        Player_x = rocket.rect.x
        Player_y = rocket.rect.y
        Player_center_x = rocket.rect.centerx
        Player_top = rocket.rect.top
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)
lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(0, 700)
            self.rect.y = 0
            lost = lost + 1 
            kick.play()
monsters = sprite.Group()
for _ in range(5):
    monster = Enemy('ufo.png', randint(80, 450), 0, 3)
    monsters.add(monster)
class Bullet(GameSprite):
    def update(self):
        self.rect.y +=self.speed
        if self.rect.y <= 0:
            self.kill()
bullets = sprite.Group()
finish = False
rocket = Player('rocket.png', 300, 400, 9)
asteroids = sprite.Group()
for i in range(3):
        asteroid = Enemy('asteroid.png', randint(80, 450), 0, 3)
        asteroids.add(asteroid)
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
                run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                shot.play()
    if finish != True:
        window.blit(galaxy, (0, 0))
        rocket.update()
        rocket.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        sprites_lists = sprite.groupcollide(monsters, bullets, True, True)
        collide_a = sprite.spritecollide(rocket, asteroids, False)
        for i in sprites_lists:
            monster = Enemy('ufo.png', randint(80, 450), 0, 3)
            monsters.add(monster)
            count +=1
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (1, 20))
        text_count = font1.render('Счёт: ' + str(count), 1, (255, 255, 255))
        window.blit(text_count, (1, 1))
        if count >= 10:
            finish = True
            window.blit(win, (300, 250, 200, 200))
        if lost >= 10:
            finish = True
            window.blit(lose, (300, 250, 200, 200))
        if collide_a:
            finish = True
            window.blit(lose, (300, 250, 200, 200))
        display.update()
        clock.tick(FPS)