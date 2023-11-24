from pygame import *
from random import randint

font.init()
mixer.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 36)

window = display.set_mode((700, 500))

missed_enemies = 0
killed_enemies = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (60, 60))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 695:
            self.rect.x += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_SPACE]:
            self.fire()

    def fire(self):
        global fire_timer
        if fire_timer > 0.1:
            bullet = Bullet('laserBullet.png', self.rect.centerx - 5, self.rect.y, 4, 10, 10)
            bullets.append(bullet)
            fire_timer = 0
        fire_timer += dt


class Enemy(GameSprite):
    def update(self):
        global missed_enemies
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            missed_enemies += 1
            self.rect.x = randint(0, 600)
            self.speed = randint(1, 4)


class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (width, height))

    def update(self):
        self.rect.y -= self.speed


dt = 0
fire_timer = 0.09
# mixer.music.load('space.ogg')
# mixer.music.play()
fire = mixer.Sound('fire.ogg')
player = Player('player.png', 500, 420, 4)
enemies = []
enemies.append(Enemy('enemy.png', 100, -100, randint(1, 5)))
enemies.append(Enemy('enemy.png', 150, -100, randint(1, 5)))
enemies.append(Enemy('enemy.png', 200, -100, randint(1, 5)))
enemies.append(Enemy('enemy.png', 250, -100, randint(1, 5)))
enemies.append(Enemy('enemy.png', 300, -100, randint(1, 5)))
enemies.append(Enemy('enemy.png', 350, -100, randint(1, 5)))
enemies.append(Enemy('enemy.png', 400, -100, randint(1, 5)))
enemies.append(Enemy('enemy.png', 450, -100, randint(1, 5)))
enemies.append(Enemy('enemy.png', 500, -100, randint(1, 5)))
enemies.append(Enemy('enemy.png', 550, -100, randint(1, 5)))
bullets = []
display.set_caption('shooter')
background = transform.scale(image.load('planet_3_0.png'), (700, 500))
FPS = 40
game = True
finish = False
clock = time.Clock()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        text_lose = font1.render('Пропущено:' + str(missed_enemies), 1, (255, 255, 255))
        text_killed = font2.render('Убито:' + str(killed_enemies), 1, (255, 255, 255))
        window.blit(background, (0, 0))
        window.blit(text_lose, (20, 20))
        window.blit(text_killed, (20, 50))
        player.reset()
        player.update()
        for enemy in enemies:
            enemy.reset()
            enemy.update()
            if sprite.collide_rect(player, enemy):
                finish = True
            for bullet in bullets:
                if sprite.collide_rect(bullet, enemy):
                    killed_enemies += 1
                    enemy.rect.x = randint(0, 600)
                    enemy.rect.y = -50
                    bullets.remove(bullet)
        for bullet in bullets:
            bullet.reset()
            bullet.update()
            if bullet.rect.y < - 50:
                bullets.remove(bullet)

    display.update()
    dt = clock.tick(FPS) / 1000
