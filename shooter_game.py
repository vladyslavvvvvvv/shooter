import pygame
from random import randint
from time import time

width = 1300
height = 700
FPS = 60

score = 0
lost = 0

window = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.display.set_caption("Гра: Шутер, Автор: Височан Владислав")

background = pygame.transform.scale(pygame.image.load("galaxy.jpg"),
                                     (width,height)
                            )

pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()

pygame.font.init()

font_stat  = pygame.font.Font(None, 36)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x,y, speed, size):
        super().__init__()
        self.image = pygame.transform.scale(
                            pygame.image.load(image),
                            size                            
        )
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys[pygame.K_RIGHT] and self.rect.x < width-70:
            self.rect.x += self.speed

    def fire(self):
        new_bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 8, (15,30))
        bullets.add(new_bullet)
        fire_sound = pygame.mixer.Sound("fire.ogg")
        fire_sound.play()


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed        
        
        if self.rect.y > height:
           self.rect.y = 0
           self.rect.x = randint(10, width-70)
           self.speed = randint(3,6)
           global lost
           lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
           self.kill()



bullets = pygame.sprite.Group()

player = Player("rocket.png", width/2, height-70, 10, (60,70))

enemy_num = 5
enemies = pygame.sprite.Group()

for i in range(enemy_num):
    new_enemy = Enemy("ufo.png", randint(10, width-70), 0, randint(3,5), (60,65))
    enemies.add(new_enemy)

asteroids = pygame.sprite.Group()
asteroids_num = 2

for i in range(asteroids_num):
    new_asteroid = Enemy('asteroid.png', randint(10,width-70), -25, randint(1,3), (60,65))
    asteroids.add(new_asteroid)



game_over = False
finish = False
restart = False
reload_time = False

lives = 3
shots = 5

while not game_over:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
                game_over = True
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                if shots > 0 and not reload_time:
                   player.fire()
                   shots -= 1
                if shots <= 0 and not reload_time:
                    last_shot_time= time()
                    reload_time = True

            if e.key == pygame.K_r:
                restart = True
        
        if restart:
            for e in enemies:
                e.kill()
            for b in bullets:
                b.kill()
            for a in asteroids:
                a.kill()
        
            score = 0
            lost  = 0

            player.rect.x = width/2
            for i in range(enemy_num):
                new_enemy = Enemy("ufo.png", randint(10, width-70), 0, randint(3,6), (60,65))
                enemies.add(new_enemy)
            for i in range(asteroids_num):
                new_asteroid = Enemy('asteroid.png', randint(10,width-70), -25, randint(1,3), (60,65))
                asteroids.add(new_asteroid)

        if not finish:
            window.blit(background, (0,0))
            text_score = font_stat.render("Рахунок:" + str(score), True, (255, 255, 255))
            text_lost = font_stat.render("Пропущено:" + str(lost), True, (255, 255, 255))
            window.blit(text_lost, (10,10))
            window.blit(text_score, (10,50))

            player.update()
            player.reset()

            if reload_time:
                cur_time = time()
                if cur_time - last_shot_time > 1:
                   shots = 5
                   reload_time = False
                else:
                    font3 = pygame.font.Font(None, 20)
                    text_reload = font3.render("Перезарядка...", True, (255,0,0))
                    window.blit(text_reload, (player.rect.x,player.rect.y))

            enemies.update()
            enemies.draw(window)

            bullets.update()
            bullets.draw(window)

            asteroids.update()
            asteroids.draw(window)

            collides_ast = pygame.sprite.groupcollide(asteroids, bullets, True, True)
            for c in collides_ast:
                new_asteroid = Enemy('asteroid.png', randint(10,width-70), -25, randint(1,3), (60,65))
                asteroids.add(new_asteroid)
 


            collides = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for c in collides:
                score += 1
                new_enemy = Enemy("ufo.png", randint(10, width-70), 0, randint(3,6), (60,65))
                enemies.add(new_enemy)

            if score >= 10:
                finish = True
                font2 = pygame.font.Font(None,60)
                text_win = font2.render("You WON", True, (0,255,0))
                window.blit(text_win, (width/2, height/2))

            if pygame.sprite.spritecollide(player, enemies, True):
                    lives -= 1
             



            if lives <= 0 or lost >= 5:
                finish = True
                font2 = pygame.font.Font(None, 60)
                text_lose = font2.render("You Lost", True, (255,0,0))
                window.blit(text_lose,(width/2, height/2))

    pygame.display.update()
    clock.tick(FPS)